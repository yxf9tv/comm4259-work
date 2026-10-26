## Assignment 2

1. Raw shape: (891, 14)
Prepared shape: (889, 18)
Raw columns: Index(['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp',
       'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked', 'FamilySize',
       'IsAlone'],
      dtype='str')
Prepared columns: Index(['PassengerId', 'Survived', 'Age', 'SibSp', 'Parch', 'Fare', 'Cabin',
       'FamilySize', 'IsAlone', 'HasCabin', 'Sex_female', 'Sex_male',
       'Embarked_C', 'Embarked_Q', 'Embarked_S', 'Pclass_1', 'Pclass_2',
       'Pclass_3'],
      dtype='str')
------------
2. Missing Age values remaining: 0

- It all checks out:

Rows count: Raw dataset had 891 rows. The prepared dataset has 889 rows because I dropped the 2 rows with missing values in Embarked. This matches exactly.

Age imputation: Out of 889 passengers, 202 of them now have the exact median age of 28.0, proving the median fill was successful. 

IsAlone feature: Showed that passengers traveling alone survived at a rate of 30.4%, while those with family/others survived at a rate of 50.6%. =
