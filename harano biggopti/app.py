from flask import Flask, url_for, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
import uuid
import bcrypt

app = Flask(__name__)
app.secret_key = 'flash message'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/haranobiggopti'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# db starts
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    number = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255))

    def __init__(self, name, email, number, password):
        self.name = name
        self.email = email
        self.number = number
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
class post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    number = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255))

    def __init__(self, name, email, number, password):
        self.name = name
        self.email = email
        self.number = number

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/create_posts")
def cp():
    return render_template('cp.html')

# login/logout/signup

@app.route("/login", methods=['GET', 'POST'])
def login():

    if 'number' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        number = request.form['number']
        password = request.form['password']

        user = User.query.filter_by(number=number).first()

        if user and user.check_password(password):
            session['name'] = user.name
            session['email'] = user.email
            session['number'] = user.number
            session['password'] = user.password

            return redirect(url_for('index'))
        else:
            return render_template("login.html", error="Invalid User")
    return render_template("login.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():

    if 'number' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        password = request.form['password']

        new_user = User(name=name, email=email, number=number, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template("signup.html")

@app.route('/logout')
def logout():
    session.pop('number', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)








    id	
    title	
    description	
    section	
    category	
    security	
    image	
    tags