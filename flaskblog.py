from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return "<p>Hello, Ouou!</p>"

@app.route("/about")
def about():
    return "<p>This is the About Page!</p>"



# if __name__ == '__main__':
#     app.run(debug=True)