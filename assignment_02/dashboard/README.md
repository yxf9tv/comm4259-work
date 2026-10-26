# Data Preparation Workbench

A Streamlit app with one tab. You upload a CSV file, apply data-preparation steps from a menu, and check the effect of each step. The app carries out the steps you pick. It makes no decisions by itself and uses no AI model.

## How to run
From the `comm4259-work` folder:
```
pip install -r assignment_02/dashboard/requirements.txt
streamlit run assignment_02/dashboard/app.py
```
The app opens in the browser. If Streamlit asks for an email address, leave it blank and press Enter.

## How to use
1. **Load data.** Upload a CSV file. If you do not upload one, the app uses `data/titanic_features.csv`. The profile shows the rows, the columns, the type of each column, and the number and share of missing values in each column.
2. **Add steps.** Pick a step and a column, then click **Add step**. The menu has:
   - Drop a column
   - Fill missing values (mean, median, most frequent, or a value you type)
   - Dummy-code a column
   - Drop rows that are missing a value
   - Add a 0/1 flag for "has a value" (for example, HasCabin from Cabin)
3. **Check each step.** For each step, the app shows the rows, columns and missing values before and after, and the pandas line the step equals. **Undo last step** removes the last step.
4. **Download.** Click **Download prepared CSV** to save the prepared data as `titanic_prepared.csv`.

Uploading a different file clears the list of steps.
