CREATE TABLE facilitator (
   id INTEGER PRIMARY KEY,
   name VARCHAR(255)
);

CREATE TABLE student (
   id INTEGER PRIMARY KEY,
   name VARCHAR(255)
);

CREATE TABLE course (
   id INTEGER PRIMARY KEY,
   name VARCHAR(255)
);

CREATE TABLE session (
   session_id INTEGER PRIMARY KEY,
   course_id INTEGER,
   facilitator_id INTEGER,
   date_schedule DATETIME
);

CREATE TABLE session_student (
   session_id INTEGER,
   student_id INTEGER,
   status VARCHAR(255)
);

