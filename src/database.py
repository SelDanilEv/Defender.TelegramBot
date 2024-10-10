from pymongo import MongoClient
from config import MONGO_URI
from config import logger

client = MongoClient(MONGO_URI)
db = client['local_Defender_TelegramBot']
subscribers_collection = db['subscribers']

def get_subscribers():
    return [sub['chat_id'] for sub in subscribers_collection.find()]

def add_subscriber(chat_id):
    if not subscribers_collection.find_one({'chat_id': chat_id}):
        subscribers_collection.insert_one({'chat_id': chat_id})
        logger.info(f'New subscriber: {chat_id}')

def remove_subscriber(chat_id):
    subscribers_collection.delete_one({'chat_id': chat_id})
    logger.info(f'Unsubscribed: {chat_id}')