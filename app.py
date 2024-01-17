"""Blogly application."""

from flask import Flask, render_template, redirect, request, url_for, flash
from models import db, connect_db, User

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://xiang:password@localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

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
    users = User.query.all()
    print(users)
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
    return render_template('user_detail_page.html')

# **GET */users/[user-id]/edit :*** Show the edit page for a user. Have a cancel button that returns to the detail page for a user, and a save button that updates the user.
@app.route('/users/<user_id>/edit', methods=['GET', 'POST'])
def user_edit(user_id):
    # **POST */users/[user-id]/edit :***Process the edit form, returning the user to the ***/users*** page.
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        image_url = request.form.get('image_url')
        print("post method")
    # find user in db 
    # if user: -if user exist
    return render_template('user_edit_page.html')
    # else elsesend to user not found page or redirect to userlist
    # return refirect with flash

# **POST */users/[user-id]/delete :*** Delete the user.
@app.route('/users/<user_id>/delete')
def user_delete(user_id):
    # if user found 
    flash('User deleted successfully', 'success')
    # else error 
    flash('User not found', 'error')
    # always run 
    return redirect(url_for('list_users'))


if __name__ == '__main__':
    app.run(debug=True)