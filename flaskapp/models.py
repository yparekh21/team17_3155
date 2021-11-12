from flaskapp import db;
from datetime import datetime;

class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(20), primary_key = True)
    password = db.Column(db.String(30), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    classes = db.relationship('Classes', backref = 'user',lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Classes(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(40),nullable = False)
    classcode = db.Column(db.Integer,nullable = True)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    username = db.Column(db.String, db.ForeignKey('user.username'), nullable = False)
    def __init__(self, id, name, classcode, username):
        self.id = id
        self.name = name
        self.classcode = classcode
        self.username = username