from app import app
from flask import render_template, request, jsonify
import random
import string
import time

code = ''
timer = 30

@app.route('/', methods=["GET"])
def home():
    '''
    This function returns the home page.
    '''
    return render_template('index.html')

@app.route('/code', methods=["GET"])
def show_attendance():
    return render_template('show_attendance.html')

@app.route('/submit_attendance', methods=["GET"])
def submit_attendance():
    return render_template('submit_attendance.html')

@app.route('/verify_attendance', methods=["GET"])
def verify_attendance():
    return render_template('verify_attendance.html')

@app.route('/get_code', methods=["GET"])
def get_code():
    '''
    This function generates a 6 character alphanumeric code.
    '''
    global code
    if code == '':
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return code

@app.route('/check_attendance', methods=["POST"])
def check_attendance():
    global code
    request_data = request.get_json()
    user_code = request_data.get('code', '')
    
    if user_code == code:
        response = {'verification': 'success'}
    else:
        response = {'verification': 'failure'}
    
    return jsonify(response)
