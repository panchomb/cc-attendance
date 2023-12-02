from app import app, socketio, db
from flask import render_template, request, jsonify
from app.models import Student, Professor, Course, Session, Attendance
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

@app.route('/submit_class', methods=["GET"])
def submit_class():
    return render_template('submit_class.html')

@app.route('/code', methods=["GET"])
def show_attendance():
    return render_template('show_attendance.html')

@app.route('/submit_attendance', methods=["GET"])
def submit_attendance():
    return render_template('submit_attendance.html')

@app.route('/verify_attendance', methods=["GET"])
def verify_attendance():
    return render_template('verify_attendance.html')

@socketio.on('connect', namespace='/code')
def handle_code_connection():
    global next_update_time, code, timer_thread

    # If there is no code being generated, start the timer and generate a code
    if timer_thread == None:
        code = generate_random_code()
        next_update_time = time.time() + 30
        print('generating code from new connection')
        timer_thread = threading.Thread(target=update_code_timer)
        timer_thread.start()

    print(f'Client connected {request.remote_addr}')
    
    socketio.emit('code_update', {'code': code, 'current_time': time.time(), 'next_update_time': next_update_time}, namespace='/code')

@socketio.on('disconnect', namespace='/code')
def handle_code_disconnection():
    global timer_thread

    print(f'Client disconnected {request.remote_addr}')

def update_code_timer():
    global code, next_update_time

    while not stop_timer_thread.is_set():
        if time.time() >= next_update_time:
            code = generate_random_code()
            next_update_time = time.time() + 30
            socketio.emit('code_update', {'code': code, 'current_time': time.time(), 'next_update_time': next_update_time}, namespace='/code')

@app.route('/check_attendance', methods=["POST"])
def check_attendance():
    global code

    response = {}

    if code == None:
        response['invalid'] = True
        return jsonify(response)

    request_data = request.get_json()
    user_code = request_data.get('code', '')
    
    if user_code == code:
        response['verification'] = 'success'
        attendees['attendees'].append(time.time())
        print(attendees)
    else:
        response['verification'] = 'failure'

    response['invalid'] = False
    
    return jsonify(response)

@app.route('/stop_attendance', methods=["POST"])
def stop_attendance():
    global timer_thread, code, next_update_time, stop_timer_thread
    response = {}

    if timer_thread and timer_thread.is_alive():
        stop_timer_thread.set()

        timer_thread.join(timeout=1)

        if timer_thread.is_alive():
            print('failed to stop attendance')
            response['status'] = 'failure'
        else:
            response['status'] = 'success'
            timer_thread = None
            code = None
            next_update_time = None
            attendees['attendees'] = []
            stop_timer_thread.clear()
            print('stopping attendance')
    else:
        print('error stopping attendance')
        response['status'] = 'error'

    return jsonify(response)

@app.route('/view_attendees', methods=["GET"])
def view_attendees():
    global attendees

    return jsonify(attendees)

def generate_random_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def serialize_student(student):
    return {
        'student_id': student.student_id,
        'f_name': student.f_name,
        'l_name': student.l_name,
        'student_email': student.student_email
    }


if __name__ == '__main__':
    socketio.run(app, debug=True)
