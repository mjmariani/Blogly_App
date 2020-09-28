"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolException
###importing db object and connect_db function from models module
from models import db, connect_db 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "blogging"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolException(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    """Shows home page"""
    return render_template('home.html')

