
from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secrets'
app.config['SQLALCHEMY_DATABASE_URI' ] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG_TB_ENABLED'] = True

debug = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    db.create_all()


app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secrets'


@app.route('/users')
def home_page():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/user/<int:user_id>')
def user_page(user_id):
    user = User.query.get(user_id)
    return render_template('info.html', user=user)

@app.route('/user/new')
def new_user():
    return render_template('add_user.html')


@app.route('/user/new', methods=["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(f'/user/{new_user.id}')

@app.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    print('Accessing edit_update_user route')
    user = User.query.get(user_id)
    return render_template('edit.html', user=user, user_id=user_id)


@app.route('/user/<int:user_id>/update', methods=['POST'])
def edit_update_user(user_id):
    user = User.query.get(user_id)

    user.first_name = request.form['first_name_edit']
    user.last_name = request.form['last_name_edit']
    user.image_url = request.form['image_url_edit']
    db.session.commit()

    return render_template('info.html', user=user)



@app.route('/user/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return redirect('/users')
    
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
