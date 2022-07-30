from flask import Flask, render_template, url_for

app = Flask(__name__)

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



if __name__ == '__main__':
    app.run(debug=True) 