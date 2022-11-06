import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from blogapp import app, db, bcrypt
from blogapp.models import Users, Posts
from blogapp.forms import RegistrationForm, LoginForm, UpdateAccountForm


@app.route("/")
@app.route("/home")
@login_required
def home():
    posts = Posts.query.all()
    return render_template('home.html', posts=posts)

@app.route("/about")
@login_required
def about():
    var = 'Omar'
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return(redirect(url_for('home')))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print(len(hashed_password))
        user = Users(username=form.username.data.capitalize(), email=form.email.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Welcome {}! Your account has been created'.format(form.username.data), 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form = form)
    
@app.route("/login",  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return(redirect(url_for('home')))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Welcome {}, you have been successfully logged in into your account'.format(form.email.data.split('@')[0]), 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else :
            flash('Please verify your email address and password', 'danger')
    
    return render_template('login.html', title='Login', form = form)

@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return(redirect(url_for('login')))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path + '/static/profile_pics', picture_fn)
    output_format = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_format)
    i.save(picture_path)
    return picture_fn

@app.route("/account",  methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            picture_file = save_picture(form.profile_picture.data)
            current_user.image_file = picture_file
            db.session.commit()
            flash('Your account picture has been updated!', 'success')
        if form.username.data.capitalize() != current_user.username.capitalize() or form.email.data.lower() != current_user.email.lower() or form.profile_picture.data:
            current_user.username=form.username.data.capitalize()
            current_user.email=form.email.data.lower()
            db.session.commit()
            flash('Your account has been updated!', 'success')
        else : flash('No Changes detected!', 'info')
        return redirect(url_for('account'))
    elif request.method =='GET':
        form.username.data=current_user.username.capitalize()
        form.email.data=current_user.email.lower()
    image_file = url_for('static', filename= 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', form=form, image_file = image_file)
