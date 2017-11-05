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
from sklearn.metrics import explained_variance_score,mean_absolute_error,mean_squared_error,r2_score
from sklearn.neural_network import MLPRegressor


if __name__ == "__main__":
    df = pd.read_csv("refined_data.csv")
    x = df.drop(['PriceNumeric'], axis=1)
    y = np.log(df.PriceNumeric)

    # Store X y for NN and kmean
    x.to_csv("num_X.csv",index=False)
    df.PriceNumeric.to_csv("num_Y.csv",index=False)

    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,2))
    x['KmNumeric'] = min_max_scaler.fit_transform(x['KmNumeric'].values.reshape(-1,1))
    x['MakeYear'] = (x['MakeYear']-1998)/15

    x.to_csv("minus.csv",index=False)
    # np.savetxt("minmax.csv",x,fmt='%1.3f',delimiter=',')

    # splite data
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42, test_size=.33)

    # liner regression
    lr = linear_model.LinearRegression()
    # SVR
    svr = svm.SVR(kernel='rbf')
    # GB
    gb = ensemble.GradientBoostingRegressor(n_estimators=200, max_depth=15, loss='huber', learning_rate=0.03)
    # random forest
    rf = ensemble.RandomForestRegressor(n_estimators=10)
    # NN
    nn = MLPRegressor(hidden_layer_sizes=(100,50),solver='adam',learning_rate_init=0.01,max_iter=500,activation='relu')

    models = [lr]
    for modelfc in models:
        model = modelfc.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        test_score = r2_score(y_test,y_pred)
        print("rf: ",test_score)

    # store model file in server for API
    joblib.dump(model, './model/lr_new.pkl')

    # plot figure to show the regression
    y_pred = model.predict(x_test)
    plt.scatter(y_pred, y_test, alpha=.65, color='b')
    plt.xlabel('Predicted Price')
    plt.ylabel('Actual Price')
    plt.title('Support Vector Regression Model')
    overlay = 'R^2 is: {}\nRMSE is: {}'.format(test_score, mean_squared_error(y_test, y_pred))
    plt.annotate(s=overlay,xy=(14,12),size='x-large')
    plt.show()
