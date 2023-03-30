from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentName = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))

class Course(db.Model):
    course_code = db.Column(db.String(10), primary_key=True)
    course_title = db.Column(db.String(100), nullable=False)
    course_description = db.Column(db.Text)
    course_level = db.Column(db.String(20))
    course_credits = db.Column(db.Integer)

db.create_all()
