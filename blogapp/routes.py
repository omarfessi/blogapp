from flask import render_template, url_for, flash, redirect
from blogapp import app
from blogapp.models import Users, Posts
from blogapp.forms import RegistrationForm, LoginForm

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

