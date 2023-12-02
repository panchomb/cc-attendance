from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import datetime

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
    number = db.Column(db.Integer, primary_key=True, nullable=False)
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    date = db.Column(db.Date)
    course_name = db.Column(db.String(255), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    
    course = db.relationship(
        'Course',
        backref=db.backref('sessions', lazy=True),
        primaryjoin="and_(Session.course_name==Course.course_name, Session.semester==Course.semester)"
    )

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['course_name', 'semester'],
            ['course.course_name', 'course.semester']
        ),
        {}
    )

class Attendance(db.Model):
    session_course_name = db.Column(db.String(255), nullable=False, primary_key=True)
    session_semester = db.Column(db.Integer, nullable=False, primary_key=True)
    session_number = db.Column(db.Integer, nullable=False, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False, primary_key=True)
    
    student = db.relationship('Student', backref=db.backref('attendance', lazy=True))

    session = db.relationship(
        'Session', 
        backref=db.backref('attendance', lazy=True),
        primaryjoin="and_(Attendance.session_course_name==Session.course_name, "
                     "Attendance.session_semester==Session.semester, "
                     "Attendance.session_number==Session.number)"
    )

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['session_course_name', 'session_semester', 'session_number'],
            ['session.course_name', 'session.semester', 'session.number']
        ),
        {}
    )

class AttendanceCode(db.Model):
    __tablename__ = 'attendance_code'
    course_name = db.Column(db.String(255), nullable=False, primary_key=True)
    course_semester = db.Column(db.Integer, nullable=False, primary_key=True)
    session_number = db.Column(db.Integer, nullable=False, primary_key=True)
    code = db.Column(db.String(255), nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    session = db.relationship(
        'Session', 
        backref=db.backref('codes', lazy=True),
        primaryjoin="and_(AttendanceCode.course_name==Session.course_name, "
                     "AttendanceCode.course_semester==Session.semester, "
                     "AttendanceCode.session_number==Session.number)"
    )

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['course_name', 'course_semester', 'session_number'],
            ['session.course_name', 'session.semester', 'session.number']
        ),
        {}
    )

    def __init__(self, course_name, course_semester, session_number, code):
        self.course_name = course_name
        self.course_semester = course_semester
        self.session_number = session_number
        self.code = code