from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# class TimestampMixin(object):
#     created = db.Column(
#         db.DateTime, nullable=False, default=datetime.utcnow)
   
class User(db.Model):
    """Individual user as a class"""
    __tablename__ = 'users'

    def __repr__(self):
        """Show user info"""
        return  f"<User {self.first_name} {self.last_name}>"
    
    def delete_user(self):
        """Deletes a user"""
        db.session.delete(self)
        db.session.commit()

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(20),
                           nullable = False)
    last_name = db.Column(db.String(35),
                          nullable = False)
    username = db.Column(db.String(12),
                         unique = True,
                         nullable = False)
    image_url = db.Column(db.String)


class Post(db.Model):
    """Class definition of posts"""

    __tablename__ = 'posts'

    def delete_post(self):
        """Deletes a post"""
        db.session.delete(self)
        db.session.commit()

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.String,
                      nullable = False)
    content = db.Column(db.String)

    username = db.Column(db.Text,
                         db.ForeignKey('users.username'))
    
    user = db.relationship('User', backref='posts')