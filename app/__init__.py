from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

db_host = os.environ.get('DB_HOST')
db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')


app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_username}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

from app import routes