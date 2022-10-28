from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '760be9e130b66f380a1d4430d42c91fa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/adages' #conString = "postgres://YourUserName:YourPassword@YourHostname:5432/YourDatabaseName";
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from blogapp import routes

