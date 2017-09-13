from rq import Queue
from redis import Redis
import rq_dashboard

from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
import datetime
from task import *
from db_ops import *


app = Flask(__name__)
api = Api(app)

# Tell RQ what Redis connection to use
redis_conn = Redis()

maxis = Queue(name='maxis',connection=redis_conn)  # no args implies the default queue
digi = Queue(name='digi',connection=redis_conn)  # no args implies the default queue
celcom = Queue(name='celcom',connection=redis_conn)  # no args implies the default queue
tune = Queue(name='tune',connection=redis_conn)  # no args implies the default queue
onexox = Queue(name='onexox',connection=redis_conn)  # no args implies the default queue
umobile = Queue(name='umobile',connection=redis_conn)  # no args implies the default queue

app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")


@app.route('/maxis')
def getmaxis():
    operator = "maxis"
    web_id = int(request.args.get("web_id"))
    phone = request.args.get("phone")
    amount = int(request.args.get("amount"))

    status = insert_into(operator,web_id,phone,amount)
    if status == "Success":
        print("MAXIS Created! JOBID is:{}",format(web_id))
        job = maxis.enqueue_call(
            func=maxis_eload, args=(phone,amount) , result_ttl=5000 , timeout = 60, job_id = str(web_id)
        )
        return "MAXIS CREATED:{}".format(web_id), 201

    return abort(403)



@app.route('/digi')
def getdigi():
    operator = "digi"
    web_id = int(request.args.get("web_id"))
    phone = int(request.args.get("phone"))
    amount = int(request.args.get("amount"))

    status = insert_into(operator,web_id,phone,amount)
    if status == "Success":
        print("DIGI Created! JOBID is:{}",format(web_id))
        job = digi.enqueue_call(
            func=digi_eload, args=(phone,amount) , result_ttl=5000 , timeout = 10, job_id = str(web_id)
        )
        return "DIGI CREATED:{}".format(web_id), 201
    return abort(403)


@app.route('/celcom')
def getcelcom():
    operator = "celcom"
    web_id = int(request.args.get("web_id"))
    phone = int(request.args.get("phone"))
    amount = int(request.args.get("amount"))

    status = insert_into(operator,web_id,phone,amount)
    if status == "Success":
        print("CELCOM Created! JOBID is:{}",format(web_id))
        job = celcom.enqueue_call(
            func=celcom_eload, args=(phone,amount) , result_ttl=5000 , timeout = 10, job_id = str(web_id)
        )
        return "CELCOM CREATED:{}".format(web_id), 201
    return abort(403)


@app.route('/umobile')
def getumobile():
    operator = "umobile"
    web_id = int(request.args.get("web_id"))
    phone = int(request.args.get("phone"))
    amount = int(request.args.get("amount"))

    status = insert_into(operator,web_id,phone,amount)
    if status == "Success":
        print("UMOBILE Created! JOBID is:{}",format(web_id))
        job = umobile.enqueue_call(
            func=umobile_eload, args=(phone,amount) , result_ttl=5000 , timeout = 10, job_id = str(web_id)
        )
        return "UMOBILE CREATED:{}".format(web_id), 201
    return abort(403)


@app.route('/tune')
def gettune():
    operator = "tune"
    web_id = int(request.args.get("web_id"))
    phone = int(request.args.get("phone"))
    amount = int(request.args.get("amount"))

    status = insert_into(operator,web_id,phone,amount)
    if status == "Success":
        print("TUNE Created! JOBID is:{}",format(web_id))
        job = tune.enqueue_call(
            func=tune_eload, args=(phone,amount) , result_ttl=5000 , timeout = 10, job_id = str(web_id)
        )
        return "TUNE CREATED:{}".format(web_id), 201
    return abort(403)


@app.route('/onexox')
def getxox():
    operator = "onexox"
    web_id = int(request.args.get("web_id"))
    phone = int(request.args.get("phone"))
    amount = int(request.args.get("amount"))

    status = insert_into(operator,web_id,phone,amount)
    if status == "Success":
        print("ONEXOX Created! JOBID is:{}",format(web_id))
        job = onexox.enqueue_call(
            func=onexox_eload, args=(phone,amount) , result_ttl=5000 , timeout = 10, job_id = str(web_id)
        )
        return "ONEXOX CREATED:{}".format(web_id), 201
    return abort(403)


@app.route('/status/<web_id>')
def getstatus(web_id):
    # conn = connect_db()
    # query = conn.execute("select status,message,web_id from trans where web_id=?", (web_id))
    # result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
    # if str(result) == "[]":
    #     abort(404)
    # return jsonify(result)

    conn= connect_db()
    query = conn.execute("select status from trans where web_id=?",web_id)
    status = [i[0] for i in query.cursor.fetchall()]
    if status == [1]:
        return "success", 200
    elif status == [-1]:
        return "pending", 204
    elif status == [0]:
        return abort(403)
    return abort(404)


if __name__ == '__main__':
     app.run(host='0.0.0.0', port='5151')
