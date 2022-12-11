from datetime import datetime
from blogapp import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    __tablename__ = 'blog_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=True)
    email = db.Column(db.String(120),unique=True, nullable=True)
    image_file = db.Column(db.String(20), nullable=True, default = 'default.jpg')
    password = db.Column(db.String(60), nullable=True)
    posts = db.relationship('Posts', backref='author', lazy=True)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}','{self.password}')"

    def get_reset_token(self, expires=1800):
        s = Serializer(app.config['SECRET_KEY'], expires)
        token = s.dumps({'user_id': self.id}).decode('utf-8')
        return token
         
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except : 
            return None
        return Users.query.get(user_id)

class Posts(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=True)
    posted_on = db.Column(db.DateTime, nullable = False, default= datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_users.id'), nullable = False)
    def __repr__(self) -> str:
        return f"User('{self.title}', '{self.posted_on}','{self.content}')"