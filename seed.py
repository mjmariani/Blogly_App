"""Seed file to make simple data for users db."""

from models import User, db 
from app import app

#create all tables
db.drop_all()
db.create_all()

#if table isn't empty, empty it
User.query.delete()

#Add users
Tom = User(first_name = 'Tom', last_name='Johnson', image_url ='www.google.com')
Jason = User(first_name='Jasson', last_name='Cartwright')
Colt = User(first_name='Colt', last_name='Steele', 
            image_url='https://www.google.com/url?sa=i&url=https%3A%2F%2Ftwitter.com%2Fcoolcoltsteele&psig=AOvVaw2u2gTVXhRtI1qFxKd7VZMW&ust=1601332067267000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJjQ9v2wiuwCFQAAAAAdAAAAABAD'
            )

#Add new objects to session, so they'll persist
db.session.add(Tom)
db.session.add(Jason)
db.session.add(Colt)

#Commit to database to save it
db.session.commit()

