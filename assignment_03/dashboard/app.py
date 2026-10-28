"""Model Evaluation: tune a decision tree and check it with holdout, k-fold and bootstrap validation.

The app shows the results for the settings the user picks. It makes no decisions by itself and uses no AI model.
Run it from comm4259-work with:  streamlit run assignment_03/dashboard/app.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils import resample

DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "titanic_train_clean.csv"
TARGET = "Survived"
POSITIVE = 1

METHODS = ["Holdout", "k-fold cross validation", "Bootstrap"]


@st.cache_data
def load_data():
    """Read the data, drop PassengerId, and split it into features X and target y."""
    df = pd.read_csv(DATA_FILE).drop(columns=["PassengerId"])
    return df.drop(columns=[TARGET]), df[TARGET]


def make_model(max_depth):
    return DecisionTreeClassifier(criterion="entropy", max_depth=max_depth, random_state=42)


def pct(x):
    """Show a rate as a percentage with two decimals."""
    return f"{x * 100:.2f}%"


def holdout_split(X, y, test_size):
    return train_test_split(X, y, test_size=test_size, stratify=y, random_state=1)


def kfold_scores(X, y, max_depth, k):
    skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=1)
    return cross_val_score(make_model(max_depth), X, y, cv=skf, scoring="accuracy")


def bootstrap_scores(X, y, max_depth, rounds):
    """For each round b, train on a bootstrap sample and score on the out-of-bag rows."""
    all_rows = np.arange(len(X))
    scores = []
    for b in range(rounds):
        idx = resample(all_rows, replace=True, n_samples=len(X), random_state=b)
        oob = np.setdiff1d(all_rows, idx)
        model = make_model(max_depth).fit(X.iloc[idx], y.iloc[idx])
        scores.append(accuracy_score(y.iloc[oob], model.predict(X.iloc[oob])))
    return np.array(scores)


X, y = load_data()

st.title("Model Evaluation")
(tab,) = st.tabs(["Model Evaluation"])

with tab:
    st.write(f"Data: `{DATA_FILE.name}` with {len(X)} rows. Target: `{TARGET}`, positive class = {POSITIVE}.")

    # 1. Model setting
    st.header("1. Decision tree")
    max_depth = st.slider("max_depth", min_value=1, max_value=15, value=3)
    st.code(f'model = DecisionTreeClassifier(criterion="entropy", max_depth={max_depth}, random_state=42)')

    # The holdout split is used by sections 2, 3 and 4.
    test_size = st.slider("Test size (holdout)", min_value=0.10, max_value=0.50, value=0.30, step=0.05)
    st.caption("The holdout accuracy, the confusion matrix and the cost all use this split.")
    X_train, X_test, y_train, y_test = holdout_split(X, y, test_size)
    holdout_model = make_model(max_depth).fit(X_train, y_train)
    y_pred = holdout_model.predict(X_test)
    split_code = (
        f"X_train, X_test, y_train, y_test = train_test_split(X, y, test_size={test_size:.2f}, "
        "stratify=y, random_state=1)"
    )

    # 2. Validation method and accuracy
    st.header("2. Validation method")
    method = st.radio("Method", METHODS, horizontal=True)

    if method == "Holdout":
        st.metric("Holdout accuracy", pct(accuracy_score(y_test, y_pred)))
        st.write(f"Train rows: {len(X_train)}, test rows: {len(X_test)}")
        st.code(split_code + "\nmodel.fit(X_train, y_train)\naccuracy_score(y_test, model.predict(X_test))")

    elif method == "k-fold cross validation":
        k = st.slider("k (number of folds)", min_value=3, max_value=10, value=5)
        scores = kfold_scores(X, y, max_depth, k)
        col1, col2 = st.columns(2)
        col1.metric("Mean accuracy", pct(scores.mean()))
        col2.metric("Standard deviation", pct(scores.std()))
        st.dataframe(pd.DataFrame({"Fold": range(1, k + 1), "Accuracy": [pct(s) for s in scores]}), hide_index=True)
        st.code(
            f"skf = StratifiedKFold(n_splits={k}, shuffle=True, random_state=1)\n"
            'scores = cross_val_score(model, X, y, cv=skf, scoring="accuracy")\n'
            "scores.mean(), scores.std()"
        )

    else:
        rounds = st.slider("Bootstrap rounds", min_value=10, max_value=200, value=100)
        scores = bootstrap_scores(X, y, max_depth, rounds)
        low, high = np.percentile(scores, [2.5, 97.5])
        col1, col2 = st.columns(2)
        col1.metric("Mean out-of-bag accuracy", pct(scores.mean()))
        col2.metric("Middle 95%", f"{pct(low)} to {pct(high)}")
        st.code(
            f"for b in range({rounds}):\n"
            "    idx = resample(np.arange(len(X)), replace=True, n_samples=len(X), random_state=b)\n"
            "    oob = np.setdiff1d(np.arange(len(X)), idx)\n"
            "    model.fit(X.iloc[idx], y.iloc[idx])\n"
            "    scores.append(accuracy_score(y.iloc[oob], model.predict(X.iloc[oob])))\n"
            "np.mean(scores), np.percentile(scores, [2.5, 97.5])"
        )

    # 3. Confusion matrix on the holdout split
    st.header("3. Confusion matrix (holdout split)")
    cm = confusion_matrix(y_test, y_pred, labels=[1, 0])
    cm_table = pd.DataFrame(cm, index=["Actual 1", "Actual 0"], columns=["Predicted 1", "Predicted 0"])
    st.dataframe(cm_table)
    tp, fn, fp, tn = cm.ravel()

    col1, col2, col3 = st.columns(3)
    col1.metric("Precision (class 1)", pct(precision_score(y_test, y_pred, pos_label=POSITIVE)))
    col2.metric("Recall (class 1)", pct(recall_score(y_test, y_pred, pos_label=POSITIVE)))
    col3.metric("F1 (class 1)", pct(f1_score(y_test, y_pred, pos_label=POSITIVE)))
    st.code(
        split_code + "\n"
        "y_pred = model.fit(X_train, y_train).predict(X_test)\n"
        "confusion_matrix(y_test, y_pred, labels=[1, 0])\n"
        "precision_score(y_test, y_pred, pos_label=1)\n"
        "recall_score(y_test, y_pred, pos_label=1)\n"
        "f1_score(y_test, y_pred, pos_label=1)"
    )

    # 4. Cost of the errors
    st.header("4. Cost of the holdout predictions")
    col1, col2 = st.columns(2)
    cost_fp = col1.number_input("Cost of one false positive", min_value=0.0, value=1.0)
    cost_fn = col2.number_input("Cost of one false negative", min_value=0.0, value=1.0)
    total_cost = fp * cost_fp + fn * cost_fn
    st.metric("Total cost", f"{total_cost:,.2f}")
    st.write(f"{fp} false positives × {cost_fp:,.2f} + {fn} false negatives × {cost_fn:,.2f} = {total_cost:,.2f}")
    st.code("tp, fn, fp, tn = confusion_matrix(y_test, y_pred, labels=[1, 0]).ravel()\n"
            "total_cost = fp * cost_fp + fn * cost_fn")
