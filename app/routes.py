from app import app
from flask import render_template
import random
import string

@app.route('/', methods=["GET"])
def home():
    '''
    This function returns the home page.
    '''
    return render_template('index.html')

@app.route('/get_code', methods=["GET"])
def get_code():
    '''
    This function generates a 6 character alphanumeric code.
    '''
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return code
