"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
###importing db object and connect_db function from models module
from models import db, connect_db, User, Post 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "blogging"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def user_listing():
    """Shows home page, which is the list of Users"""
    
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('User_Listing.html', users = users)

@app.route('/users/<int:user_id>')
def user_info(user_id):
    """Shows page with detailed information about a particular User"""
    
    user = User.query.get_or_404(user_id)
    return render_template('User_Detail.html', user = user)


@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    """Shows a page with a form to edit a user's information"""
    
    user = User.query.get_or_404(user_id)
    return render_template('User_Edit_Page.html', user = user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def user_info_update(user_id):
    """Function to handle form submission in order to update a user's information"""
    
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
 
    db.session.add(user)
    db.session.commit()
    
    return redirect('/')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user_info(user_id):
    """Handle the deletion of a particular user detail"""
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect("/")


###why are we using the GET method here. Do we actually need it since Flask's default is to accept "GET" requests
@app.route('/users/new_user', methods =["GET"])
def users_new_form():
    """Shows a form to create a new user and input into database"""
    
    return render_template('New_User_Form.html')


@app.route('/users/new_user', methods =["POST"])
def new_user_update_to_db():
    """Handles the submission of the form to create a new user"""
    
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )
    
    db.session.add(new_user)
    db.session.commit()
    return redirect("/")


@app.route('/user/<int: user_id>/posts/new', methods=["GET"])
def show_form(user_id):
    """Show a for to create a new post for a specific user"""
    
    user = User.query.get_or_404(user_id)
    return render_template('New_Post_Form.html', user=user)
    
    
    
@app.route('/user/<int: user_id>/posts/new', methods=["POST"])
def handle_add(user_id):
    """Handle a form submission for creating a new post belonging to a user
    """
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'], 
                    content=request.form['content'],
                    user=user)
    
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")
    return redirect(f"/users/{user_id}")
    
    
    
@app.route('/posts/<int: post_id>')
def show_post(post_id):
    """Show a page with info on a specific post
    """
    
    post = Post.query.get_or_404(post_id)
    return render_template('Post_Detail_Page.html', post=post)
    
    

@app.route('/posts/<int: post_id>/edit', methods=["GET"])
def edit_post(post_id):
    """Show a form to edit an existing post
    """
    post = Post.query.get_or_404(post_id)
    return render_template('Post_Edit_Page.html', post=post)
    
    
    
@app.route('/posts/<int: post_id>/edit', methods=["POST"])  
def handle_edit_post(post_id):
    """Handle form submission to an update of an existing post
    """
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")
    
    return redirect(f"/users/{post.user_id}")
    
    
    
@app.route('/posts/<int: post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Handle form submission for deleting an existing post
    """
    
    post= Post.query.get_or_404(post_id)
    
###Bonus Stuff

@app.route('/')
def root():
    """Show recent list of posts, with only the 5 most recent first in desc order."""
    
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("Homepage.html", posts=posts)                      

@app.errorhandler(404)
def page_not_found(e):
    """Show a 404 not found page

    Args:
        e (exception object): error object
    """
    
    return render_template('404.html'), 404

""" # Error handling can also be done without the decorator like below based on docs
app.register_error_handler(400, page_not_found) """

