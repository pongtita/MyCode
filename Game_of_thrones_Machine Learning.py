#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:47:34 2019

@author: pongtit

Purpose:
    For machine learning individual assignment
"""


# Import libraries and data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV


file = 'GOT_character_predictions.xlsx'


got = pd.read_excel(file)


########################
# Fundamental Dataset Exploration
########################


# Informaiton about each variable
got.info()


# Descriptive statistics
got.describe()


# Print list of variables name
got.columns.tolist()


##############################################################################
# Impute missing values
##############################################################################


# Check how many missing values we have
print(
      got
      .isnull()
      .sum()
     )


# Missing values imputation
for col in got:

    """ Create columns that are 0s if a value was not missing and 1 if
    a value is missing. """

    if got[col].isnull().any():
        got['m_'+col] = got[col].isnull().astype(int)


# Fixing false birth and age information in the dataset
births = {298299: 298,
          278279: 274}


ages = {-298001: 0,
        -277980: 25}


got['dateOfBirth'].replace(births, inplace=True)


got['age'].replace(ages, inplace=True)


# Fill missing values of title
for i in range(len(got)):
    if got.loc[i, 'isNoble'] == 0:
        if np.where(got['title'].isnull()):
            got.loc[i, 'title'] = 'citizen'


# Fill missing values of spouse. If characters were not married, it mean that
# they are single.
for i in range(len(got)):
    if got.loc[i, 'isMarried'] == 0:
        if np.where(got['spouse'].isnull()):
            got.loc[i, 'spouse'] = 'single'


# Create new columns where it count number of books each character appeared
got['Book_Appearance'] = got['book1_A_Game_Of_Thrones'] + got[
                        'book2_A_Clash_Of_Kings'] + got[
                        'book3_A_Storm_Of_Swords'] + got[
                        'book4_A_Feast_For_Crows'] + got[
                        'book5_A_Dance_with_Dragons']


got['Sum_Books'] = 0


for i in range(len(got)):
    if got.loc[i, 'Book_Appearance'] >= 2:
        got.loc[i, 'Sum_Books'] = 1


got['age'] = got['age'].fillna(got['age'].median())


# Impute the rest missing values with Unknown
fill = 'Unknown'

for val in got:

    if got[val].isnull().any():
        got[val] = got[val].fillna(fill)


# Re-check whether we have missing values left or not
print(
      got
      .isnull()
      .sum()
     )


##############################################################################
# Correlation Analysis
##############################################################################


# Using correlation to identify which variables we should consider in our
# Model.
df_corr = got.corr().round(2)


print(df_corr)


df_corr.loc['isAlive'].sort_values()


##############################################################################
# Data Analysis
##############################################################################


# Preparing a DataFrame based on the analysis. we decided to use
# the following variables and test it.
got_data = got.loc[:, ['S.No',
                       'male',
                       'book1_A_Game_Of_Thrones',
                       'book2_A_Clash_Of_Kings',
                       'book3_A_Storm_Of_Swords',
                       'book4_A_Feast_For_Crows',
                       'book5_A_Dance_with_Dragons',
                       'isMarried',
                       'isNoble',
                       'Book_Appearance',
                       'Sum_Books',
                       'numDeadRelations',
                       'popularity',
                       'm_isAliveSpouse',
                       'm_isAliveHeir',
                       'm_culture',
                       'm_dateOfBirth'
                       ]]


# Creating target dataset by selecting isAlive which is our predict variable
got_target = got.loc[:, 'isAlive']


# Dividing 10% of our data as our test data while the rest 90% is train data
# We are setting random_state = 508 so we could replicate our work
X_train, X_test, y_train, y_test = train_test_split(
            got_data,
            got_target.values.ravel(),
            test_size=0.10,
            random_state=508,
            stratify=got_target)


########################
# Building KNN
########################


# Creating a classifier object
knn_class = KNeighborsClassifier(algorithm='auto',
                                 n_neighbors=1)


# Checking the type of this new object
type(knn_class)


# Teaching (fitting) the algorithm based on the training data
knn_class.fit(X_train, y_train)


# Predicting on the X_data that the model has never seen before
y_pred = knn_class.predict(X_test)


# Calling the score method, which compares the predicted values to the actual
# values
knn_score = knn_class.score(X_test, y_test)


# The score is directly comparable to R-Square. This result is not good
# enough since the number of neighbor is not the suitest number in this
# model.
print(knn_score)


########################
# Building KNN Model on the optimal model
########################


# Creating two lists, one for training set accuracy and the other for test
# set accuracy
training_accuracy = []
test_accuracy = []


# Building a visualization to check to see  1 to 50
neighbors_settings = range(1, 51)


for n_neighbors in neighbors_settings:
    # Building the model
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    clf.fit(X_train, y_train)

    # Recording the training set accuracy
    training_accuracy.append(clf.score(X_train, y_train))

    # Recording the generalization accuracy
    test_accuracy.append(clf.score(X_test, y_test))


# Plotting the visualization
fig, ax = plt.subplots(figsize=(12, 9))
plt.plot(neighbors_settings, training_accuracy, label="training accuracy")
plt.plot(neighbors_settings, test_accuracy, label="test accuracy")
plt.ylabel("Accuracy")
plt.xlabel("n_neighbors")
plt.legend()
plt.show()


# Finding the optimal k, in this case we have to be careful that index will
# start at 0. As we got index number 10. It means our k will be 11.
print(test_accuracy.index(max(test_accuracy)))


# According to the result above the best number of neighbor is 14 so we
# will use n_neighbors = 14 for our model
knn_class = KNeighborsClassifier(n_neighbors=11)


# Fitting the model based on the training data
knn_class_fit = knn_class.fit(X_train, y_train)


# Scoring the model
y_score_knn_optimal = knn_class.score(X_test, y_test)


# The score is directly comparable to R-Square.
print(y_score_knn_optimal)

print("""
      KNN model's score is in acceptable range which is
      {y_score_knn_optimal.round(3)} but this is only the first model we
      build. I think we should try other model before making a conclusion.
      """)


########################
# Building Logistic Regression Model
########################


# Creating the logistic model
log = LogisticRegression(solver='lbfgs', C=1)


# Fitting the model
my_log_fit = log.fit(X_train, y_train)


# Scoring the model
my_log_score = my_log_fit.score(X_test, y_test).round(4)

print("""
      The score from logistic model is slightly higher than KNN model.
      {my_log_score.round(3)} for logistic and {y_score_knn_optimal.round(3)}
      but we have other models which we should take a look before making a
      decision which model we should use for our prediction.
      """)


########################
# Building Classification Trees
########################


class_tree = DecisionTreeClassifier(random_state=508)


class_tree_fit = class_tree.fit(X_train, y_train)


print('Training Score', class_tree_fit.score(X_train, y_train).round(3))
print('Testing Score:', class_tree_fit.score(X_test, y_test).round(3))


####################################
# Optimizing for two hyperparameters
####################################


# Creating a hyperparameter grid
depth_space = pd.np.arange(1, 10)
leaf_space = pd.np.arange(1, 500)


param_grid = {'max_depth': depth_space,
              'min_samples_leaf': leaf_space}


# Building the model object one more time
class_tree_2 = DecisionTreeClassifier(random_state=508)


# Creating a GridSearchCV object
class_tree_2_cv = GridSearchCV(class_tree_2, param_grid, cv=3)


# Fit it to the training data
class_tree_2_cv.fit(X_train, y_train)


# Print the optimal parameters and best score
print("Tuned Logistic Regression Parameter:", class_tree_2_cv.best_params_)
print("Tuned Logistic Regression Accuracy:",
      class_tree_2_cv.best_score_.round(3))

print("""
      The result of the optimal parameters are max depth = 3 and min sameples
      leaf = 149 so we will put those number to the decision tree classifier
      to build the optimal model
      """)


# Building a tree model object with optimal hyperparameters
class_tree_optimal = DecisionTreeClassifier(criterion='gini',
                                            random_state=508,
                                            max_depth=3,
                                            min_samples_leaf=149)


class_tree_optimal_fit = class_tree_optimal.fit(X_train, y_train)
y_pred_tree = class_tree_optimal_fit.predict(X_test)


print('Training Score', class_tree_optimal.score(X_train, y_train).round(3))
print('Testing Score:', class_tree_optimal.score(X_test, y_test).round(3))

print("""
      The result we got is acceptable however it still not good enough so we
      will continue building other model. If the result is good we will come
      back to this model and try to visual it to understand the model.
      However, if the other models could predict better model we will not
      try to visualize this model.
      """)


########################
# Building Random Forest Model
########################


# Create full forest model using "gini"
full_forest_gini = RandomForestClassifier(n_estimators=500,
                                          criterion='gini',
                                          max_depth=None,
                                          min_samples_leaf=15,
                                          bootstrap=True,
                                          warm_start=False,
                                          random_state=508)


# Create full forest model using "entropy"
full_forest_entropy = RandomForestClassifier(n_estimators=500,
                                             criterion='entropy',
                                             max_depth=None,
                                             min_samples_leaf=15,
                                             bootstrap=True,
                                             warm_start=False,
                                             random_state=508)


# Fitting the models
full_gini_fit = full_forest_gini.fit(X_train, y_train)


full_entropy_fit = full_forest_entropy.fit(X_train, y_train)


# Are our predictions the same for each model?
pd.DataFrame(full_gini_fit.predict(X_test), full_entropy_fit.predict(X_test))


full_gini_fit.predict(X_test).sum() == full_entropy_fit.predict(X_test).sum()


# Scoring the gini model
print('Training Score', full_gini_fit.score(X_train, y_train).round(3))
print('Testing Score:', full_gini_fit.score(X_test, y_test).round(3))


# Scoring the entropy model
print('Training Score', full_entropy_fit.score(X_train, y_train).round(3))
print('Testing Score:', full_entropy_fit.score(X_test, y_test).round(3))

print("""
      The result from randomforest is considerably higher than previous models
      but we will use gbm as a last model to make a comparison.
      """)

########################
# Using Gradient Boosting Model
########################


# Building gbm model, see footnote for randomized parameter which I decided
# not to use because I got lower accuracy.
my_gbm = GradientBoostingClassifier(loss='deviance',
                                    learning_rate=0.05,
                                    n_estimators=100,
                                    max_depth=6,
                                    criterion='friedman_mse',
                                    random_state=508)


# Fitting the model
my_gbm_fit = my_gbm.fit(X_train, y_train)


# Make a prediction
my_gbm_predict_test = my_gbm_fit.predict(X_test)
my_gbm_predict_train = my_gbm_fit.predict(X_train)


# Training and Testing Scores
print('Training Score', my_gbm_fit.score(X_train, y_train).round(3))
print('Testing Score:', my_gbm_fit.score(X_test, y_test).round(3))

print("""
      GBM gives us the best result eventhough it is a little bit overfitting
      but it is acceptable so we will use gbm as a model for our prediction
      in this dataset.
      """)

# Giving objective to the score so we could use it for AUC score
gbm_basic_train = my_gbm_fit.score(X_train, y_train)
gmb_basic_test = my_gbm_fit.score(X_test, y_test)


# Cross validation score
cv_gbm_3 = cross_val_score(my_gbm_fit, 
                           got_data, 
                           got_target, 
                           cv=3,
                           scoring = 'roc_auc')
print(cv_gbm_3)

print("""
      In conclusion, from this case the best predict model is Gradient
      Boosting Machine which could predict more accurate than other models.
      """)


##############################################################################
# Model result and decision
##############################################################################


# Summary of the highest AUC's mean after cross validation is as following
print("The summary of our best model which is GBM as following:")
print('Training Score', my_gbm_fit.score(X_train, y_train).round(3))
print('Testing Score:', my_gbm_fit.score(X_test, y_test).round(3))
print('Average: ',
      pd.np.mean(cv_gbm_3).round(3),
      '\nMinimum: ',
      min(cv_gbm_3).round(3),
      '\nMaximum: ',
      max(cv_gbm_3).round(3))


##############################################################################
# Export the prediction to excel
##############################################################################


pred = pd.DataFrame(data=my_gbm_predict_test, columns=['isAlive'])
pred.to_excel("GoT_predicted_values_gbm.xlsx")
