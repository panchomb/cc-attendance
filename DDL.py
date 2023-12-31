import sqlite3
import mysql.connector

def create_tables(conn):
    cursor = conn.cursor()

    # Create student table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student (
            student_id INTEGER PRIMARY KEY,
            f_name VARCHAR(255) NOT NULL,
            l_name VARCHAR(255) NOT NULL,
            student_email VARCHAR(255) UNIQUE NOT NULL
        );
    ''')

    # Create professor table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS professor (
            faculty_id INTEGER PRIMARY KEY,
            f_name VARCHAR(255) NOT NULL,
            l_name VARCHAR(255) NOT NULL,
            faculty_email VARCHAR(255) UNIQUE NOT NULL
        );
    ''')

    # Create course table with a foreign key reference to professor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS course (
            course_name VARCHAR(255) NOT NULL,
            semester INTEGER,
            credits INTEGER,
            faculty_id INTEGER,
            PRIMARY KEY (course_name, semester),
            FOREIGN KEY (faculty_id) REFERENCES professor(faculty_id)
        );
    ''')

    # Create session table with number, start, end, date, and foreign keys to course
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS session (
            number INTEGER,
            start TIME,
            end TIME,
            date DATE,
            course_name VARCHAR(255),
            semester INTEGER,
            PRIMARY KEY (course_name, semester, number),
            FOREIGN KEY (course_name, semester) REFERENCES course(course_name, semester)
        );
    ''')


    # Create attendance table with foreign keys to session and a student_id column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            session_course_name VARCHAR(255) NOT NULL,
            session_semester INTEGER NOT NULL,
            session_number INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            PRIMARY KEY (session_course_name, session_semester, session_number, student_id),
            FOREIGN KEY (session_course_name, session_semester, session_number) REFERENCES session(course_name, semester, number),
            FOREIGN KEY (student_id) REFERENCES student(student_id)
        );
    ''')

    # Create table for attendance codes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance_code (
            course_name VARCHAR(255) NOT NULL,
            course_semester INTEGER NOT NULL,
            session_number INTEGER NOT NULL,
            code VARCHAR(6) NOT NULL,
            created_at DATETIME NOT NULL,
            active BOOLEAN NOT NULL DEFAULT TRUE,
            PRIMARY KEY (course_name, course_semester, session_number, code),
            FOREIGN KEY (course_name, course_semester, session_number) REFERENCES session(course_name, semester, number)
        );
    ''')


    conn.commit()

def insert_data(conn):
    cursor = conn.cursor()

    # Insert data into student table
   
    cursor.execute("INSERT INTO student (student_id, f_name, l_name, student_email) VALUES (1, 'Laura', 'Cuellar', 'laura.cuellar@student.com');")
    cursor.execute("INSERT INTO student (student_id, f_name, l_name, student_email) VALUES (2, 'Isabel', 'De Valenzuela', 'isabel.devalenzuela@student.com');")
    cursor.execute("INSERT INTO student (student_id, f_name, l_name, student_email) VALUES (3, 'Anna', 'Payne', 'anna.payne@student.com');")
    cursor.execute("INSERT INTO student (student_id, f_name, l_name, student_email) VALUES (4, 'Daniel', 'Rosel', 'daniel.rosel@student.com');")
    cursor.execute("INSERT INTO student (student_id, f_name, l_name, student_email) VALUES (5, 'Zaid', 'Saheb', 'zaid.saheb@student.com');")
    cursor.execute("INSERT INTO student (student_id, f_name, l_name, student_email) VALUES (6, 'Sofia', 'Vitorica', 'sofia.vitorica@student.com');")
    cursor.execute("INSERT INTO student (student_id, f_name, l_name, student_email) VALUES (7, 'Tomas', 'Sanchez', 'tomas.sanchez@student.com');")
    cursor.execute("INSERT INTO student (student_id, f_name, l_name, student_email) VALUES (8, 'Kye', 'Electriciteh', 'kye.electriciteh@student.com');")
    cursor.execute("INSERT INTO student (student_id, f_name, l_name, student_email) VALUES (9, 'Sammy', 'Lawy', 'sammy.lawy@student.com');")
    cursor.execute("INSERT INTO student (student_id, f_name, l_name, student_email) VALUES (10, 'Sky', 'Rowaldsky', 'sky.rowaldsky@student.com');")

    conn.commit()

    # Insert data into professor table
    cursor.execute("INSERT INTO professor (faculty_id, f_name, l_name, faculty_email) VALUES (1, 'Eduardo', 'Rodriguez', 'eduardo.rodriguez@professor.com');")
    cursor.execute("INSERT INTO professor (faculty_id, f_name, l_name, faculty_email) VALUES (2, 'Harry', 'Styles', 'harry.styles@professor.com');")
    cursor.execute("INSERT INTO professor (faculty_id, f_name, l_name, faculty_email) VALUES (3, 'Bad', 'Bunny', 'bad.bunny@professor.com');")
    cursor.execute("INSERT INTO professor (faculty_id, f_name, l_name, faculty_email) VALUES (4, 'Taylor', 'Swift', 'taylor.swift@professor.com');")
    cursor.execute("INSERT INTO professor (faculty_id, f_name, l_name, faculty_email) VALUES (5, 'Selena', 'Gomez', 'selena.gomez@professor.com');")
    cursor.execute("INSERT INTO professor (faculty_id, f_name, l_name, faculty_email) VALUES (6, 'Gregorio', 'Maranon', 'gregorio.maranon@professor.com');")

    conn.commit()

    # Insert data into course table
    cursor.execute("INSERT INTO course (course_name, semester, credits, faculty_id) VALUES ('Rock Picking', 2, 3, 1);")
    cursor.execute("INSERT INTO course (course_name, semester, credits, faculty_id) VALUES ('Income Management', 2, 3, 2);")
    cursor.execute("INSERT INTO course (course_name, semester, credits, faculty_id) VALUES ('How to Stand Your Roomate', 2, 1, 3);")
    cursor.execute("INSERT INTO course (course_name, semester, credits, faculty_id) VALUES ('Business Management', 1, 6, 4);")
    cursor.execute("INSERT INTO course (course_name, semester, credits, faculty_id) VALUES ('Math for Dummies', 1, 6, 5);")
    cursor.execute("INSERT INTO course (course_name, semester, credits, faculty_id) VALUES ('Ethics of AI', 2, 6, 4);")
    cursor.execute("INSERT INTO course (course_name, semester, credits, faculty_id) VALUES ('Communication Techniques', 1, 3, 2);")
    cursor.execute("INSERT INTO course (course_name, semester, credits, faculty_id) VALUES ('Dream Big, Try Low', 2, 6, 6);")
    cursor.execute("INSERT INTO course (course_name, semester, credits, faculty_id) VALUES ('Discrete Math', 1, 6, 2);")

    conn.commit()

    # Insert data into session table
    # Rock picking class
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (1, '09:00:00', '11:00:00', '2024-01-08', 'Rock Picking', 2);")
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (2, '09:00:00', '11:00:00', '2024-01-15', 'Rock Picking', 2);")
    # Income Management class
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (1, '11:00:00', '13:00:00', '2024-01-08', 'Income Management', 2);")
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (2, '11:00:00', '13:00:00', '2024-01-15', 'Income Management', 2);")
    # Roommate class
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (1, '09:00:00', '11:00:00', '2024-01-09', 'How to Stand Your Roomate', 2);")
    # Business class
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (1, '09:00:00', '11:00:00', '2023-09-11', 'Business Management', 1);")
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (2, '09:00:00', '11:00:00', '2023-10-11', 'Business Management', 1);")
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (3, '09:00:00', '11:00:00', '2023-11-11', 'Business Management', 1);")
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (4, '09:00:00', '11:00:00', '2023-12-11', 'Business Management', 1);")
    # Math for Dummies
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (1, '10:00:00', '12:00:00', '2023-10-2', 'Math for Dummies', 1);")
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (2, '10:00:00', '12:00:00', '2023-11-6', 'Math for Dummies', 1);")
    # Ethics of AI
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (1, '15:00:00', '17:00:00', '2024-02-19', 'Ethics of AI', 2);")
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (2, '15:00:00', '17:00:00', '2024-04-15', 'Ethics of AI', 2);")
    # Communication Techniques
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (1, '10:00:00', '12:00:00', '2024-02-02', 'Communication Techniques', 1);")
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (2, '10:00:00', '12:00:00', '2024-03-13', 'Communication Techniques', 1);")
    # Dream Big class
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (1, '15:00:00', '17:00:00', '2024-02-20', 'Dream Big, Try Low', 2);")
    # Discrete Math class
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (1, '08:00:00', '10:00:00', '2023-09-08', 'Discrete Math', 1);")
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (2, '08:00:00', '10:00:00', '2023-10-25', 'Discrete Math', 1);")
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (3, '08:00:00', '10:00:00', '2023-11-30', 'Discrete Math', 1);")
    cursor.execute("INSERT INTO session (number, start, end, date, course_name, semester) VALUES (4, '08:00:00', '10:00:00', '2023-12-17', 'Discrete Math', 1);")

    conn.commit()

def main():
    # Connect to the SQLite database (create one if it doesn't exist)
    #conn = sqlite3.connect('checked_DB.db')

    host='dockerlab.westeurope.cloudapp.azure.com'
    username='CC_8'
    password='s8SqfUTpyG7fWRkVpb75BnKbJl-ew5u6J2SZx7vfK48'
    database='CC_8'

    conn = mysql.connector.connect(user=username, password=password,
                                    host=host, database=database)


    # Call functions to create tables and insert data
    create_tables(conn)
    insert_data(conn)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
