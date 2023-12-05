import logging
import azure.functions as func
import json
from datetime import datetime
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage

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
    code = req.params.get('code')

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
            code = req_body.get('code')

    
    current_code, active = get_attendance_code(course_name, course_semester, session_number)
    if code == current_code:
        if active == True:
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
        else:
            return func.HttpResponse(
                    json.dumps(dict(error="Attendance code is not active.")),
                    headers=headers,
                    status_code=400
            )
    else:
        # Send request to Dead Letter Queue (DLQ)
        send_to_dlq(req)
        return func.HttpResponse(
            json.dumps(dict(error="Invalid attendance code.")),
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

    insert_query = f"INSERT INTO attendance(session_course_name, session_semester, session_number, student_id) VALUES ('{course_name}','{course_semester}', {session_number}, {student_id})"

    cursor = cnx.cursor()
    cursor.execute(insert_query)
    cnx.commit()

    cursor.close()
    cnx.close()

    return True

def get_attendance_code(course_name, course_semester, session_number):
    import os

    username=os.environ['db_username']
    password=os.environ['db_password']
    host=os.environ['db_host']
    database=os.environ['db_name']

    import mysql.connector
    cnx = mysql.connector.connect(user=username, password=password,
                                host=host, database=database)

    select_query = f"SELECT code, active FROM attendance_code WHERE course_name='{course_name}' AND course_semester='{course_semester}' AND session_number={session_number} ORDER BY created_at DESC LIMIT 1"

    cursor = cnx.cursor()
    cursor.execute(select_query)
    result = cursor.fetchone()

    cursor.close()
    cnx.close()

    return result

def send_to_dlq(req: func.HttpRequest):
    '''
    Send the request to the Dead Letter Queue (DLQ) in Azure Storage Queue
    '''
    import os

    connection_string = os.environ["connection_string"]
    queue_name = os.environ["queue_name"]

    try:
        # Create a QueueServiceClient instance using the connection string
        queue_service_client = QueueServiceClient.from_connection_string(connection_string)

        # Get a reference to the queue
        queue_client = queue_service_client.get_queue_client(queue_name)

        # Add the request to the queue
        queue_client.send_message(req.get_body().decode('utf-8'))

    except Exception as ex:
        logging.error(f"Error sending message to DLQ: {ex}")

    return True