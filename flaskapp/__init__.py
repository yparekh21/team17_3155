from flask import Flask
from database import db

app = Flask(__name__)     # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ProjectDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db.init_app(app)

from models import User as User
from models import Classes as Classes

with app.app_context():
    db.create_all()

import routes

