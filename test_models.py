from unittest import TestCase
from app import app, db
from models import User,Tag,Post
from dotenv import load_dotenv
load_dotenv()
import os

class UserModelCase(TestCase):
    """Test for User Cases"""
    def setUp(self):
        """Set up a Flask application context and create a clean state."""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        self.app.config['SQLALCHEMY_ECHO'] = False
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """Clean up."""
        with self.app.app_context():
            db.session.rollback()

    def test_userinfo(self):
        with self.app.app_context():
            user = User(first_name="John", last_name="Doe", image_url="somethingurl.jpg")
            self.assertEqual(user.full_name, "John Doe")
            self.assertEqual(user.image_url, "somethingurl.jpg")

    def test_userdefault(self):
        with self.app.app_context():
            user = User(first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()
            self.assertEqual(user.full_name, "John Doe")
            self.assertEqual(user.image_url, "default.jpg")
            db.session.delete(user)
            db.session.commit()
            
class PostModelCase(TestCase):
    """Test for Post Cases"""
    def setUp(self):
        """Set up a Flask application context and create a clean state."""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        self.app.config['SQLALCHEMY_ECHO'] = False
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            User.query.delete()
            Post.query.delete()
            # Add a sample user
            user = User(first_name="John", last_name="Doe", image_url="image_url.jpg")
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id

    def tearDown(self):
        """Clean up."""
        with self.app.app_context():
            db.session.rollback()

    def test_postinfo(self):
        with self.app.app_context():
            post = Post(title="title", content="some content", user_id=self.user_id)
            self.assertEqual(post.title, "title")
            self.assertEqual(post.content, "some content")

class TagModelCase(TestCase):
    """Test for Tag Cases"""
    def setUp(self):
        """Set up a Flask application context and create a clean state."""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        self.app.config['SQLALCHEMY_ECHO'] = False
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """Clean up."""
        with self.app.app_context():
            db.session.rollback()    
    
    def test_taginfo(self):
        with self.app.app_context():
            tag = Tag(name="pikachu")
            self.assertEqual(tag.name, "pikachu")
    
    
if __name__ == "__main__":
    import unittest
    unittest.main()
