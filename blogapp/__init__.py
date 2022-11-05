from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '760be9e130b66f380a1d4430d42c91fa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/blogapp' #conString = "postgres://YourUserName:YourPassword@YourHostname:5432/YourDatabaseName";
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
#in order for the LoginManager extention to know where a user login we need to specify it here
login_manager.login_view = 'login'
login_manager.login_message='Please log in first'
login_manager.login_message_category='info'

from blogapp import routes


