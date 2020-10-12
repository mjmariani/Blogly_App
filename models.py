"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
# Models below

class User(db.Model):
    __tablename__ = 'Users'
    
    def __repr__(self):
        p = self
        return f"<User id= {p.id}, first name = {p.first_name}, last name ={p.last_name}, image URL = {p.image_url}"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.Text,
                           nullable=False,
                           unique=False)
    
    last_name = db.Column(db.Text, nullable=False, unique=False)
    
    image_url = db.Column(db.Text, nullable=True, unique=False)
    
    @property 
    def full_name(self):
        """Return full name of user."""
        
        return f"{self.first_name} {self.last_name}"
    