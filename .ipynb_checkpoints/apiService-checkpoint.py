from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
from flask.ext.mysql import MySQL
from flask_cors import CORS

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
    mysql.init_app(app)
    conn = mysql.connect()
    cursor = conn.cursor()
    id = request.args.get('id')
    json_data=[]
    try:
        try:
            cursor.execute("select * from raw_car_data where ProfileId=%s", str(id)) # This line performs query and returns json result
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
            return None
        row_headers=[x[0] for x in cursor.description]
        rows = cursor.fetchall()
        if rows:
            json_data=[]
            for result in rows:
                json_data.append(dict(zip(row_headers,result)))
            response = app.response_class(response= dumps(json_data), status=200, mimetype='application/json')
            return response
        return None
    finally:
        conn.close()

@app.route('/test', methods=['GET','POST'])
def hello():
    if request.method == 'POST':
        return "post request"
    return "Please Send post request"

@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        
        return "post request"
    return "Please Send post request"
    
        
            
if __name__ == '__main__':
     app.run(port='5002')
     