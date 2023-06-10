from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


   
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

    # posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")


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

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)

    username = db.Column(db.Text,
                         db.ForeignKey('users.username'))
    
    tags = db.relationship('Tag', secondary='post_tag', backref='posts')


    @property
    def friendly_date(self):
        """Return nicer date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    
class Tag(db.Model):
    """Creates a library of tags"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key = True)
    
    name = db.Column(db.Text,
                     nullable = False,
                     unique = True)
    
    posts = db.relationship(
        'Post',
        secondary="post_tag",
        backref="tags",)
    
class PostTag(db.Model):
    """Connects the posts and the tags"""

    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key = True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id"),
                       primary_key = True)