from flask import Flask, url_for, render_template, redirect, request, session, g
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.secret_key = 'flash message'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/haranobiggopti'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

posts = [
    {
        'user': 'Mahamudul',
        'title': 'lost',
        'date_postsed': '13th july, 2021',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.'
    },
    {
        'user': 'Hasan',
        'title': 'lost',
        'date_postsed': '9th March, 2022',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.'
    },
    {
        'user': 'Tanvir',
        'title': 'lost',
        'date_postsed': '20th April, 2019',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.'
    }
]


@app.route("/")
def index():
    return render_template('index.html', post = posts)

@app.route("/create_posts")
def cp():
    return render_template('cp.html')

@app.route("/user")
def user():
    return render_template('profile.html', post = posts)

# login/logout/signup

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/logout')
def logout():
    session.pop('number', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)