from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from sklearn.model_selection import train_test_split
from sklearn import linear_model, ensemble, metrics, gaussian_process
from dataClean import *
from sklearn.svm import SVC
from sklearn import metrics, svm
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib

if __name__ == "__main__":

    df = clean_trainig_data()
    # show all number column
    numeric_features = df.select_dtypes(include=[np.number])

    # correlation
    # corr = numeric_features.corr()
    # print("Correlations:\n")
    # print (corr['PriceNumeric'].sort_values(ascending=False)[:6], '\n')
    # print (corr['PriceNumeric'].sort_values(ascending=False)[-5:])

    # print ("Skew is:", numeric_features.KmNumeric.skew()) # used to check the distribution of value
    # plt.hist(numeric_features.KmNumeric, color='blue')
    # plt.show()
    # sys.exit()

    # Model regression using all number column, use log transform for y
    y = np.log(numeric_features.PriceNumeric)
    temp = pd.DataFrame.copy(numeric_features)

    # Normalization . Method is selected based on distribution
    temp['MakeYear'] = preprocessing.scale(numeric_features.MakeYear)
    temp['KmNumeric'] = preprocessing.minmax_scale(numeric_features.KmNumeric)

    corr = temp.corr()
    print(corr['PriceNumeric'].sort_values(ascending=False)[:6], '\n')
    print(corr['PriceNumeric'].sort_values(ascending=False)[-5:])

    X = temp.drop(['PriceNumeric'], axis=1)

    # Store X y for NN
    X.to_csv("num_X.csv")
    numeric_features.PriceNumeric.to_csv("num_Y.csv")

    # splite data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=42, test_size=.33)

    # liner regression
    lr = linear_model.LinearRegression()
    # SVR
    svr = svm.SVR(kernel='rbf')
    # GB
    gb = ensemble.GradientBoostingRegressor(
        n_estimators=5000, max_depth=10, loss='ls', learning_rate=0.01)
    # random forest
    rf = ensemble.RandomForestRegressor(n_estimators=5000)
    # Gausain process
    gp = gaussian_process.GaussianProcessRegressor()

    # Train model
    model = gb.fit(X_train, y_train)

    # store model file in server for other script
    #joblib.dump(model, 'gb.pkl')

    # Calculate score on test dataset
    test_score = model.score(X_test, y_test)

    # plot figure to show the regression
    predictions = model.predict(X_test)

    print(test_score)
    plt.scatter(predictions, y_test, alpha=.65, color='b')
    plt.xlabel('Predicted Price')
    plt.ylabel('Actual Price')
    plt.title('Support Vector Regression Model')
    overlay = 'R^2 is: {}\nRMSE is: {}'.format(test_score, mean_squared_error(y_test, predictions))
    plt.annotate(s=overlay,xy=(14,12),size='x-large')
    plt.show()
