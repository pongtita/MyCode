#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:27:24 2019

@author: pongtit

Purpose:
    Machine Learning team assignment
"""


# Import libraries and data
import pandas as pd
import statsmodels.formula.api as smf
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.metrics


from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


file = 'birthweight_feature_set.xlsx'


bwht = pd.read_excel(file)


########################
# Fundamental Dataset Exploration
########################


# Information about each variable
bwht.info()


# Displaying the first rows of the DataFrame
bwht.head()


# Descriptive statistics
bwht.describe().round(2)


bwht.sort_values('bwght', ascending=False)


##############################################################################
# Impute missing values
##############################################################################


print(
      bwht
      .isnull()
      .sum()
      )


for col in bwht:

    """ Create columns that are 0s if a value was not missing and 1 if
    a value is missing. """

    if bwht[col].isnull().any():
        bwht['m_'+col] = bwht[col].isnull().astype(int)


# Creating a dropped dataset so we could plot a graph to identify which
# values we should use to impute our data.
df_dropped = bwht.dropna()


# Plotting each variable to identify which values we should use to impute
# missing values.
sns.distplot(df_dropped['mage'])
plt.show()


sns.distplot(df_dropped['meduc'])
plt.show()


sns.distplot(df_dropped['monpre'])
plt.show()


sns.distplot(df_dropped['npvis'])
plt.show()


sns.distplot(df_dropped['fage'])
plt.show()


sns.distplot(df_dropped['feduc'])
plt.show()


sns.distplot(df_dropped['omaps'])
plt.show()


sns.distplot(df_dropped['fmaps'])
plt.show()


sns.distplot(df_dropped['cigs'])
plt.show()


sns.distplot(df_dropped['drink'])
plt.show()


sns.distplot(df_dropped['male'])
plt.show()


sns.distplot(df_dropped['mwhte'])
plt.show()


sns.distplot(df_dropped['mblck'])
plt.show()


sns.distplot(df_dropped['moth'])
plt.show()


sns.distplot(df_dropped['fwhte'])
plt.show()


sns.distplot(df_dropped['fblck'])
plt.show()


sns.distplot(df_dropped['foth'])
plt.show()


sns.distplot(df_dropped['bwght'])
plt.show()


# After visual analysis above, we decided to use median to impute
# all missing values.
fill = bwht['meduc'].median()

bwht['meduc'] = bwht['meduc'].fillna(fill)


fill = bwht['npvis'].median()

bwht['npvis'] = bwht['npvis'].fillna(fill)


fill = bwht['feduc'].median()

bwht['feduc'] = bwht['feduc'].fillna(fill)


# Checking the overall dataset to see if there are any remaining
# missing values.
print(
      bwht
      .isnull()
      .any()
      .any()
      )


##############################################################################
# Outliers Analysis
##############################################################################


# We used quantiles to take a first look in the beginning and identify the
# possible outliers which we might flag them.
birth_quantiles = bwht.loc[:, :].quantile([0.20,
                                           0.40,
                                           0.60,
                                           0.80,
                                           1.00])


print(birth_quantiles)


for col in bwht:
    print(col)

########################
# Flagging outliers
########################

# Our outliers come from the combination of external research and the data
# from dataset.
# See Footnote 0 for a more detailed explanation of the outliers.

mage_hi = 55
meduc_lo = 10
monpre_hi = 5
npvis_hi = 20
fage_hi = 53
feduc_lo = 8


# 'Mother age' outliers
bwht['out_mage'] = 0

for val in enumerate(bwht.loc[:, 'mage']):

    if val[1] >= mage_hi:
        bwht.loc[val[0], 'out_mage'] = 1


# 'Mother education' outliers
bwht['out_meduc'] = 0

for val in enumerate(bwht.loc[:, 'meduc']):

    if val[1] <= meduc_lo:
        bwht.loc[val[0], 'out_meduc'] = -1


# 'Month prenatal care began' outliers
bwht['out_monpre'] = 0

for val in enumerate(bwht.loc[:, 'monpre']):

    if val[1] >= monpre_hi:
        bwht.loc[val[0], 'out_monpre'] = 1


# 'Total number of prenatal visits ' outliers
bwht['out_npvis'] = 0

for val in enumerate(bwht.loc[:, 'npvis']):

    if val[1] >= npvis_hi:
        bwht.loc[val[0], 'out_npvis'] = 1


# 'Father age' outliers
bwht['out_fage'] = 0

for val in enumerate(bwht.loc[:, 'fage']):

    if val[1] >= fage_hi:
        bwht.loc[val[0], 'out_fage'] = 1


# 'Father education' outliers
bwht['out_feduc'] = 0

for val in enumerate(bwht.loc[:, 'feduc']):

    if val[1] <= feduc_lo:
        bwht.loc[val[0], 'out_feduc'] = -1


##############################################################################
# Correlation Analysis
##############################################################################


# Using correlation to identify which variables we should consider in our
# Model.
df_corr = bwht.corr().round(2)


print(df_corr)


df_corr.loc['bwght'].sort_values(ascending=False)
'''
By looking at correlation analysis, we found that some varaibles should be
used in our new DataFrame such as average drink per week or average
cigareetes per day.
'''


#############################################################################
# OLS Regression Analysis in statsmodels
#############################################################################


# Drop birthweight because we could not use predict variable to predict model
# Drop omaps and fmaps because they are measured after the birth
bwht_data = bwht.drop(['bwght', 'omaps', 'fmaps'], axis=1)


# Creating target dataset by selecting birthweight which is our
# predict varaible
bwht_target = bwht.loc[:, 'bwght']


# Dividing 10% of our data as our test data while the rest 90% is train data
# We are setting random_state = 508 so we could replicate our work
X_train, X_test, y_train, y_test = train_test_split(
            bwht_data,
            bwht_target,
            test_size=0.1,
            random_state=508
            )


# We need to merge our X_train and y_train sets so that they can be
# used in statsmodels
bwht_train = pd.concat([X_train, y_train], axis=1)


########################
# Applying statmodels to our data
########################


# Step 1: Build the model with all variable to see the model
lm_bwht_qual = smf.ols(
                formula="""bwght ~ mage +
                                   meduc +
                                   monpre +
                                   npvis +
                                   fage +
                                   feduc  +
                                   cigs +
                                   drink +
                                   male +
                                   mwhte +
                                   mblck +
                                   moth +
                                   fwhte +
                                   fblck +
                                   foth +
                                   m_meduc +
                                   m_npvis +
                                   m_feduc +
                                   out_mage +
                                   out_meduc +
                                   out_monpre +
                                   out_npvis +
                                   out_fage +
                                   out_feduc
                                   """, data=bwht_train
                                   )


# Step 2: Fit the model based on the data
lm_results = lm_bwht_qual.fit()


# Step 3: Analyze the summary output. This result after putting all variables
# are not good enough so we have to remove some variables to create
# good model for prediction.
print(lm_results.summary())


###############################################################################
# Applying the Optimal Model in scikit-learn
###############################################################################


# Preparing a DataFrame based the analysis above. We decided to use
# the following variables and test it again.
bwht_sig_data = bwht.loc[:, ['cigs',
                             'drink',
                             'out_mage',
                             'out_fage',
                             'out_feduc',
                             'feduc',
                             'fage']]


# Preparing the target variable
bwht_sig_target = bwht.loc[:, 'bwght']


# Creating train and test set with the new DataFrame
X_train, X_test, y_train, y_test = train_test_split(
            bwht_sig_data,
            bwht_sig_target,
            test_size=0.10,
            random_state=508)


########################
# Using OLS on the optimal model
########################


# Same process of creating train and test sets
X_train, X_test, y_train, y_test = train_test_split(
            bwht_sig_data,
            bwht_sig_target,
            test_size=0.10,
            random_state=508)


# Prepping the Model
lr = LinearRegression()


# Fitting the model
lr_fit = lr.fit(X_train, y_train)


# OLS Predictions which will use to compare with KNN model
lr_pred = lr_fit.predict(X_test)


# Scoring the model
y_score_ols_optimal = lr_fit.score(X_test, y_test)


# The score is directly comparable to R-Square
print(y_score_ols_optimal)


# Comparing the testing score to the training score for our OLS model
print('Training Score:', lr.score(X_train, y_train).round(3))
print('Testing Score:', lr.score(X_test, y_test).round(3))
print("""
      Let's compare the training score and testing score. The training score
      is 0.731 and testing score is 0.707. The results of training and
      testing are not much difference which mean our prediction model is not
      overfitting.
      """)


########################
# Using KNN on the optimal model
########################


# Creating a regressor object
knn_reg = KNeighborsRegressor(algorithm='auto',
                              n_neighbors=1)


# Checking the type of this new object
type(knn_reg)


# Teaching (fitting) the algorithm based on the training data
knn_reg.fit(X_train, y_train)


# Predicting on the X_data that the model has never seen before
y_pred = knn_reg.predict(X_test)


# Calling the score method, which compares the predicted values to the actual
# values
y_score = knn_reg.score(X_test, y_test)


# The score is directly comparable to R-Square. This result is not good
# enough since the number of neighbor is not the suitest number in this
# model.
print(y_score)


########################
# Finding the optimal model
########################


# Same process of creating train and test sets
X_train, X_test, y_train, y_test = train_test_split(
            bwht_sig_data,
            bwht_sig_target,
            test_size=0.10,
            random_state=508)


# Creating two lists, one for training set accuracy and the other for test
# set accuracy
training_accuracy = []
test_accuracy = []


# Building a visualization to check to see  1 to 50
neighbors_settings = range(1, 51)


for n_neighbors in neighbors_settings:
    # Building the model
    clf = KNeighborsRegressor(n_neighbors=n_neighbors)
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
# start at 0. As we got index number 13. It means our k will be 14.
print(test_accuracy.index(max(test_accuracy)))


# According to the result above the best number of neighbor is 14 so we
# will use n_neighbors = 14 for our model
knn_reg = KNeighborsRegressor(algorithm='auto',
                              n_neighbors=14)


# Fitting the model based on the training data
knn_reg_fit = knn_reg.fit(X_train, y_train)


# Scoring the model
y_score_knn_optimal = knn_reg.score(X_test, y_test)


# The score is directly comparable to R-Square.
print(y_score_knn_optimal)
print(f"""
      The result of {y_score_knn_optimal.round(3)} is the best testing score 
      from KNN models which still not good enough when we compared to OLS 
      model.
      """)


# Generating Predictions based on the optimal KNN model
knn_reg_optimal_pred = knn_reg_fit.predict(X_test)


# We calculated mean squared error for both model to use them for our
# root mean squared error to compare how far we are compare to actual data.
lr_mse = sklearn.metrics.mean_squared_error(y_test, lr_pred)
knn_mse = sklearn.metrics.mean_squared_error(y_test, knn_reg_optimal_pred)


# Calculating RMSE to see how far we predict from the actual data itself.
lr_rmse = pd.np.sqrt(lr_mse)
knn_rmse = pd.np.sqrt(knn_mse)


print('OLS_RMSE:', lr_rmse.round(3))
print('KNN_RMSE:', knn_rmse.round(3))
print(f"""
      In this case we could see that OLS model could predict closer to the
      actual data compare to KNN model. OLS model predict about 
      {lr_rmse.round(0)} gram away from the data while KNN predict about 
      {knn_rmse.round(0)} gram away.
      """)


# Comparing our testing score from 2 models which are KNN and OLS.
print('OLS_testing score:', y_score_ols_optimal.round(3))
print('KNN_testing score:', y_score_knn_optimal.round(3))
print(f"""
      Comparing our testing score from OLS and KNN models.
      In this case, we could see that OLS model could predict much better
      than KNN model with test score of {y_score_ols_optimal.round(3)} and
      {y_score_knn_optimal.round(3)} respectively.
      """)


print("""
      In conclusion, from this case, OLS model could predict more accurate
      compare to KNN model.
      """)


# Exporting our prediction from OLS model to excel file.
pred = pd.DataFrame(data=lr_pred, columns=['y_pred'])
pred.to_excel("predicted_values.xlsx")


'''
##############################################################################
# Footnotes
##############################################################################


Footnotes 0

For mother age, 51 is average woman in us for women to start menopause
so comparing that to the data we decided that 55 was a better fit for
the outlier in our case.

For mother / father education, external research indicates that lower
level of education might be correlated with lower ability to care for
the baby while pregnant also in relation to having access to lower levels
and less care thus we decided to create lower flags of education to be
less than hs level of education.

For father age, although the men don't have menopause to worry about and
stay fertile, sperm can lessen with age and that may have an affect on
the baby.

For total number of prenatal visits |, more visits can indicate a higher
level of care or can preface high risk and require more visits both cases
might positively and negatively affect bwght.

For month prenatal care began, earlier access to care can lead to more
education and information about the process, although it means an earlier
start to supplements and caring for the growing child which in turn can
impact bwght.

'''
