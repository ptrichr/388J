from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager


# TODO: implement
@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

# TODO: implement fields
class User(db.Document, UserMixin):
    username = db.StringField(min_length=1, 
                              max_length=40, 
                              unique=True, 
                              required=True)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()

    # Returns unique string identifying our object
    def get_id(self):
        # TODO: implement
        return self.username


# TODO: implement fields
class Review(db.Document):
    commenter = db.ReferenceField(User)
    content = db.StringField(min_length=5, max_length=500, required=True)
    date = db.StringField()
    imdb_id = db.StringField(min_length=9, max_length=9, required=True)
    movie_title = db.StringField(min_length=1, max_length=100, required=True)
    image = db.StringField()