from __future__ import print_function
from flask import Flask, request
from sklearn.externals import joblib
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import simplejson as json
from flask.ext.jsonpify import jsonify
from flask.ext.mysql import MySQL
from flask_cors import CORS
import numpy as np
import pandas as pd
import dataClean


app = Flask(__name__)
CORS(app)
api = Api(app)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1314'
app.config['MYSQL_DATABASE_DB'] = 'car'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


@app.route('/cardetail', methods=['GET'])
def get():
    id = request.args.get('id')
    query = "select * from raw_car_data where ProfileId="+str(id) 
    response = access_sql(query)
    return response

@app.route('/predict', methods=['GET','POST'])
def hello():
    if request.method == 'POST':
        param_json = request.get_json()
        model = joblib.load('./model/.pkl')
        raw_df = pd.DataFrame.from_dict(param_json,orient='index').transpose()
        df = dataClean.clean_post_data(raw_df)
        price = str(round(np.exp(model.predict(df)[0]),2))

        jsonData= '{"price":"'+price+'","max":0,"min":0}'
        response = json.loads(jsonData)
        # Get min max Price
        query = "select max(PriceNumeric) as max, min(PriceNumeric) as min from raw_car_data"
        mysql.init_app(app)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                response["max"]= row[0]
                response["min"]=row[1]
        return json.dumps(response)
    return "Please Send post request"
 
@app.route('/getcluster', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        # param_json = request.get_json()
        # raw_df = pd.DataFrame.from_dict(param_json,orient='index').transpose()
        # df = dataClean.clean_post_data(raw_df) 
        # model = joblib.load('./model/svr_2.pkl')
        # cluster = np.asscalar(model.predict(df)[0])
        # Access database to retrive all data in this cluster 
        return "test"
    return "Please Send post request"  

@app.route('/getmapdata', methods=['GET'])
def getmapdata():
    query = "SELECT StateName, count(ProfileId) as number, max(PriceNumeric) as max_price , min(PriceNumeric) as min_price, avg(PriceNumeric) as avg_price, max(KmNumeric) as max_km, min(KmNumeric) as min_km, avg(KmNumeric) as avg_km, max(MakeYear) as max_year, min(MakeYear) as min_year, avg(MakeYear)  as avg_year from raw_car_data group by StateName;"
    response = access_sql(query)
    return response

@app.route('/getamountdata', methods=['GET'])
def getamountdata():
    query = "SELECT count(ProfileId) as count, CarName from raw_car_data group by CarName HAVING count >10 order by CarName ASC;"
    response = access_sql(query)
    return response

@app.route('/getboxplotdata', methods=['GET'])
def getboxplotdata():
    query = "SELECT CarName, GROUP_CONCAT(PriceNumeric) as PriceList FROM `raw_car_data` GROUP BY CarName  HAving count(`ProfileId`) >10 order by CarName ASC;"
    response = access_sql(query)
    return response

@app.route('/getdatabyyear', methods=['GET'])
def getdatabyyear():
    query = "SELECT `MakeYear`, GROUP_CONCAT(PriceNumeric) as PriceList, count(`ProfileId`) as amount FROM `raw_car_data` GROUP BY MakeYear having `MakeYear`>1999 order by `MakeYear` ASC;"
    response = access_sql(query)
    return response
    
def access_sql(query):
    mysql.init_app(app)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    row_headers=[x[0] for x in cursor.description]
    rows = cursor.fetchall()
    if rows:
        result_json=[]
        for result in rows:
            result_json.append(dict(zip(row_headers,result)))
        response = app.response_class(response=json.dumps(result_json,use_decimal=True), status=200, mimetype='application/json')
        return response
    return None


if __name__ == '__main__':
     app.run(port='5002')
     