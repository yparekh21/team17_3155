from database import db;
from datetime import datetime;

class User(db.Model):
    __tablename__ = 'user'
    full_name = db.Column("full_name", db.String(100))
    username = db.Column(db.String(20), primary_key = True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column("email", db.String(100))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    classes = db.relationship('Classes', backref = 'user',lazy=True)
    posts = db.relationship('Posts', backref = 'user', lazy = True)

    def __init__(self, full_name, email, username, password):
        self.full_name = full_name
        self.username = username
        self.password = password
        self.email = email

class Classes(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(40),nullable = False)
    classcode = db.Column(db.Integer,nullable = True)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    username = db.Column(db.String, db.ForeignKey('user.username'), nullable = False)
    posts = db.relationship('Posts', backref='classes', lazy=True)
    classusers = db.relationship('ClassUsers', backref = 'classes', lazy = True)
    def __init__(self, id, name, classcode, username):
        self.id = id
        self.name = name
        self.classcode = classcode
        self.username = username

class ClassUsers(db.Model):
    __tablename__ = 'classusers'
    id  = db.Column(db.Integer, primary_key = True)
    classid = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable = False)
    userid = db.Column(db.String, db.ForeignKey('user.username'),nullable = False)

    def __init__(self, id, classid, userid):
        self.id = id
        self.classid = classid
        self.userid = userid


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    post = db.Column(db.String(300), nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    upvote = db.Column(db.Integer, default = 0)
    downvote = db.Column(db.Integer, default = 0)
    ratio = db.Column(db.Numeric, nullable = True)
    classrelation = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    userrelation = db.Column(db.String, db.ForeignKey('user.username'), nullable = False)
    postcomments = db.relationship("Comment", backref="note", cascade="all, delete-orphan", lazy=True)

    def __init__(self, id, title, post,classrelation, userrelation):
        self.id = id
        self.title = title
        self.post = post
        self.classrelation = classrelation
        self.userrelation = userrelation

class ClassPosts(db.Model):
    __tablename__ = 'classposts'
    id  = db.Column(db.Integer, primary_key = True)
    classid = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable = False)
    postid = db.Column(db.Integer, db.ForeignKey('posts.id'),nullable = False)

    def __init__(self, id, classid, postid):
        self.id = id
        self.classid = classid
        self.postid = postid

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    content = db.Column(db.String, nullable=False)
    postrelation = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    userrelation = db.Column(db.Integer, db.ForeignKey("user.username"), nullable=False)

    def __init__(self, id, content, postrelation, userrelation):
        self.id = id
        self.content = content
        self.postrelation = postrelation
        self.userrelation = userrelation
        
class PostComments(db.Model):
    __tablename__ = 'postcomments'
    id = db.Column(db.Integer, primary_key = True)
    commentid = db.Column(db.Integer, db.ForeignKey('comment.id'),nullable = False)
    postid = db.Column(db.Integer, db.ForeignKey('posts.id'),nullable = False)
    
    def __init__(self, id, commentid, postid):
        self.id = id
        self.commentid = commentid
        self.postid = postid
        
