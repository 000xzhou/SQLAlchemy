from unittest import TestCase
from app import app, db
from models import User,Tag,Post
from dotenv import load_dotenv
load_dotenv()
import os

class UserFlaskCase(TestCase):
    """Test for User Cases"""
    @classmethod
    def setUpClass(cls):
        """Set up Flask application context and configuration."""
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        cls.app.config['SQLALCHEMY_ECHO'] = False
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.drop_all()
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up class-level resources."""
        pass

    def setUp(self):
        """Add sample"""
        with self.app.app_context():
            User.query.delete()
            # Add a sample user
            user = User(first_name="John", last_name="Doe", image_url="image_url.jpg")
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id

    def tearDown(self):
        """Clean up instance-level resources."""
        with self.app.app_context():
            User.query.delete()
            db.session.rollback()
        
    # check to seee if homepage loaded with no errors
    def test_homepage(self):
        with self.app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 200)
    
    # test to see if user is display
    def test_user_list(self):
        with self.app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("John Doe", html)

    # test to see user is display after submiting it though the form 
    def test_user_form_submit(self):
        with self.app.test_client() as client:
            resp = client.post("/users/new", data={"fname": "Lucky", "lname": "Star"}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Lucky Star", html)
            
    # testing to see user info
    def test_user_detail_page(self):
        with self.app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("John Doe", html)            
            self.assertIn("image_url.jpg", html)            
            
    # editing user test plus follow up!
    def test_user_edit_page(self):
        with self.app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/edit", data={"fname": "Lucky", "lname": "Star"}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotEqual("John Doe", html)
            self.assertIn("Lucky Star", html) 
            
    # deleting user test plus follow up!
    def test_user_edit_page(self):
        with self.app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotEqual("John Doe", html)
class PostFlaskCase(TestCase):
    """Test for Post Cases"""
    @classmethod
    def setUpClass(cls):
        """Set up Flask application context and configuration."""
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        cls.app.config['SQLALCHEMY_ECHO'] = True
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.drop_all()
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up class-level resources."""
        pass

    def setUp(self):
        """Add sample"""
        with self.app.app_context():
            Post.query.delete()
            User.query.delete()
            # Add a sample user
            user = User(first_name="John", last_name="Doe", image_url="image_url.jpg")
            db.session.add(user)
            db.session.commit()
            post = Post(title= "Lucky Star", content= "Little Star")
            db.session.add(post)
            db.session.commit()
            self.user_id = user.id
            self.post_id = post.id

    def tearDown(self):
        """Clean up instance-level resources."""
        with self.app.app_context():
            Post.query.delete()
            User.query.delete()
            db.session.rollback()
    
    # test new post form 
    def test_post_form_submit(self):
        with self.app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/posts/new", data={"title": "Another", "content": "Star"}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Another", html)
            
    def test_post_detail_page(self):
        with self.app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Lucky Star", html) 
            
    def test_post_edit_page(self):
        with self.app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/posts/new", data={"title": "Another", "content": "Star"}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Another", html)
            
    def test_post_delete(self):
        with self.app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
class TagFlaskCase(TestCase):
    """Test for Tag Cases"""
    
    
    
if __name__ == "__main__":
    import unittest
    unittest.main()
