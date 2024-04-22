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
    role = db.Column(db.String(50), default='user')

    def __init__(self, name, email, number, password, role=None):
        self.name = name
        self.email = email
        self.number = number
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
        if role:
            self.role = role


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
    tags = db.Column(db.String(255))
    image = db.Column(db.String(255))
    created_by = db.Column(db.String(255))
    timestamp = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    person_name = db.Column(db.String(255))
    person_age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    animal = db.Column(db.String(50))
    govt_paper_type = db.Column(db.String(50))
    certificate_type = db.Column(db.String(50))
    post_status = db.Column(db.String(50), default='pending')

    def __init__(self, title, category, description, status, security_question, security_question_answer, created_by, person_name , person_age , gender , animal , govt_paper_type , certificate_type , tags , image, post_status=None):  # Make post_status optional
        self.title = title
        self.category = category
        self.description = description
        self.status = status
        self.security_question = security_question
        self.security_question_answer = security_question_answer
        self.tags = tags
        self.image = image
        self.created_by = created_by
        self.person_name = person_name
        self.person_age = person_age
        self.gender = gender
        self.animal = animal
        self.govt_paper_type = govt_paper_type
        self.certificate_type = certificate_type
        if post_status:
            self.post_status = post_status

@app.route("/")
def index():
    if 'id' in session:
        id = session['id']
    else:
        id = None  

    if 'name' in session:
        name = session['name']
    else:
        name = None  

    posts = Post.query.filter_by(post_status='approved').all()

    return render_template('index.html', posts=posts, id = id, name = name)

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
        person_age = request.form.get('person_age') or None
        gender = request.form.get('gender')
        animal = request.form.get('animal')
        govt_paper_type = request.form.get('govt_paper_type')
        certificate_type = request.form.get('certificate_type')
        tags = request.form.get('tags')
        img = str(uuid.uuid4())
        image = request.files['image']
        image.save('static/images/' + img + '.jpg')
        image_filename = 'images/' + img + '.jpg'

        new_post = Post(title=title, category=category, description=description, status=status, security_question=security_question, security_question_answer=security_question_answer, created_by=session['name'], person_name=person_name, person_age=person_age, gender=gender, animal=animal, govt_paper_type=govt_paper_type, certificate_type=certificate_type, tags=tags, image=image_filename)

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('cp.html', id = id)

@app.route('/category/<string:category>')
def category(category):
    if 'id' in session:
        id = session['id']
    else:
        id = None  

    if 'name' in session:
        name = session['name']
    else:
        name = None  

    if 'id' not in session:
        return redirect(url_for('login'))
        
    category_posts = Post.query.filter_by(category=category).all()
    return render_template('category.html', category=category, category_posts=category_posts, id = id, name = name)

@app.route("/admin")
def admin_panel():
    id = session.get('id')
    if 'role' in session and session['role'] == 'admin':
        return render_template("admin.html", id=id)
    else:
        return ("<h1><b>404 not found</b></h1>")
    
@app.route("/user")
def user():
    
    posts = User.query.all()

    return render_template("control.html", posts=posts)

@app.route("/pending")
def pending():
    pending_posts = Post.query.filter_by(post_status='pending').all()
    return render_template("control.html", posts=pending_posts, post_status="pending")

@app.route("/approved")
def approved():
    approved_posts = Post.query.filter_by(post_status='approved').all()
    return render_template("control.html", posts=approved_posts, post_status="approved")

@app.route("/declined")
def declined():
    declined_posts = Post.query.filter_by(post_status='declined').all()
    return render_template("control.html", posts=declined_posts, post_status="declined")

@app.route("/solved")
def solved():
    solved_posts = Post.query.filter_by(post_status='solved').all()
    return render_template("control.html", posts=solved_posts, post_status="solved")

@app.route("/approve_post/<int:post_id>")
def approve_post(post_id):
    post = Post.query.get(post_id)
    post.post_status = 'approved'
    db.session.commit()
    return redirect(url_for('user'))

@app.route("/decline_post/<int:post_id>")
def decline_post(post_id):
    post = Post.query.get(post_id)
    post.post_status = 'declined'
    db.session.commit()
    return redirect(url_for('user'))

@app.route("/solved_post/<int:post_id>")
def solved_post(post_id):
    post = Post.query.get(post_id)
    post.post_status = 'solved'
    db.session.commit()
    return redirect(url_for('user'))

# login/logout/signup

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'id' in session:
        id = session['id']
    else:
        id = None  

    if 'number' in session:
        number = session['number']
    else:
        number = None  

    if 'id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        number = request.form['number']
        password = request.form['password']

        user = User.query.filter_by(number=number).first()

        if user and user.check_password(password):
            session['id'] = user.id
            session['name'] = user.name
            session['email'] = user.email
            session['number'] = user.number
            session['password'] = user.password
            session['role'] = user.role

            print("User role:", session['role']) 

            return redirect(url_for('index'))
        else:
            return render_template("login.html", error="Invalid User")
    return render_template("login.html", id=id, number=number)

@app.route("/signup", methods=['GET', 'POST'])
def signup(): 
    if 'number' in session:
        number = session['number']
    else:
        number = None  
        
    if 'id' in session:
        id = session['id']
    else:
        id = None 

    if 'id' in session:
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
    
    return render_template("signup.html", number = number, id = id)

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
