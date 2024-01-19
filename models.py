"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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
class Post(db.Model):
    __tablename__ = "posts"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.text, nullable=False)
    content = db.Column(db.text, nullable=False)
    # server_default=db.func.now() sets a default value of the current timestamp when a new post is created. 
    created_at = db.Column(db.date, server_default=db.func.now())
    user_id = db.ForeignKey(db.Integer, db.ForeignKey('users.id'))
    
    dept = db.relationship('User', backref='posts')
    
    def __repr__(self):
        s = self
        return f"<post id={s.id}, first name={s.first_name}, last name={s.last_name}, photo:{s.image_url}>"

