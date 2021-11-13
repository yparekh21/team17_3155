from flask import render_template, redirect, url_for, request
import os
import random as random
from models import User as User, Classes as Classes
from __init__ import app
from database import db

# Link: http://127.0.0.1:5000/

@app.route('/Home/<username>')
def index(username):
    queryUser = User.query.filter_by(username = username)
    result = queryUser.first()
    return render_template('AccountHomePage.html',user = result)

@app.route('/Classes/<username>', methods= ['POST','GET'])
def classes(username):
    if request.method == 'POST':
        class_name = request.form['name']

        new_id = random.randint(1000, 9999)
        code = random.randint(100000, 999999)

        queryUser = User.query.filter_by(username = username)
        result = queryUser.first()

        #push to db
        try:
            db.session.add(Classes(new_id, class_name, code, username))
            db.session.commit()

            return redirect(url_for('classes', username = username))
        except:
            return "There was an error setting your class"

    else:
        myclass = User.query.filter_by(username = username).first()


        return render_template('classes.html', user = myclass)

@app.route('/ClassPage/<username>/<id>', methods = ['POST', 'GET'])
def classpage(username,id):

    user_a = User.query.filter_by(username = username).first()
    classes = Classes.query.filter_by(id = id).first()
    return render_template('ClassPage.html', user = user_a, classinfo = classes)

@app.route('/SignUp', methods = ['POST','GET'])
def signup():
    user_id = random.randint(1000000, 99999999)
    if(request.method == "POST"):
        username = request.form['name']
        password = request.form['password']

        db.session.add(User(username = username, password = password ))
        db.session.commit()

        return redirect('/Login')

    else:
        return render_template('SignUpPage.html')
@app.route('/Login', methods = ['POST','GET'])
def login():

    if(request.method == "POST"):
        user = request.form['name']
        password = request.form['password']
        queryPass = db.session.query(User).filter(User.username==user, User.password==password)
        result = queryPass.first()
        if(result):
            return redirect(url_for('index', username = user))
    else:

        return render_template('LoginPage.html')

app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=False)
