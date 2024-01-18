from unittest import TestCase
from app import app, db
from models import User
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
        self.app.config['SQLALCHEMY_ECHO'] = True
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
            db.session.add(user)
            db.session.commit()
            self.assertEqual(user.full_name, "John Doe")
            self.assertEqual(user.image_url, "somethingurl.jpg")

    def test_userdefault(self):
        with self.app.app_context():
            user = User(first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()
            self.assertEqual(user.full_name, "John Doe")
            self.assertEqual(user.image_url, "default.jpg")

if __name__ == "__main__":
    import unittest
    unittest.main()
