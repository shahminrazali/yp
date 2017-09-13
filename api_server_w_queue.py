from rq import Queue
from redis import Redis


from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
import datetime
from task import *

db_connect = create_engine('sqlite:///../yopay.db')
app = Flask(__name__)
api = Api(app)


redis_conn = Redis()
maxis = Queue(name='maxis',connection=redis_conn)  # no args implies the default queue
digi = Queue(name='digi',connection=redis_conn)  # no args implies the default queue
celcom = Queue(name='celcom',connection=redis_conn)  # no args implies the default queue


class Transaction(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from apiserver;") # This line performs query and returns json result
        return {'trans': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID

class Transall(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from apiserver;")
        result = {'Transactions': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Transaction_Status(Resource):
    def get(self, trans_id):
        conn = db_connect.connect()
        query = conn.execute("select * from apiserver where id =%d "  %int(trans_id))
        result = {'Status': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Transaction_New(Resource):
    def post(self):
        args = request.get_json()

        web_id = int(args['web_id'])
        operator = int(args['operator'])
        amount = int(args['amount'])
        phone = args['phone']

        conn = db_connect.connect()
        #query db for web_id, if exist return error
        query = conn.execute("INSERT INTO apiserver (web_id, operator, amount, phone, status) VALUES ({0},{1},{2},{3},{4});".format(web_id, operator, amount, phone, 0))

        result = {"Created": query.rowcount}
        # query = conn.execute("SELECT  status  FROM apiserver WHERE web_id ={}".format(web_id))

        return jsonify(result)

class Status(Resource):
    def get(self, trans_id):
        conn = db_connect.connect()
        query = conn.execute("select status,date_time,message,web_id from apiserver where web_id={}".format(trans_id))


        result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
        if str(result) == "[]":
            abort(404)

        return jsonify(result)

api.add_resource(Transaction, '/trans') # Route_1
api.add_resource(Transall, '/transall') # Route_2
api.add_resource(Transaction_New, '/transaction_new') # Route_2
api.add_resource(Transaction_Status, '/trans/<trans_id>') # Route_3
api.add_resource(Status, '/status/<trans_id>')


if __name__ == '__main__':
     app.run(host='0.0.0.0', port='5050')
