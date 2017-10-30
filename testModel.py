from __future__ import print_function
from sklearn.externals import joblib
import pandas as pd
import numpy as np


string ="{u'KmNumeric': u'', u'MakeYear': u'', u'BodyStyleId': u'6', u'Color': u'Silver', u'CityName': u'New Delhi', u'Seller': u'Dealer', u'RootName': u'Innova', u'Fuel': u'Diesel', u'GearBox': u'Manual', u'OwnerTypeId': u'1'}"
clf = joblib.load('svr_2.pkl')
x = pd.read_csv("num_X.csv")
print(x.shape)
sample = x.iloc[:1,1:]
print(sample)
sample.to_csv("sample.csv")
price = round(np.exp(clf.predict(sample)[0]),2)
print(price)