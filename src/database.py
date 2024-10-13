from dataclasses import asdict
from pymongo import MongoClient
from classes import User
from config import MONGO_URI
from config import logger

client = MongoClient(MONGO_URI)
db = client['local_Defender_TelegramBot']
users_collection = db['users']
cache_collection = db['cache']

def get_subscribers():
    return [User.from_dict(user) for user in users_collection.find()]

def get_active_subscribers():
    return [User.from_dict(user) for user in users_collection.find({'isActive': True, 'isSubscribed': True})]


def subscribe_user(user: User):
    users_collection.update_one({'chat_id': user.chat_id}, {'$set': {'isSubscribed': True}})
    logger.info(f'User subscribed: {user.chat_id}')

def unsubscribe_user(user: User):
    users_collection.update_one({'chat_id': user.chat_id}, {'$set': {'isSubscribed': False}})
    logger.info(f'User subscribed: {user.chat_id}')


def activate_user(user: User):
    users_collection.update_one({'chat_id': user.chat_id}, {'$set': {'isActive': True}})
    logger.info(f'User activated: {user.chat_id}')

def deactivate_user(user: User):
    users_collection.update_one({'chat_id': user.chat_id}, {'$set': {'isActive': False}})
    logger.info(f'User deactivated: {user.chat_id}')

def get_user_by_username(username: str):
    user_doc = users_collection.find_one({'username': username})
    if user_doc:
        return User.from_dict(user_doc)
    return None

def add_user(user: User):
    if not users_collection.find_one({'chat_id': user.chat_id}):
        users_collection.insert_one(asdict(user))
        logger.info(f'New user added: {user.chat_id}')

def remove_user(user: User):
    users_collection.delete_one({'chat_id': user.chat_id})
    logger.info(f'User removed: {user.chat_id}')
    


def add_to_cache(response):
    cache_collection.insert_one(response)
    logger.info(f'Cache added')