import time
from rq import Worker
from rq import get_current_job
import os
from db_ops import *

import maxis_server

from sqlalchemy import create_engine


def maxis_eload(phone,amount):
    port = os.environ.get('SERVER_URL')
    print("SERVER_URL is:", port)
    job_id = get_current_job().get_id()
    print(job_id)
    os.environ['CURRENT_JOB'] = job_id
    
    response = maxis_server.maxis_modem(phone,amount)
    # dbstatus= update_status(job_id = job_id,status=response[0],message=response[3])
    return


def digi_eload(phone, amount):
    time.sleep(3)
    print(os.environ.get('SERVER_URL'))
    job_id = get_current_job().get_id()
    dbstatus= update_status(job_id = job_id,status=1,message="Successfull")

    return dbstatus

def celcom_eload(phone, amount):
    time.sleep(3)
    print(os.environ.get('SERVER_URL'))
    job_id = get_current_job().get_id()
    dbstatus= update_status(job_id = job_id,status=0,message="FAILED")

    return dbstatus

def umobile_eload(phone, amount):
    time.sleep(3)
    print(os.environ.get('SERVER_URL'))
    job_id = get_current_job().get_id()
    dbstatus= update_status(job_id = job_id,status=0,message="FAILED")

    return dbstatus

def tune_eload(phone, amount):
    time.sleep(3)
    print(os.environ.get('SERVER_URL'))
    job_id = get_current_job().get_id()
    dbstatus= update_status(job_id = job_id,status=0,message="FAILED")

    return dbstatus

def onexox_eload(phone, amount):
    time.sleep(3)
    print(os.environ.get('SERVER_URL'))
    job_id = get_current_job().get_id()
    dbstatus= update_status(job_id = job_id,status=0,message="FAILED")

    return dbstatus
