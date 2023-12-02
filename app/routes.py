from app import app, db
from flask import render_template, request, jsonify
from app.models import Student, Professor, Course, Session, Attendance, AttendanceCode
import random
import string
import threading
import time

code = None
next_update_time = None
timer_thread = None
attendees = {}
attendees['attendees'] = []
stop_timer_thread = threading.Event()

@app.route('/', methods=["GET"])
def home():
    return render_template('index.html')

@app.route('/student_page', methods=["GET"])
def student_page():
    return render_template('student_page.html')

@app.route('/professor_page', methods=["GET"])
def professor_page():
    return render_template('professor_page.html')

@app.route('/professor_attendance_page', methods=["GET"])
def professor_attendance_page():
    return render_template('professor_attendance_page.html')

@app.route('/submit_class_student', methods=["GET"])
def submit_class_student():
    return render_template('submit_class_student.html')

@app.route('/submit_class_professor', methods=["GET"])
def submit_class_professor():
    return render_template('submit_class_professor.html')


@app.route('/code', methods=["GET"])
def show_attendance():
    return render_template('show_attendance.html')

@app.route('/submit_attendance', methods=["GET"])
def submit_attendance():
    return render_template('submit_attendance.html')

@app.route('/verify_attendance', methods=["GET"])
def verify_attendance():
    return render_template('verify_attendance.html')

@app.route('/stop_attendance', methods=["POST"])
def stop_attendance():
    request_json = request.get_json()

    course_name = request_json['course_name']
    course_semester = request_json['semester']
    session_number = request_json['number']

    students = Attendance.query.filter_by(session_cousre_name=course_name, session_semester=course_semester, session_number=session_number).all()

    return jsonify([format_student(student) for student in students])

@app.route('/view_attendees', methods=["GET"])
def view_attendees():
    global attendees

    return jsonify(attendees)

@app.route('/generate_code', methods=["POST"])
def generate_code():
    '''
    Generate a random 6 character code and insert it into the database
    '''
    request_data = request.get_json()
    course_name = request_data['course_name']
    semester = request_data['semester']
    session_number = request_data['number']

    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    session = Session.query.filter_by(course_name=course_name, semester=semester, number=session_number).first()
    attendance_code = AttendanceCode(course_name=session.course_name, course_semester=session.semester, session_number=session.number, code=code)
    db.session.add(attendance_code)
    db.session.commit()

    return code



def format_student(student):
    return {
        'student_id': student.student_id,
        'f_name': student.f_name,
        'l_name': student.l_name,
        'student_email': student.student_email
    }