from flask import Flask, render_template, url_for, request, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from datetime import datetime
import os

# Initi app
app = Flask(__name__)
# App secret key
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY') or '7cb40e16074e4222e8ee8a99e9364353'
# Csrf token
csrf = CSRFProtect(app)
# DB uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URI') or 'postgresql://postgres:akib123@localhost/flaskblog'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
#     'DATABASE_URI') or "postgresql://root:''@localhost/flaskblog"
# DB instance
db = SQLAlchemy(app)
# DB migration handler
migrate = Migrate(app=app, db=db)


# User model
class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg', nullable=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def __str__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    def __str__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# Home page
@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


# About page
@app.route('/about')
def about():
    return render_template('about.html', title="About")


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.email.data == 'newaz@gmail.com' and form.password.data == '123456':
            flash(f"You are now logged in as {form.email.data}", 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login unseccessful. Please check username and password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form, title="Login")


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash(f"Account created for {form.username.data}", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


# 404 page
@app.errorhandler(404)
def page_not_found(error):
    return error


if __name__ == "__main__":
    app.run(debug=True, port=8000)
