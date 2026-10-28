# Model Evaluation

A Streamlit app with one tab. You set the depth of a decision tree, pick a validation method, and check the accuracy, the confusion matrix and the cost of the errors. The app shows the results for the settings you pick. It makes no decisions by itself and uses no AI model.

The data is `data/titanic_train_clean.csv`. The target is `Survived` and the positive class is 1. The app drops `PassengerId`. The model is `DecisionTreeClassifier(criterion="entropy", random_state=42)`.

## How to run
From the `comm4259-work` folder:
```
pip install -r assignment_03/dashboard/requirements.txt
streamlit run assignment_03/dashboard/app.py
```
The app opens in the browser. If Streamlit asks for an email address, leave it blank and press Enter.

Note: `pyarrow<17` has no wheels for Python 3.14. On Python 3.14, the install of that line can fail. The app runs with the pyarrow that Streamlit already uses.

## How to use
1. **Decision tree.** Set `max_depth` with the slider (1 to 15). Set the test size of the holdout split (0.10 to 0.50, default 0.30). The split is stratified and uses `random_state=1`.
2. **Validation method.** Pick one method:
   - **Holdout:** the accuracy on the test part of the split.
   - **k-fold cross validation:** set k (3 to 10). The app uses `StratifiedKFold(shuffle=True, random_state=1)` and shows the mean and the standard deviation of the fold accuracies.
   - **Bootstrap:** set the number of rounds (10 to 200). Round b draws a sample with `resample(..., random_state=b)` for b = 0, 1, 2, and so on. The app scores each round on the out-of-bag rows and shows the mean and the middle 95% (2.5th to 97.5th percentile).
3. **Confusion matrix.** The matrix uses the same holdout split as step 1. Rows are the actual class and columns are the predicted class, with Survived = 1 first. The app shows precision, recall and F1 for class 1.
4. **Cost.** Enter the cost of one false positive and of one false negative. The app shows the total cost of the holdout predictions.

The app shows every rate as a percentage with two decimals. Under each result, it shows the scikit-learn code that gives the result.
