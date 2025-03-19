from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from main import db, app
from sqlalchemy.dialects.sqlite import JSON
# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    programming_skills = db.relationship('ProgrammingSkill', backref='user', lazy=True)
    work_experiences = db.relationship('WorkExperience', backref='user', lazy=True)
    education = db.relationship('Education', backref='user', lazy=True)
    certifications = db.relationship('Certification', backref='user', lazy=True)
    projects = db.relationship('Project', backref='user', lazy=True)
    blog_posts = db.relationship('BlogPost', backref='user', lazy=True)

    
    def __repr__(self):
        return f'<User {self.username}>'

# Programming Skills Model
class ProgrammingSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Work Experience Model
class WorkExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(100), nullable=False, default="Brain")
    color = db.Column(db.String(50), nullable=True)
    achievements =  db.Column(JSON, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Education Model
class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(200), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    period = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    gpa = db.Column(db.String(10))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Certifications Model
class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    expiry = db.Column(db.String(100), nullable=True)
    credential_id = db.Column(db.String(100))
    icon = db.Column(db.String(100), nullable=True)
    skills =  db.Column(JSON, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Projects Model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-incrementing ID
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    long_description = db.Column(db.Text)  # Added longDescription
    image = db.Column(db.String(300))
    technologies = db.Column(JSON, nullable=False)  # Storing as JSON array
    purpose = db.Column(db.Text)
    approach = db.Column(db.Text)
    contribution = db.Column(db.Text)
    results = db.Column(db.Text)
    github = db.Column(db.String(300))
    demo = db.Column(db.String(300))
    category = db.Column(db.String(100))
    features = db.Column(JSON)  # JSON to store array of feature objects
    screenshots = db.Column(JSON)  # JSON to store array of image URLs
    tech_stack = db.Column(JSON)  # JSON to store categorized tech stack
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Blog Posts Model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    tags = db.Column(db.Text)
    read_time = db.Column(db.String(50))
    image = db.Column(db.String(300))
    author_name = db.Column(db.String(100), nullable=False)
    author_avatar = db.Column(db.String(300))
    featured = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Initialize Database

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
