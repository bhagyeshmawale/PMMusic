from flask import Flask, render_template,session,flash
from flask import Flask, render_template, request
from requests import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_mail import Mail
import os
basedir = os.path.abspath(os.path.dirname(__file__))

with open('config.json','r') as c:
    params=json.load(c)["params"]


local_Server = True

app = Flask (__name__)
# server =app.server
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params["gmail-user"] ,
    MAIL_PASSWORD = params["gmail-password"]

    )
#mail = Mail(app)

# if (local_Server):
#     app.config ['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
# else:
#     app.config ['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]

app.secret_key = params["secret_key"]
# app.config ['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mydb.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




db = SQLAlchemy(app)

class Contacts(db.Model):
   sno = db.Column( db.Integer, primary_key = True)
   name = db.Column(db.String(100),nullable=False)
   phone = db.Column(db.String(50),nullable=False)  
   message = db.Column(db.String(200),nullable=False)
   date = db.Column(db.String(12),nullable=False)
   email = db.Column(db.String(20),nullable=False)

class Post(db.Model):
   sno = db.Column( db.Integer, primary_key = True)
   title = db.Column(db.String(500),nullable=False)
   slug = db.Column(db.String(30),nullable=False)  
   content = db.Column(db.String(500),nullable=False)
   tagline = db.Column(db.String(500),nullable=False)
   date = db.Column(db.String(12),nullable=False)
   img_file = db.Column(db.String(20),nullable=False)


class User(db.Model):
    __tablename__ = 'User'

    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Password = db.Column(db.String(100), nullable=False)
    RegistrationDate = db.Column(db.String(12),nullable=False)




class Tutorial(db.Model):
    __tablename__ = 'tutorials'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    difficulty_level = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def __init__(self, title, description, difficulty_level, release_date):
        self.title = title
        self.description = description
        self.difficulty_level = difficulty_level
        self.release_date = release_date



class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    instructor = db.relationship('Instructor', backref=db.backref('courses', lazy=True))

    def __init__(self, name, description, duration, instructor):
        self.name = name
        self.description = description
        self.duration = duration
        self.instructor = instructor



class Instructor(db.Model):
    __tablename__ = 'instructors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(255), nullable=False)
    joining_date = db.Column(db.Date, nullable=False)

    def __init__(self, name, bio, joining_date):
        self.name = name
        self.bio = bio
        self.joining_date = joining_date


@app.route('/')
def home():
    return render_template('home.html',params=params)

@app.route('/about')
def about():
    return render_template('about.html',params=params)

@app.route('/course')
def course():
    return render_template('course.html',params=params)


@app.route('/gallery')
def gallery():
    return render_template('gallery.html',params=params)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')
        entry = User(Username = username ,Email = email,Password = hashed_password,RegistrationDate=datetime.now())

        db.session.add(entry)
        db.session.commit()

        # Store the user details in the database or perform any desired action

        return redirect(url_for("login"))

    return render_template('signup.html',params=params)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(Username=username).first()
        if user and check_password_hash(user.Password, password):
            session['username'] = user.Username
            flash('Login successful!', 'success')
            return redirect('/')
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html',params=params)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


@app.route("/contact",methods = ['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        message = request.form.get('message')
        date = request.form.get('date')
        email = request.form.get('email')

        entry = Contacts(name = name ,phone = phone,message = message,date=datetime.now(),email=email)
        db.session.add(entry)
        db.session.commit()
        #mail.send_message("New Message from " + name,sender = email,
            #recipients = [params['gmail-user']],
            #body = message + "\n" + phone +"\n" + name

            #)


    return  redirect(url_for("home"))




if __name__ == '__main__':
    app.run(debug=False) 