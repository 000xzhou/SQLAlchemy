"""Blogly application."""

from flask import Flask, render_template, redirect, request, url_for, flash
from models import db, connect_db, User, Post, Tag, PostTag
from dotenv import load_dotenv
load_dotenv()
import os


app = Flask(__name__)
secret_key = os.environ.get('SECRET_KEY')
database_uri = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.secret_key = secret_key

connect_db(app)
# Use app.app_context() to create an application context
with app.app_context():
    db.create_all()

# **GET */ :*** Change the homepage to a page that shows the 5 most recent posts.
@app.route('/')
def homepage():
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('homepage.html', posts=recent_posts)

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
    # user = User.query.get_or_404(user_id)
    user = User.query.get(user_id)
    if user:
        posts = user.posts  
        return render_template('user_detail_page.html', user=user, posts=posts)
    else:
        flash('User not found', 'error')
        return redirect(url_for('list_users'))

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
    return render_template('user_edit_page.html', user = user)

# **POST */users/[user-id]/delete :*** Delete the user.
@app.route('/users/<user_id>/delete')
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('list_users'))


# **GET */users/[user-id]/posts/new :*** Show form to add a post for that user.
# **POST */users/[user-id]/posts/new :*** Handle add form; add post and redirect to the user detail page.
@app.route('/users/<user_id>/posts/new', methods=['GET', 'POST'])
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        add_new_post = Post(title=title, content=content, user_id=user.id)
        db.session.add(add_new_post)
        db.session.commit()
        flash('Post created successfully', 'success')
        return redirect(url_for('user_detail', user_id=user_id))
    
    return render_template('new_post_form.html', user = user)

# **GET */posts/[post-id] :*** Show a post. Show buttons to edit and delete the post.
@app.route('/posts/<posts_id>')
def post_details(posts_id):
    post = Post.query.get_or_404(posts_id)
    return render_template('post_detail_page.html', post=post)


# **GET */posts/[post-id]/edit :*** Show form to edit a post, and to cancel (back to user page).
# **POST */posts/[post-id]/edit :*** Handle editing of a post. Redirect back to the post view.
@app.route('/posts/<posts_id>/edit', methods=['GET', 'POST'])
def edit_post(posts_id):
    post = Post.query.get_or_404(posts_id)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        post.title = title
        post.content = content
        db.session.commit()
        flash('Post Edited Successfully', 'success')
        return redirect(url_for('post_details', posts_id=posts_id))
        
    return render_template('post_edit_page.html', post=post)

# **POST */posts/[post-id]/delete :*** Delete the post.
@app.route('/posts/<posts_id>/delete')
def delete_post(posts_id):
    post = Post.query.get_or_404(posts_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully', 'success')
    return redirect(url_for('homepage'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# **GET */tags :*** Lists all tags, with links to the tag detail page.
@app.route('/tags')
def list_of_tags():
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('tags_list.html', tags=tags)


# **GET */tags/[tag-id] :*** Show detail about a tag. Have links to edit form and to delete.
@app.route('/tags/<tag_id>')
def tag_detail(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    
    return render_template('tag_detail.html', tag = tag)

# **GET */tags/new :*** Shows a form to add a new tag.
# **POST */tags/new :*** Process add form, adds tag, and redirect to tag list.
@app.route('/tags/new', methods=['GET', 'POST'])
def new_tag():
    if request.method == 'POST':
        name = request.form.get('name')
        add_new_tag = Tag(name=name)
        db.session.add(add_new_tag)
        db.session.commit()
        return redirect(url_for('list_of_tags'))
        
    return render_template('new_tag_form.html')


# **GET */tags/[tag-id]/edit :*** Show edit form for a tag.
# **POST */tags/[tag-id]/edit :*** Process edit form, edit tag, and redirects to the tags list.
@app.route('/tags/<tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    if request.method == 'POST':
        name = request.form.get('name')
        tag.name = name
        db.session.commit()
        flash('Tag Edited Successfully', 'success')
        return redirect(url_for('list_of_tags'))
    return render_template('tag_edit_page.html', tag=tag)

# **POST */tags/[tag-id]/delete :*** Delete a tag.
@app.route('/tags/<tag_id>/delete')
def tag_deleting(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag deleted successfully', 'success')
    return redirect(url_for('homepage'))


if __name__ == '__main__':
    app.run(debug=True)