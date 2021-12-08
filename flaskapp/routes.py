from datetime import datetime

from flask import render_template, redirect, url_for, request
import os
import random as random

from sqlalchemy import desc

from models import PostComments as PostComments, User as User, Classes as Classes, Posts as Posts, ClassUsers as ClassUsers, ClassPosts as ClassPosts, Comment as Comment, PostUsers as PostUsers

from __init__ import app
from database import db
from forms import RegisterForm, LoginForm, CommentForm
from flask import session
import bcrypt


@app.route('/')
@app.route('/Home', methods= ['POST','GET'])
def index():
    # check if a user is saved in session
    if session.get('user'):
        list = []
        postlist = []
        popList = []
        allPopPost = []
        allPost = []
        queryUser = User.query.filter_by(full_name = session.get('user')).first()

        username = queryUser.username
        try:
            queryClassUser = (ClassUsers).query.join(User).filter_by(username = username).all()
            #print(queryClassUser)

            for myclass in queryClassUser:

                returnList = db.session.query(Classes).filter_by(id=myclass.classid).first()
                returnThis = returnList.id

                list.append(returnList)
                posts = db.session.query(Posts).filter_by(classrelation=myclass.classid).order_by(desc(Posts.date)).all()
                popularposts = db.session.query(Posts).filter_by(classrelation = myclass.classid).order_by(Posts.ratio).all()
                postlist.append(posts)
                popList.append(popularposts)


            print(popList)
            for post in postlist:
                for item in post:
                    allPost.append(item)

            for posts in popList:
                for items in posts:
                    if(items.downvote > 0):
                        allPopPost.append(items)
            print(allPost)


            #print(allPopPost)
            allPost.sort(key = lambda x: x.date, reverse = True)
            allPopPost.sort(key = lambda x: x.ratio, reverse = True)




            return render_template("AccountHomePage.html", user=queryUser,  posts = allPost, classinfo = list, latestclass = list, popularposts = allPopPost)
        except:
            return render_template("AccountHomePage.html", user=queryUser)

    else:
        return redirect(url_for('login'))
@app.route('/delete/<postid>', methods = ['POST', 'GET'])
def deletepost(postid):

    if(session.get('user')):
        mypost = db.session.query(Posts).filter_by(id = postid).first()
        classes = db.session.query(ClassPosts).filter_by(postid = postid).first()
        classId = classes.classid

        db.session.delete(mypost)
        db.session.commit()

        return redirect(url_for('classpost', id = classId))

    else:
        redirect(url_for('login'))

@app.route('/upvote/<postid>', methods= ['POST','GET'])
def upvote(postid):
    if(session.get('user')):

            mypost = db.session.query(Posts).filter_by(id=postid).first()
            classes = db.session.query(ClassPosts).filter_by(postid = postid).first()
            classId = classes.classid
            upvote = mypost.upvote
            downvote = mypost.downvote
            print(upvote)
            newupvote = upvote + 1
            print(newupvote)
            mypost.upvote = newupvote

            if(downvote > 0):

                newratio = newupvote/downvote
                mypost.ratio = newratio
            db.session.add(mypost)
            db.session.commit()
            print(mypost)
            return redirect(url_for('classpage', id = classId))
    else:
        return redirect(url_for('login'))
@app.route('/downvote/<postid>', methods=['POST', 'GET'])
def downvote(postid):
    if(session.get('user')):
        mypost = db.session.query(Posts).filter_by(id=postid).first()
        classes = db.session.query(ClassPosts).filter_by(postid=postid).first()
        classId = classes.classid
        downvote = mypost.downvote
        upvote = mypost.upvote
        print(downvote)
        newdownvote = downvote + 1
        print(newdownvote)
        mypost.downvote = newdownvote
        if(newdownvote > 0):
            newratio = upvote / newdownvote
            mypost.ratio = newratio
        db.session.add(mypost)
        db.session.commit()
        print(mypost)
        return redirect(url_for('classpage', id = classId))
    else:
        return redirect(url_for('login'))

@app.route('/Classes', methods= ['POST','GET'])
def classes():
    if session.get('user'):
        if request.method == 'POST':
            class_name = request.form['name']

            new_id = random.randint(1000, 9999)
            code = random.randint(100000, 999999)
            username = session.get('user')

            queryUser = User.query.filter_by(full_name = username).first()
            result = queryUser.username
            classusersid = random.randint(0,10000)

            #push to db
            try:

                db.session.add(Classes(new_id, class_name, code, result))
                db.session.commit()
                print('got here')
                print(new_id)
                classid = db.session.query(Classes).filter_by(id=new_id).first()
                print('class id below')
                print(classid.id)

                db.session.add(ClassUsers(classusersid, classid.id, result))
                db.session.commit()



                return redirect(url_for('classes'))
            except:
                return "There was an error setting your class"

        else:
            username = session.get('user')
            queryUser = User.query.filter_by(full_name = username).first()

            #print(username)
            user = User.query.filter_by(full_name = username).first()
            #print(user.classes)
            queryClassUser = (ClassUsers).query.join(User).filter_by(username=user.username).all()
            #print(queryClassUser)
            try:
                list = []
                for myclass in queryClassUser:

                    returnList = Classes.query.filter_by(id=myclass.classid).first()
                    returnThis = returnList.id
                    list.append(returnList)



                return render_template('classes.html', user = user, classes = list)
            except:
                return render_template('classes.html', user = user)
    else:
        return redirect(url_for('login'))

@app.route('/ClassPage/<id>/post', methods= ['POST','GET'])
def post(id):
    if session.get('user'):
        if request.method == 'POST':
            title = request.form['title']
            post = request.form['post']
            postid = random.randint(10000, 99999)
            postusersid = random.randint(10000,99999)
            classIn = db.session.query(Classes).filter_by(id = id).first()
            classId = classIn.id
            username = session.get('user')
            user = db.session.query(User).filter_by(full_name = username).first()
            userName = user.username
            classpostsid = random.randint(0, 10000)
            #push to db
            try:
                db.session.add(Posts(postid, title, post, classId, userName))
                db.session.commit()

                print('class id below')

                db.session.add(ClassPosts(classpostsid, classId, postid))
                db.session.add(PostUsers(postusersid, postid, userName))
                db.session.commit()

                return redirect(url_for('index'))
            except:

                postsOut = db.session.query(Posts).all()
                #print(classId)
               # print(classIn)
               # print(userName)
               # print(user)
               # print(postsOut)
                return "There was an error posting your post"

        else:
            user_a = User.query.filter_by(full_name=session.get('user')).first()

            classes = Classes.query.filter_by(id=id).first()
            return render_template('post.html', user = user_a, classinfo = classes)
    else:
        return redirect(url_for('login'))



@app.route('/ClassPage/<id>/<post_id>/edit/', methods = ['POST','GET'])
def editpost(id, post_id):
    if session.get('user'):
        if(request.method == 'POST'):
            title = request.form['title']
            post = request.form['post']

            _post = db.session.query(Posts).filter_by(id=post_id).first()

            _post.title = title
            _post.post = post

            db.session.add(_post)
            db.session.commit()
            return redirect(url_for('classpage', id = id))

        else:
            user_a = User.query.filter_by(full_name=session.get('user')).first()
            _posts = db.session.query(Posts).filter_by(id = post_id).first()
            classes = Classes.query.filter_by(id=id).first()
            return render_template('post.html', posts = _posts, user = user_a, classinfo = classes)
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))

@app.route('/Classes/join', methods = ['POST','GET'])
def classesJoin():
    if session.get('user'):
        if request.method == 'POST':

            codeIn = request.form['code']

            classIn = db.session.query(Classes).filter_by(classcode=codeIn).first()
            classId = classIn.id
            classusersid = random.randint(0, 10000)
            user = db.session.query(User).filter_by(full_name=session.get('user')).first()
            username = user.username

            #push to db
            try:

                db.session.add(ClassUsers(classusersid, classId, username))
                db.session.commit()
               # print(ClassUsers.query.filter_by(classid = classId).first())
               # print(user)
               # print(username)
                return redirect(url_for('classes'))
            except:
                return "There was an error setting your class"

        else:
            userIn = session.get('user')

          #  print(userIn)
            myclass = User.query.filter_by(full_name=userIn).first()
          #  print(ClassUsers.query.all())
           # printout = ClassUsers.query.filter_by(id = 871).first()

            return render_template('join.html', user = myclass)
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))

@app.route('/ClassPage/<id>', methods = ['POST', 'GET'])
def classpage(id):
    if session.get('user'):
        user_a = db.session.query(User).filter_by(full_name = session.get('user')).first()
        classes = Classes.query.filter_by(id = id).first()

        queryClassPosts = (ClassPosts).query.join(Classes).filter_by(id = classes.id).all()

        try:
            latestposts = db.session.query(Posts).filter_by(classrelation=id).order_by(desc(Posts.date)).limit(7)
            popularvotes = Posts.query.filter_by(classrelation = id).order_by(desc(Posts.ratio)).limit(7)


            for post in latestposts:
                mypost = db.session.query(Posts).filter_by(id=post.id).first()

                newdate = mypost.date.strftime("%m/%d/%Y %H:%M")
                post.convertdate = newdate
                db.session.add(mypost)
                db.session.commit()
                queryPostUser = (PostUsers).query.join(Posts).filter_by(id=mypost.id).first()

                queryUser = db.session.query(User).filter_by(username=queryPostUser.userid).first()

                mypost.user = queryUser.username
                db.session.add(mypost)
                db.session.commit()
            for thispost in popularvotes:
                currpost = db.session.query(Posts).filter_by(id=thispost.id).first()
                newdate = currpost.date.strftime("%m/%d/%Y %H:%M")
                print(newdate)
                currpost.convertdate = newdate
                db.session.add(currpost)
                db.session.commit()
                queryPostUser = (PostUsers).query.join(Posts).filter_by(id=currpost.id).first()

                queryUser = db.session.query(User).filter_by(username=queryPostUser.userid).first()

                currpost.user = queryUser.username
                db.session.add(currpost)
                db.session.commit()

            return render_template('ClassPage.html', user=user_a, posts=latestposts, classinfo=classes,
                                   popularposts=popularvotes, postuser=queryPostUser.userid)
        except:
            return render_template('ClassPage.html', user=user_a, posts=latestposts, classinfo=classes,popularposts=popularvotes)


    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))
@app.route('/ClassPage/<id>/ClassForum', methods = ['POST', 'GET'])
def classpost(id):
    if session.get('user'):
        user_a = db.session.query(User).filter_by(full_name = session.get('user')).first()
        classes = db.session.query(Classes).filter_by(id = id).first()

        posts = db.session.query(Posts).filter_by(classrelation = classes.id).all()
        return render_template('classposts.html', user = user_a, classinfo = classes, classposts = posts)
    else:
        # user is not in session redirect to
        return redirect(url_for('login'))
@app.route('/ClassPage/<id>/<topicname>')
def topics(id, topicname):
        redirect(url_for('login'))
@app.route('/signup', methods = ['POST','GET'])
def signup():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        full_name = request.form['full_name']
        # get entered email data
        user_email = request.form['email']
        # get entered username data
        user_username = request.form['username']
        # create user model
        new_user = User(full_name, user_email, user_username, h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = full_name
        # show user dashboard view
        return redirect(url_for('index'))

    # something went wrong - display register view
    return render_template('SignUpPage.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = User.query.filter_by(username=request.form['username']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.full_name
            # render view
            return redirect(url_for('index'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("LoginPage.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("LoginPage.html", form=login_form)

@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('login'))

@app.route('/ClassPage/post/<postid>', methods = ['POST','GET'])
def get_post(postid):
     # check if a user is saved in session
    if session.get('user'):
        # retrieve post form database
        my_post = db.session.query(Posts).filter_by(id=postid).first()
        queryClassInfo = ClassPosts.query.filter_by(postid = my_post.id).first()
        classinfo = db.session.query(Classes).filter_by(id = queryClassInfo.classid).first()
        print(classinfo)
        comments = db.session.query(Comment).filter_by(postrelation = postid).all()
        # create a comment form object
        print(comments)
        form = CommentForm()

        return render_template('EditPost.html', classinfo = classinfo, post=my_post, comments = comments, form=form, user=session.get('user'))
    else:
        return redirect(url_for('login'))



@app.route('/ClassPage/post/<postid>/comment', methods=['POST'])
def new_comment(postid):
    if session.get('user'):
        new_id = random.randint(1000, 9999)
        PostComID = random.randint(1000, 9999)
        comment_form = CommentForm()
        user = db.session.query(User).filter_by(full_name = session.get('user')).first()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            new_record = Comment(new_id, comment_text, postid, user.username)
            db.session.add(new_record)
            db.session.commit()

            db.session.add(PostComments(PostComID, new_id, postid))
            db.session.commit()

        return redirect(url_for('get_post', postid=postid))

    else:
        return redirect(url_for('login'))

app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=False)
