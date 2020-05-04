from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json 
from settings import app

db = SQLAlchemy(app)

class Book(db.Model):
	__tablename__ = 'books'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	price = db.Column(db.Float)
	isbn = db.Column(db.Integer)

	def json(self):
		return {'name': self.name, 'price': self.price, 'isbn': self.isbn}

	def __repr__(self):
		return self.__str__()

	def get_all_books():
		return [Book.json(book) for book in Book.query.all()]
	
		
	def get_book_by_isbn(_isbn):
		return Book.query.filter_by(isbn=_isbn).first_or_404(description="There's no book which matches at {} ISBN".format(_isbn))
	
	def add_book(dictio):
		new_book = Book(name=dictio['name'], price=dictio['price'], isbn=dictio['isbn'])
		db.session.add(new_book)
		db.session.commit()
	
	def update_a_book(isbn, request_data):
		book = Book.query.filter_by(isbn=isbn).first_or_404(description="There's no match for {} ISBN".format(isbn))
		if "price" in request_data:
			book.__setattr__("price", request_data["price"])
		if "name" in request_data:
			book.__setattr("name", request_data["name"])
		db.session.commit()		

	
	def replace_a_book(isbn, request_data):
		book = Book.query.filter_by(isbn=isbn).first_or_404(description="There is no book which matches as {} ISBN".format(isbn))
		book.__setattr__("name", request_data['name'])
		book.__setattr__("price", request_data['price'])
		book.__setattr__("isbn", isbn)
		db.session.commit()

	def delete_book(isbn):
		book = Book.query.filter_by(isbn=isbn).first_or_404(description="There's no match with {} ISBN".format(isbn))
		if book is True:
			db.session.delete(book)
			db.session.commit()
			return True
		else:
			return False

	def __str__(self):
		book_object = {
			'name': self.name,
			'price': self.price,
			'isbn': self.isbn
			}
		return '{}'.format(book_object)
