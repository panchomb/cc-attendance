import logging
import azure.functions as func
import json
from datetime import datetime

headers = {
    "Content-type": "application/json",
    "Access-Control-Allow-Origin": "*"
}

def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    This is the entry point for HTTP calls to our function
    '''

    logging.info('Python HTTP trigger function processed a request.')

    # For HTTP GET requests
    course_name = req.params.get('course_name')
    course_semester = req.params.get('course_semester')
    session_number = req.params.get('session_number')
    student_id = req.params.get('student_id')

    # For HTTP POST requests, when params are provided in the HTTP body:
    if not course_name or not course_semester or not session_number or not student_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            course_name = req_body.get('course_name')
            course_semester = req_body.get('course_semester')
            session_number = req_body.get('session_number')
            student_id = req_body.get('student_id')

    # Event is routed to the target database and table
    try:
        insert_attendance(course_name, course_semester, session_number, student_id)
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
                json.dumps(dict(error="Supported parameters: course_name, course_semester, session_number, student_id", exception=str(ex))),
                headers=headers,
                status_code=400
        )

    # Return the event back to the client as successful feedback
    return func.HttpResponse(
            json.dumps(dict(course_name=course_name, course_semester=course_semester, session_number=session_number, student_id=student_id)),
            headers=headers,
            status_code=200
    )

def insert_attendance(course_name, course_semester, session_number, student_id):
    '''
    Insert attendance information into the Attendance table
    Connection details stored as Function Application settings
    '''
    import os

    # This must be set as Function application settings. https://learn.microsoft.com/en-us/azure/azure-functions/functions-app-settings
    username=os.environ['db_username']
    password=os.environ['db_password']
    host=os.environ['db_host']
    database=os.environ['db_name']

    import mysql.connector
    cnx = mysql.connector.connect(user=username, password=password,
                                host=host, database=database)

    insert_query = f"INSERT INTO Attendance(course_name, course_semester, session_number, student_id) VALUES ('{course_name}','{course_semester}', {session_number}, {student_id})"

    cursor = cnx.cursor()
    cursor.execute(insert_query)
    cnx.commit()

    cursor.close()
    cnx.close()

    return True
