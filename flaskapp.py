from flask import Flask, render_template,session,flash
from flask import Flask, render_template, request
from requests import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
import secrets
import bcrypt
import datetime

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


app.secret_key = params["secret_key"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, params["database"])
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
    reset_token = db.Column(db.String(128), unique=True)
    token_expiry = db.Column(db.DateTime)
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

def send_email(to, subject, message):
    print(f"Email sent to {to}: Subject: {subject}\nMessage: {message}")

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        
        if email in User:
            user = user[email]
            token = secrets.token_hex(16)
            user["reset_token"] = token
            user["token_expiry"] = datetime.datetime.now() + datetime.timedelta(hours=1)

            reset_link = f"https://pmmusic.com/reset-password?token={token}"
            send_email(email, "Password Reset Request", f"Click the link to reset your password: {reset_link}")
            
            flash("Password reset request sent. Check your email.")
            return redirect(url_for("login"))
        else:
            flash("If the email exists, we've sent a reset link. Please check your email.")
            return redirect(url_for("forgot_password"))
    return render_template("forgot_password.html")

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    token = request.args.get("token")
    if token:
        user = None
        for email, data in user.items():
            if data["reset_token"] == token and data["token_expiry"] > datetime.datetime.now():
                user = data
                break
        if user:
            if request.method == "POST":
                new_password = request.form.get("new_password")
                hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
                user["password"] = hashed_password
                user["reset_token"] = None
                user["token_expiry"] = None
                
                flash("Password reset successfully. You can now log in with your new password.")
                return redirect(url_for("login"))
            return render_template("reset_password.html")
    flash("Invalid or expired token.")
    return redirect(url_for("login"))


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
        hashed_reset_token = generate_password_hash(password, method='sha256')
        entry = User(Username = username ,Email = email,Password = hashed_password,reset_token=hashed_reset_token,token_expiry=datetime.now(),RegistrationDate=datetime.now())

        db.session.add(entry)
        db.session.commit()

        # Store the user details in the database or perform any desired action

        return redirect(url_for("login"))

    return render_template('signup.html',params=params)




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
