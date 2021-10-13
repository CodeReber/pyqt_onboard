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

CREATE TABLE course_facilitator (
   course_id INTEGER,
   facilitator_id INTEGER,
   date_schedule DATETIME
);

CREATE TABLE course_facilitator_student (
   course_id INTEGER,
   student_id INTEGER,
   facilitator_id INTEGER,
   status VARCHAR(255)
);


