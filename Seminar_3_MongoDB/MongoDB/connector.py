import os

import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv

from Seminar_3_MongoDB.MongoDB.crud import upload_data, create_new_book, select_book, update_book, delete_book

load_dotenv()
mongo_url = os.getenv('MONGO_URL')
mongo_database = os.getenv('DB_NAME')
mongo_collection = os.getenv('DB_COLLECTION')

client = MongoClient(mongo_url)
# create db
db = client[mongo_database]
# create collection in db
collection = db[mongo_collection]


if __name__ == '__main__':
    # file_path = 'books_description.json'
    # upload_data(file_path, collection=collection)
    # create_new_book(db=db, collection=collection)
    # select_book(db=db, collection=collection)
    # update_book(db=db, collection=collection)
    delete_book(db=db, collection=collection)
