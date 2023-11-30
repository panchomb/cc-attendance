from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Professor(db.Model):
    professor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

class Course(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    semester = db.Column(db.String(50), primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.professor_id'))
    professor = db.relationship('Professor', backref='courses')

class Session(db.Model):
    course_name = db.Column(db.String(100), primary_key=True)
    course_semester = db.Column(db.String(50), primary_key=True)
    number = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    start = db.Column(db.Time)
    end = db.Column(db.Time)

class Attendance(db.Model):
    course_name = db.Column(db.String(100), primary_key=True)
    course_semester = db.Column(db.String(50), primary_key=True)
    session_number = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), primary_key=True)
    student = db.relationship('Student', backref='attendances')

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
