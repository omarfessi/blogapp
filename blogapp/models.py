from datetime import datetime
from blogapp import db 
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