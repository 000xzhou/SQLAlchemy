"""Models for Blogly."""
# - ***id***, an autoincrementing integer number that is the primary key
# - ***first_name*** and ***last_name***    -require
# - ***image_url*** for profile images      -defaults photo
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
class Blogly(db.Model):
    __tablename__ = "Bloglys"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Colum(db.String(10),
                          nullable=False)
    last_name = db.Colum(db.String(10),
                          nullable=False)
    # https://images.pexels.com/photos/69932/tabby-cat-close-up-portrait-69932.jpeg?cs=srgb&dl=pexels-pixabay-69932.jpg&fm=jpg
    image_url = db.Colum(db.String(255), default='default.jpg')
