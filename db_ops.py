from sqlalchemy import create_engine
sqlite_path = 'sqlite:///modemDB.db'

def connect_db():
    return create_engine('sqlite:///modemDB.db').connect()

def insert_into(operator,web_id,phone,amount):
    conn = connect_db()
    try:
        query = conn.execute("INSERT INTO trans (web_id, operator, phone, amount ) VALUES (?,?,?,?);", (web_id, operator, phone, amount))
    except:
        conn.close()
        print("ERROR")
        return "Failed"
    conn.close()
    return "Success"

def update_status(job_id,status,message):
    conn = connect_db()
    # try:
    query = conn.execute("UPDATE trans SET status=?,message=? WHERE web_id=?;", (int(status),message,job_id))
    # except:
    #     print("ERROR")
    #     return "Failed"
    conn.close()
    return "Success"
