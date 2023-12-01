from flask_sqlalchemy import SQLAlchemy
from app import db

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(255), nullable=False)
    l_name = db.Column(db.String(255), nullable=False)
    student_email = db.Column(db.String(255), unique=True, nullable=False)

class Professor(db.Model):
    faculty_id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(255), nullable=False)
    l_name = db.Column(db.String(255), nullable=False)
    faculty_email = db.Column(db.String(255), unique=True, nullable=False)

class Course(db.Model):
    course_name = db.Column(db.String(255), primary_key=True, nullable=False)
    semester = db.Column(db.Integer, primary_key=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('professor.faculty_id'))
    professor = db.relationship('Professor', backref=db.backref('courses', lazy=True))

class Session(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    date = db.Column(db.Date)
    course_name = db.Column(db.String(255), db.ForeignKey('course.course_name'), primary_key=True, nullable=False)
    semester = db.Column(db.Integer, db.ForeignKey('course.semester'), primary_key=True, nullable=False)
    course = db.relationship('Course', backref=db.backref('sessions', lazy=True))

class Attendance(db.Model):
    session_course_name = db.Column(db.String(255), primary_key=True, nullable=False)
    session_semester = db.Column(db.Integer, primary_key=True, nullable=False)
    session_number = db.Column(db.Integer, primary_key=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), primary_key=True, nullable=False)
    session = db.relationship('Session', backref=db.backref('attendance', lazy=True))
    student = db.relationship('Student', backref=db.backref('attendance', lazy=True))
