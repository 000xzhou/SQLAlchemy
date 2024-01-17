"""Blogly application."""

from flask import Flask, render_template, redirect, request, url_for, flash
from models import db, connect_db, User
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)
secret_key = os.environ.get('SECRET_KEY')
database_uri = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = secret_key

connect_db(app)
# Use app.app_context() to create an application context
with app.app_context():
    db.create_all()

# **GET */ :*** Redirect to list of users. (We’ll fix this in a later step).
@app.route('/')
def redirect_to_users():
    # Redirect to the 'users' endpoint
    return redirect(url_for('list_users'))

# **GET */users :*** Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form.
@app.route('/users')
def list_users():
    # users = User.query.all()
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user_list.html', users = users)

@app.route('/users/new', methods=['GET', 'POST'])
def add_new_user():
    # **POST */users/new :*** Process the add form, adding a new user and going back to ***/users***
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        image_url = request.form.get('image_url')
        # set default if image is left blank 
        if not image_url:
            image_url = 'default.jpg'
        # add to database
        add_new_user = User(first_name=fname, last_name=lname, image_url=image_url)
        db.session.add(add_new_user)
        db.session.commit()
        # Redirect to the list of users
        return redirect(url_for('list_users'))
    # **GET */users/new :*** Show an add form for users
    return render_template('new_user_form.html')
    
# **GET */users/[user-id] :***Show information about the given user. Have a button to get to their edit page, and to delete the user.
@app.route('/users/<user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_detail_page.html', user = user)

# **GET */users/[user-id]/edit :*** Show the edit page for a user. Have a cancel button that returns to the detail page for a user, and a save button that updates the user.
@app.route('/users/<user_id>/edit', methods=['GET', 'POST'])
def user_edit(user_id):
    # check if user exist 
    user = User.query.get_or_404(user_id)
    
    # **POST */users/[user-id]/edit :***Process the edit form, returning the user to the ***/users*** page.
    if request.method == 'POST':
        # user = User.query.get_or_404(user_id)
        if user:
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            image_url = request.form.get('image_url')

        # update user info 
            user.first_name = fname
            user.last_name = lname
            user.image_url = image_url
            
            db.session.commit()

            flash('User updated successfully', 'success')
            return redirect(url_for('user_detail', user_id=user_id))
        else:
            flash('User not found', 'error')
            return redirect(url_for('list_users'))
    return render_template('user_edit.page.html', user = user)

# **POST */users/[user-id]/delete :*** Delete the user.
@app.route('/users/<user_id>/delete')
def user_delete(user_id):
    user = User.query.get(user_id)
    # if user found 
    if(user):
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully', 'success')
    else:
        flash('User not found', 'error')
    return redirect(url_for('list_users'))


if __name__ == '__main__':
    app.run(debug=True)