from __future__ import print_function
from sklearn.externals import joblib
import pandas as pd
import numpy as np
import json


clf = joblib.load('svr.pkl')
x = pd.read_csv("num_X.csv")
print(x.shape)
sample = x.iloc[:1,1:]
print(sample)
sample.to_csv("sample.csv")
price = round(np.exp(clf.predict(sample)[0]),2)
print(price)