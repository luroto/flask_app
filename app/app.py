from flask import Flask, request, jsonify, Response
from BookModels import *
from settings import *


@app.route('/')
def hello_world():
	return 'Hello world'


@app.route('/books')
def get_all_books():
	return jsonify({'books': Book.get_all_books()})

def validBookObject(bookObject):
	if  ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
		if type(bookObject["name"]) is str and type(bookObject["price"]) is int and type(bookObject["isbn"]) is int:
			return True
		else:
		 	return False
	else:
	 	return False

@app.route('/books', methods=['POST'])
def add_book():
	request_data = request.get_json()
	if (validBookObject(request_data)):
		new_book = {
			"name": request_data["name"],
			"price": request_data["price"],
			"isbn" : request_data["isbn"]
		}
		Book.add_book(new_book)
		return "True"
	else:
		return "False"

@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
	request_data = request.get_json()
	if validBookObject(request_data):
		Book.replace_a_book(isbn, request_data)
		response = Response("", status=204)
	else:
		err = {'Error': 'Requests for update books requires name, price and isbn fields'}
		response = Response(jsonify(err), status=204)
	return response
		
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
	request_data = request.get_json()
	if "price" or "name" in request_data:
		Book.update_a_book(isbn, request_data)
		response = Response("", status=204)
		response.headers['Location'] = "/books/" + str(isbn)
		return response

@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
	mono = Book.delete_book(isbn)
	if mono is True:
		response = Response("", status=204)
		return response
	else:
		invalidBookObjectError = {"error": "This ISBN doesn't match with any book"}
		response = Response(invalidBookObjectError, status=404, mimetype='application/json')
		return response 

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
	response = Book.get_book_by_isbn(isbn)
	print(type(response))
	return jsonify(response.json()) 


app.run(host="0.0.0.0", port=5000)
