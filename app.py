
from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post


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

@app.route('/user/new', methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form['username']
        image_url = request.form["image_url"]

        new_user = User(first_name=first_name, last_name=last_name, username=username, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
    
        return redirect(f'/user/{new_user.id}')
    else:
        return render_template('add_user.html')

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
    User.delete_user(user)

    return redirect('/users')

@app.route('/user/<int:user_id>/add_post', methods=['GET', 'POST'])
def add_post(user_id):
    user = User.query.get(user_id)

    if request.method == 'POST':
        title = request.form['post_title']
        content = request.form['post_body']

        new_post = Post(title=title, content=content, username=user.username)
        db.session.add(new_post)
        db.session.commit()

        return redirect(f'/post/{new_post.id}')
    else:
        return render_template('add_post.html', user=user)
    
@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    Post.delete_post(post)

    return redirect('/')

@app.route('/')
def show_posts():
    posts = Post.query.all()
    
    return render_template('posts.html', posts=posts)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template('single_post.html', post=post)