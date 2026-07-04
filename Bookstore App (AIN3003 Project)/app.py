import os
import certifi
from dotenv import load_dotenv
from flask import Flask, redirect, request, jsonify
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from bson import ObjectId

load_dotenv()
connection_string = os.getenv("COSMOS_DB_CONNECTION")

client = MongoClient(connection_string, tls=True, tlsCAFile=certifi.where())
database: Database = client.get_database("bookstore")
collection: Collection = database.get_collection("books")

app = Flask(__name__)

@app.route('/')
def main():
    return "Welcome to the Burak Demirci's Bookstore!"

@app.route('/books', methods=['GET'])
def redirect_to_list():
    return (redirect(f'/books/list'))

@app.route('/books/list', methods=['GET'])
def get_books():
    books = list(collection.find())
    for book in books:
        book['_id'] = str(book['_id'])
    return jsonify(books), 200

@app.route('/books/find.isbn/<book_isbn>', methods=['GET'])
def get_book(book_isbn):
    book = collection.find_one({'isbn': book_isbn})
    if book:
        book['_id'] = str(book['_id'])
        return jsonify(book), 200
    else:
        return jsonify({'error': 'Book not found'}), 404
    
@app.route("/books/delete.isbn/<book_isbn>", methods=['DELETE'])
def remove_book(book_isbn):
    result = collection.delete_one({'isbn': book_isbn})

    if result.deleted_count:
        return jsonify({'message': 'Book deleted successfully.'}), 200
    else:
        return jsonify({'error': 'Book not found'}), 404
    
@app.route('/books/add', methods=['POST'])
def add_book():
    data = request.get_json()
    required_fields = ['title', 'author', 'isbn', 'year', 'page', 'price', 'category']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    if collection.find_one({'isbn': data['isbn']}):
        return jsonify({'error': 'A book with this ISBN already exists.'}), 400

    new_book = {
        'title': data['title'],
        'author': data['author'],
        'isbn': data['isbn'],
        'year': data['year'],
        'page': data['page'],
        'price': data['price'],
        'category': data['category']
    }
    result = collection.insert_one(new_book)
    new_book['_id'] = str(result.inserted_id)
    return jsonify(new_book), 201

@app.route('/books/update.isbn/<book_isbn>', methods=['PUT'])
def update_book(book_isbn):
    data = request.get_json()
    update_fields = {key: value for key, value in data.items() if key in ['title', 'author', 'year', 'page', 'price', 'category']}  
    
    if not update_fields:
        return jsonify({'error': 'No valid fields to update.'}), 400

    result = collection.update_one({'isbn': book_isbn}, {'$set': update_fields})

    if result.matched_count:
        updated_book = collection.find_one({'isbn': book_isbn})
        updated_book['_id'] = str(updated_book['_id'])
        return jsonify(updated_book), 200
    else:
        return jsonify({'error': 'Book not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)