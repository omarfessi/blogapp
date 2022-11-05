from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from blogapp.models import Users
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=8)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f'The following username : {username.data} is already taken. Please choose another one')
    
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'The following email address : {email.data} is already taken. Please choose another one')
   


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(f'The following email address : {email.data} does not exist. Please log in with a valid one or register for a new account')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=8)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Confirm changes')

    def validate_username(self, username):
        if current_user.username != username.data:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(f'The following username : {username.data} is already taken. Please choose another one')
        
    def validate_email(self, email):
        if current_user.email != email.data:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(f'The following email address : {email.data} is already taken. Please choose another one')
    