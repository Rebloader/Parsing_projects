import json


def upload_data(file_path_in, collection):
    try:
        with open(file_path_in, 'r') as f:
            data = json.load(f)
        collection.insert_many(data)
        print('Data Inserted')
    except FileNotFoundError:
        print('Data Insertion Failed')


def create_new_book(db, collection):
    book = {
        "title": "Assassin's creed",
        "price": "£116",
        "available": 11.0
    }
    try:
        collection.insert_one(book)
        print('Book Inserted')
    except Exception as e:
        print(f'Error with inserted{e}')


def select_book(db, collection):
    # query = {'available': 15.0}
    query = {'available': {'$gte': 1, '$lte': 2}}
    # query = {'title': {'$gte': "A", '$lte': "D"}}
    # query = {'title': {'$regex': '[Bb]atman'}}
    projection = {'_id': 0, 'title': 1, 'price': 1}
    item = collection.find(query, projection)
    i = 0
    for book in item:
        print(book)
        i += 1
    print(f'Total: {i} books')


def update_book(db, collection):
    query = {'available': {'$gte': 1, '$lte': 2}}
    try:
        collection.update_many(query, {'$set': {'available': 0}})
        print('Book Updated')
    except Exception as e:
        print(f'Error with inserted{e}')


def delete_book(db, collection):
    query = {'available': 0}
    collection.delete_many(query)
