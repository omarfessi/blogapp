from crypt import methods
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# you need the secret key to protect your app from crsf attacks when using forms.
app.config['SECRET_KEY'] = '760be9e130b66f380a1d4430d42c91fa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/adages' #conString = "postgres://YourUserName:YourPassword@YourHostname:5432/YourDatabaseName";
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #conString = "postgres://YourUserName:YourPassword@YourHostname:5432/YourDatabaseName";

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# posts = [
#     {
#         'author' : 'Donatello', 
#         'title' : 'I am the brain =)', 
#         'content' : 'Purle is my favorite color', 
#         'date_posted' : '12 April 1994'

#     },

#         {
#         'author' : 'Leanardo', 
#         'title' : 'Hey Captain!', 
#         'content' : 'I love my brothers', 
#         'date_posted' : '13 July 1995'

#     }
# ]

class Users(db.Model):
    __tablename__ = 'blog_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=True)
    email = db.Column(db.String(120),unique=True, nullable=True)
    image_file = db.Column(db.String(20), nullable=True, default = 'default.jpg')
    password = db.Column(db.String(60), nullable=True)
    posts = db.relationship('Posts', backref='author', lazy=True)
    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}','{self.password}')"

class Posts(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=True)
    posted_on = db.Column(db.DateTime, nullable = False, default= datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_users.id'), nullable = False)
    def __repr__(self) -> str:
        return f"User('{self.title}', '{self.posted_on}','{self.content}')"

@app.route("/")
@app.route("/home")
def home():
    posts = Posts.query.all()
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    var = 'Omar'
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Welcome {}! Your account has been created'.format(form.username.data), 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form = form)
    
@app.route("/login",  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'omarfessy@gmail.com' and form.password.data =='password':
            flash('Welcome {}, you have been successfully logged in into your account'.format(form.email.data.split('@')[0]), 'success')
            return redirect(url_for('home'))
        else :
            flash('Please verify your email address and password', 'danger')
    
    return render_template('login.html', title='Login', form = form)


# if __name__ == '__main__':
#     app.run(debug=True) 