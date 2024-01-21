"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "users"
    
    def __repr__(self):
        s = self
        return f"<user id={s.id}, first name={s.first_name}, last name={s.last_name}, photo:{s.image_url}>"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(10),
                           nullable=False)
    last_name = db.Column(db.String(10),
                          nullable=False)
    image_url = db.Column(db.String(255), default='default.jpg')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan")
class Post(db.Model):
    __tablename__ = "posts"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # user = db.relationship('User', backref='posts')
    tags = db.relationship('Tag', secondary='posttags', backref='posts')
    
    def __repr__(self):
        s = self
        return f"<post id={s.id}, title={s.title}, content={s.content}, created_at={s.created_at}>"

class Tag(db.Model):
    __tablename__ = "tags"
    
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
class PostTag(db.Model):
    __tablename__ = "posttags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
