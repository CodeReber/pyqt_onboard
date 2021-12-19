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
CREATE TABLE IF NOT EXISTS "session_student" (
        "student_id"    INTEGER,
        "session_id"    INTEGER,
        "status"        VARCHAR(255),
        PRIMARY KEY("student_id","session_id")
);
CREATE TABLE IF NOT EXISTS "session" (
        "session_id"    INTEGER,
        "course_id"     INTEGER,
        "facilitator_id"        INTEGER,
        "date_schedule" DATETIME,
        "week"  INTEGER,
        PRIMARY KEY("session_id")
);
