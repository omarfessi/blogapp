from crypt import methods
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '760be9e130b66f380a1d4430d42c91fa'
posts = [
    {
        'author' : 'Donatello', 
        'title' : 'Blog Post 1', 
        'content' : 'First post content', 
        'date_posted' : '12 April 1994'

    },

        {
        'author' : 'Leanardo', 
        'title' : 'Blog Post 2', 
        'content' : 'Second post content', 
        'date_posted' : '13 July 1995'

    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    var = 'Omar'
    return render_template('about.html', title='about')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Welcome {}! Your account has been created'.format(form.username.data), 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form = form)
    
@app.route("/login",  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='login', form = form)


if __name__ == '__main__':
    app.run(debug=True) 