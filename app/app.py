from flask import Flask, request, jsonify, Response

from settings import *

books = [
	{
		'name': 'Matilda',
		'price': 15000,
		'isbn': 9780142410370
	},
	{
		'name': 'Maus',
		'price': 48000,
		'isbn': 9780141014081
	}
	]

@app.route('/')
def hello_world():
	return 'Hello world'


@app.route('/books')
def get_books():
	return jsonify({'books': books})

def validBookObject(bookObject):
	if  ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
		return True
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
		books.insert(0, new_book)
		return "True"
	else:
		return "False"

@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
	request_data = request.get_json()
	new_book = {
		'name' : request_data['name'],
		'price' : request_data['price'],
		'isbn' : isbn
	}
	i = 0
	for book in books:
		currentIsbn = book['isbn']
		if currentIsbn == isbn:
			books[i] = new_book
		i += 1
	response = Response("", status=204)
	return response

@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
	request_data = request.get_json()
	updated_book = {}
	if ("name" in request_data):
		updated_book['name'] = request_data["name"]
	if "price" in request_data:
 		updated_book["price"] = request_data["price"]
	for book in books:
		if book["isbn"] == isbn:
   			book.update(updated_book)
	response = Response("", status=204)
	response.headers['Location'] = "/books/" + str(isbn)
	return response

@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
	i = 0
	for book in books:
		if book["isbn"] == isbn:
			books.pop(i)
			response = Response("", status=204)
			return response
		i += 1
	invalidBookObjectError = {"error": "This ISBN doesn't match with any book"}
	response = Response(invalidBookObjectError, status=404, mimetype='application/json')
	return response 
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
	response = {}
	for book in books:
		if book["isbn"] == isbn:
			response["name"] = book["name"]
			response["price"] = book["price"]
	return jsonify(response)


app.run(host="0.0.0.0", port=5000)
