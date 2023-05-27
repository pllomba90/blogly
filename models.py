from flask_sqlalchemy import SQLAlchemy

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

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(20),
                           nullable = False)
    last_name = db.Column(db.String(35),
                          nullable = False)
    image_url = db.Column(db.String)
