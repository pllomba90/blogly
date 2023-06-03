from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name='Bob', last_name='Loblaw', username='blob1')
u2 = User(first_name='Anita', last_name='Dick', username='adick2')
u3 = User(first_name='Amanda', last_name='Hugnkiss', username='ahugn3')

db.session.add(u1)
db.session.add(u2)
db.session.add(u3)

db.session.commit()