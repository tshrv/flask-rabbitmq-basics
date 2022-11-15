from producer import Producer
from flask import Flask, request
from enum import Enum
from uuid import uuid4
from loguru import logger
from pymongo import MongoClient
from pymongo.collection import Collection
import json

CONNECTION_STRING = "mongodb://db-service"
DB_NAME = 'test-db'
COLLECTION_NAME = 'events'

app = Flask(__name__)

def get_collection() -> Collection:
    client = MongoClient(CONNECTION_STRING)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    return collection

class EventStatus(Enum):
    PENDING = 'pending'
    COMPLETE = 'complete'

@app.route('/', methods=['GET'])
def root():
    event_name = request.args.get("event-name", None)
    new_record = {
        'uuid': str(uuid4()),
        'event_name': event_name,
        'status': EventStatus.PENDING.value,
    }
    logger.debug(new_record)
    logger.debug('-'*50)
    collection = get_collection()
    collection.insert_one(new_record)

    # data serialization
    new_record['_id'] = str(new_record['_id'])

    # send event to message queue
    queue_name = 'events'
    Producer(queue_name=queue_name).send(message=json.dumps(new_record))

    response = {
        'data': [],
        'count': 0,
    }
    query = {'status': EventStatus.PENDING.value}
    projection = {'_id': 0, 'uuid': 1, 'event_name': 1, 'status': 1}
    pending_records = collection.find(query, projection)
    for record in pending_records:
        response['data'].append(record)
    
    response['count'] = len(response['data'])

    logger.debug('*'*50)
    return response
