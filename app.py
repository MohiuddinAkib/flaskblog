from flask import Flask, render_template, url_for, request, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
# Csrf token
csrf = CSRFProtect(app)

# Secret key
app.config['SECRET_KEY'] = '7cb40e16074e4222e8ee8a99e9364353'

# posts
posts = [
    {
        'author': 'Md akib',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'Feb 24, 2019'
    },
    {
        'author': 'Md alif',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'Feb 27, 2019'
    },
    {
        'author': 'Mr jane',
        'title': 'Blog post 3',
        'content': 'Third post content',
        'date_posted': 'Jan 11, 2019'
    },
]

# Home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


# About page
@app.route('/about')
def about():
    return render_template('about.html', title="About")


# Login route
@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form, title="Login")

# 404 page
@app.errorhandler(404)
def page_not_found(error):
    return error


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        flash(f"Account created for {form.username.data}", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
