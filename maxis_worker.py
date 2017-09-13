import os
import sys
import redis
from rq import Worker, Queue, Connection


listen = ['maxis']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    args = sys.argv
    with Connection(conn):
        worker = Worker(map(Queue, listen),name=args[1])
        worker.work()
