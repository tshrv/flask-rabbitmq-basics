import json
from enum import Enum

from bson.objectid import ObjectId
from consumer import Consumer
from loguru import logger
from pymongo import MongoClient
from pymongo.collection import Collection

CONNECTION_STRING = "mongodb://db-service"
DB_NAME = 'test-db'
COLLECTION_NAME = 'events'

def get_collection() -> Collection:
    client = MongoClient(CONNECTION_STRING)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    return collection

class EventStatus(Enum):
    PENDING = 'pending'
    COMPLETE = 'complete'

def process_message(channel, method, properties, body) -> None:
    # simulate delay in processing
    import time
    time.sleep(3)

    event = json.loads(body)
    collection = get_collection()
    filter_params = {'_id': ObjectId(event['_id'])}
    update_attrs = {'$set': {'status': EventStatus.COMPLETE.value}}
    rsp = collection.update_one(filter_params, update_attrs)
    logger.debug(rsp.raw_result)
    logger.debug(f"{event['uuid']} completed")

def main() -> None:
    queue_name = 'events'
    consumer = Consumer(queue_name=queue_name, callback=process_message)
    consumer.consume()

if __name__ == '__main__':
    main()