-- Professor table
CREATE TABLE Professor (
    professor_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE
);

-- Course table
CREATE TABLE Course (
    name VARCHAR(100) NOT NULL,
    semester VARCHAR(50) NOT NULL,
    professor_id INT,
    PRIMARY KEY (name, semester),
    FOREIGN KEY (professor_id) REFERENCES Professor (professor_id)
);

-- Session table
CREATE TABLE Session (
    course_name VARCHAR(100) NOT NULL,
    course_semester VARCHAR(50) NOT NULL,
    number INT NOT NULL,
    date DATE,
    start TIME,
    end TIME,
    PRIMARY KEY (course_name, course_semester, number),
    FOREIGN KEY (course_name, course_semester) REFERENCES Course (name, semester)
);

-- Student table
CREATE TABLE Student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE
);

-- Attendance table
CREATE TABLE Attendance (
    course_name VARCHAR(100) NOT NULL,
    course_semester VARCHAR(50) NOT NULL,
    session_number INT NOT NULL,
    student_id INT NOT NULL,
    PRIMARY KEY (course_name, course_semester, session_number, student_id),
    FOREIGN KEY (course_name, course_semester, session_number) REFERENCES Session (course_name, course_semester, number),
    FOREIGN KEY (student_id) REFERENCES Student (student_id)
);
