from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

filepath = os.path.abspath(os.getcwd())+"/database.db" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+filepath
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

