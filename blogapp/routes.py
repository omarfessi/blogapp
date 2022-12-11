import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from blogapp import app, db, bcrypt, mail
from blogapp.models import Users, Posts
from blogapp.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                            CreateNewPostForm, UpdatePostForm, RequestTokenForm, ResetPasswordForm)
from flask_mail import Message

@app.route("/")
@app.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.posted_on.desc()).paginate(page, per_page=2)
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

@app.route("/posts/new",  methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreateNewPostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created !', 'success')
        return redirect(url_for("home"))

    return render_template('create_post.html', form=form, title='New Post')

@app.route("/posts/<int:id>",  methods=['GET', 'POST'])
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/posts/<int:id>/update",  methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Posts.query.get_or_404(id)
    if current_user != post.author :
        abort(403)
        return redirect(url_for("home"))
    else :
        form = UpdatePostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash('Your post has been updated !', 'success')
            return redirect(url_for("post", id=post.id))
        elif request.method =='GET':
            form.title.data=post.title
            form.content.data=post.content
    return render_template('create_post.html', form=form, title='Update Post')

@app.route("/posts/<int:id>/delete",  methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Posts.query.get_or_404(id)
    if current_user != post.author :
        abort(403)
        return redirect(url_for("home"))
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted !', 'success')
    return redirect(url_for("home"))

@app.route("/user/<string:username>")
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = Users.query.filter_by(username=username).first_or_404(description='There is no username that matches {}'.format(username))
    posts = Posts.query.filter_by(author=user)\
            .order_by(Posts.posted_on.desc())\
            .paginate(page, per_page=2)
    return render_template('user_posts.html', posts=posts, user=user)

def send_reset_password_email(user):
    token=user.get_reset_token()
    msg = Message(
        'Password Reset Request',
        sender='noreplay@blogapp.com',
        recipients=[user.email])
    msg.body = f""" To Reset your password visit the following link:
{url_for('reset_password', token=token, _external=True)} 
If you did not make this request, Please ignore this email and nothing will be made."""
    mail.send(msg)
    

@app.route("/forgetpassword",  methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        return(redirect(url_for('home')))
    form = RequestTokenForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        send_reset_password_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return(redirect(url_for('login')))
    return render_template('request_token.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>",  methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return(redirect(url_for('home')))
    user = Users.verify_reset_token(token)
    if user is None : 
        flash('Invalid or expired token, please proceed again', 'warning')
        return(redirect(url_for('request_password_reset')))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('It is done {}! Your password has been updated'.format(user.username), 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)