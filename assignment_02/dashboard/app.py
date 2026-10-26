"""Data Preparation Workbench: apply data-preparation steps from a menu and check each one.

The app carries out the steps the user picks. It makes no decisions by itself and uses no AI model.
Run it from comm4259-work with:  streamlit run assignment_02/dashboard/app.py
"""
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).parent / "data"
DEFAULT_FILE = DATA_DIR / "titanic_features.csv"

STEP_TYPES = [
    "Drop a column",
    "Fill missing values",
    "Dummy-code a column",
    "Drop rows that are missing a value",
    "Add a 0/1 flag for 'has a value'",
]
FILL_METHODS = ["mean", "median", "most frequent", "a value I type"]


def apply_step(df, step):
    """Apply one step to a copy of df. Return the new table and the pandas line the step equals."""
    col = step["column"]
    kind = step["type"]

    if kind == "Drop a column":
        return df.drop(columns=[col]), f'df = df.drop(columns=["{col}"])'

    if kind == "Fill missing values":
        method = step["method"]
        new_df = df.copy()
        if method == "mean":
            new_df[col] = new_df[col].fillna(new_df[col].mean())
            code = f'df["{col}"] = df["{col}"].fillna(df["{col}"].mean())'
        elif method == "median":
            new_df[col] = new_df[col].fillna(new_df[col].median())
            code = f'df["{col}"] = df["{col}"].fillna(df["{col}"].median())'
        elif method == "most frequent":
            new_df[col] = new_df[col].fillna(new_df[col].mode()[0])
            code = f'df["{col}"] = df["{col}"].fillna(df["{col}"].mode()[0])'
        else:
            value = step["value"]
            new_df[col] = new_df[col].fillna(value)
            code = f'df["{col}"] = df["{col}"].fillna({value!r})'
        return new_df, code

    if kind == "Dummy-code a column":
        return pd.get_dummies(df, columns=[col]), f'df = pd.get_dummies(df, columns=["{col}"])'

    if kind == "Drop rows that are missing a value":
        return df.dropna(subset=[col]), f'df = df.dropna(subset=["{col}"])'

    # Add a 0/1 flag for "has a value"
    new_name = step["new_name"]
    new_df = df.copy()
    new_df[new_name] = new_df[col].notnull().astype(int)
    return new_df, f'df["{new_name}"] = df["{col}"].notnull().astype(int)'


def check_step(df, step):
    """Return an error message if the step cannot run on df, or None if it can."""
    col = step["column"]
    is_number = pd.api.types.is_numeric_dtype(df[col])
    if step["type"] == "Fill missing values":
        if step["method"] in ["mean", "median"] and not is_number:
            return f'"{col}" is not a number column, so it has no {step["method"]}. Pick another method.'
        if step["method"] == "a value I type" and step["value"] == "":
            return "Type a value to fill with."
    if step["type"] == "Add a 0/1 flag for 'has a value'":
        if step["new_name"] == "":
            return "Type a name for the new column."
        if step["new_name"] in df.columns:
            return f'A column "{step["new_name"]}" already exists. Pick another name.'
    return None


def typed_value(text, column):
    """Turn the typed text into a number when the column holds numbers."""
    if pd.api.types.is_numeric_dtype(column):
        try:
            return float(text)
        except ValueError:
            return text
    return text


def profile(df):
    """One row per column: its type, and the number and share of missing values."""
    return pd.DataFrame({
        "type": df.dtypes.astype(str),
        "missing": df.isnull().sum(),
        "missing share": df.isnull().mean().round(3),
    })


def run_steps(raw, steps):
    """Replay every step on the raw data. Return the final table and one summary per step."""
    df = raw
    results = []
    for step in steps:
        new_df, code = apply_step(df, step)
        results.append({
            "step": step,
            "code": code,
            "before": (df.shape[0], df.shape[1], int(df.isnull().sum().sum())),
            "after": (new_df.shape[0], new_df.shape[1], int(new_df.isnull().sum().sum())),
        })
        df = new_df
    return df, results


st.set_page_config(page_title="Data Preparation Workbench", layout="wide")
st.title("Data Preparation Workbench")

(tab,) = st.tabs(["Data Preparation Workbench"])

with tab:
    # 1. Load the data and show a profile
    uploaded = st.file_uploader("Upload a CSV file (or leave empty to use titanic_features.csv)", type="csv")
    if uploaded is not None:
        raw = pd.read_csv(uploaded)
        source = uploaded.name
    else:
        raw = pd.read_csv(DEFAULT_FILE)
        source = DEFAULT_FILE.name

    # A new file starts with an empty list of steps
    if st.session_state.get("source") != source:
        st.session_state["source"] = source
        st.session_state["steps"] = []

    st.subheader(f"Profile of {source}")
    st.write(f"Rows: {raw.shape[0]}  |  Columns: {raw.shape[1]}")
    st.dataframe(profile(raw))

    df, results = run_steps(raw, st.session_state["steps"])

    # 2. Add a step from the fixed menu
    st.subheader("Add a step")
    step_type = st.selectbox("Step", STEP_TYPES)
    column = st.selectbox("Column", list(df.columns))
    step = {"type": step_type, "column": column}
    if step_type == "Fill missing values":
        step["method"] = st.selectbox("Fill with", FILL_METHODS)
        if step["method"] == "a value I type":
            step["value"] = typed_value(st.text_input("Value"), df[column])
    if step_type == "Add a 0/1 flag for 'has a value'":
        step["new_name"] = st.text_input("Name of the new column", value=f"Has{column}")
    if step_type == "Dummy-code a column" and df[column].isnull().any():
        st.warning(f'"{column}" still has missing values. Rows with a missing value get 0 in every new column.')

    left, right = st.columns(2)
    if left.button("Add step"):
        error = check_step(df, step)
        if error:
            st.error(error)
        else:
            st.session_state["steps"] = st.session_state["steps"] + [step]
            st.rerun()
    if right.button("Undo last step", disabled=not st.session_state["steps"]):
        st.session_state["steps"] = st.session_state["steps"][:-1]
        st.rerun()

    # 3. Show each step: before and after, and the pandas line
    st.subheader("Steps")
    if not results:
        st.write("No steps yet.")
    for number, result in enumerate(results, start=1):
        before_rows, before_cols, before_missing = result["before"]
        after_rows, after_cols, after_missing = result["after"]
        st.markdown(f"**Step {number}: {result['step']['type']} ({result['step']['column']})**")
        st.code(result["code"], language="python")
        st.write(
            f"Rows {before_rows} → {after_rows}  |  "
            f"Columns {before_cols} → {after_cols}  |  "
            f"Missing values {before_missing} → {after_missing}"
        )

    # 4. Show and download the prepared data
    st.subheader("Prepared data")
    st.write(f"Rows: {df.shape[0]}  |  Columns: {df.shape[1]}")
    st.dataframe(profile(df))
    st.dataframe(df.head(10))
    st.download_button(
        "Download prepared CSV",
        data=df.to_csv(index=False),
        file_name="titanic_prepared.csv",
        mime="text/csv",
    )
