from flask import Flask, url_for, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
import uuid
import bcrypt

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'static/images'

app.secret_key = 'flash message'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/haranobiggopti'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    category = db.Column(db.String(50))
    description = db.Column(db.String(500))
    status = db.Column(db.String(50))
    security_question = db.Column(db.String(255))
    security_question_answer = db.Column(db.String(255))
    person_name = db.Column(db.String(255))
    person_age = db.Column(db.String(255))
    gender = db.Column(db.String(50))
    animal = db.Column(db.String(50))
    govt_paper_type = db.Column(db.String(50))
    certificate_type = db.Column(db.String(50))
    tags = db.Column(db.String(255))
    image = db.Column(db.String(255))
    created_by = db.Column(db.String(255))
    timestamp = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def __init__(self, title, category, description, status, security_question, security_question_answer, created_by, person_name=None, person_age=None, gender=None, animal=None, govt_paper_type=None, certificate_type=None, tags=None, image=None):
        self.title = title
        self.category = category
        self.description = description
        self.status = status
        self.security_question = security_question
        self.security_question_answer = security_question_answer
        self.person_name = person_name
        self.person_age = person_age
        self.gender = gender
        self.animal = animal
        self.govt_paper_type = govt_paper_type
        self.certificate_type = certificate_type
        self.tags = tags
        self.image = image
        self.created_by = created_by

@app.route("/")
def index():
    if 'name' in session:
        name = session['name']
    else:
        name = None  

    posts = Post.query.all()

    return render_template('index.html', posts=posts, name = name)

@app.route("/create_posts", methods=['GET', 'POST'])
def cp():

    if 'id' in session:
        id = session['id']
    else:
        id = None  

    if 'id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        description = request.form['description']
        status = request.form['status'] 
        security_question = request.form['security_question']
        security_question_answer = request.form['security_question_answer']
        person_name = request.form.get('person_name')
        person_age = request.form.get('person_age')
        gender = request.form.get('gender')
        animal = request.form.get('animal')
        govt_paper_type = request.form.get('govt_paper_type')
        certificate_type = request.form.get('certificate_type')
        tags = request.form.get('tags')
        img = str(uuid.uuid4())
        image = request.files['image']
        image.save('static/images/' + img + '.jpg')
        image_filename = 'images/' + img + '.jpg'

        if category == 'Person':
            new_post = Post(title=title, category=category, description=description, status=status, security_question=security_question, security_question_answer=security_question_answer, person_name=person_name, person_age=person_age, gender=gender, tags=tags, image=image_filename, created_by=session['name'])
        elif category == 'Pet':
            new_post = Post(title=title, category=category, description=description, status=status, security_question=security_question, security_question_answer=security_question_answer, animal = animal, tags=tags, image=image_filename, created_by=session['name'])

        elif category == 'govt_paper_type':
            new_post = Post(title=title, category=category, description=description, status=status, security_question=security_question, security_question_answer=security_question_answer, govt_paper_type=govt_paper_type, tags=tags, image=image_filename, created_by=session['name'])

        elif category == 'certificate_type':
            new_post = Post(title=title, category=category, description=description, status=status, security_question=security_question, security_question_answer=security_question_answer, certificate_type=certificate_type, tags=tags, image=image_filename, created_by=session['name'])

        new_post = Post(title=title, category=category, description=description, status=status, security_question=security_question, security_question_answer=security_question_answer, created_by=session['name'], person_name=person_name, person_age=person_age, gender=gender, animal=animal, govt_paper_type=govt_paper_type, certificate_type=certificate_type, tags=tags, image=image_filename)

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('cp.html', id = id)

@app.route('/category/<string:category>')
def category(category):
    
    return render_template('category.html')


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