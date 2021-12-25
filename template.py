"""
@author: Jim
"""

# Import statements
from typing import ItemsView
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUiType

import sqlite3

from time import sleep
import sys, os
from os import path, stat_result

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


FORM_CLASS,_=loadUiType(resource_path("main.ui"))

class Main(QMainWindow, FORM_CLASS):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)
        self.handle_buttons()
        self.get_data_ScheduleSessionTab()
        self.get_data_RegistrationTab()
        self.calendarDateChanged()
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.Get_CurrentWeek()
        self.getData_completeCourseTab()
        self.courses_comboBox.currentIndexChanged.connect(self.getDatesByCourse)
        self.dateCourse_comboBox.currentIndexChanged.connect(self.getAllAttendants_completeScreen)
        self.facilitators_comboBox_2.currentIndexChanged.connect(self.showCouresByFacilitator)
        self.spin.setValue(self.Get_CurrentWeek())
        self.resourcePlanningByWeek()
        self.spin.valueChanged.connect(self.resourcePlanningByWeek)
        self.header_resize()
 

        


    def handle_buttons(self):
        self.add_btn.clicked.connect(self.add)
        self.clear_btn.clicked.connect(self.clearScheduleTable)
        self.addFac_button.clicked.connect(self.addFacilitator)
        self.addCourse_button.clicked.connect(self.addCourse)
        self.addStudent_button.clicked.connect(self.addStudent)
        self.assignCourseToFac_button.clicked.connect(self.assignCourseToFacilitator)
        self.listPercentCompleted_button.clicked.connect(self.listStudentsByPercentCompleted)
        self.listStudentsByScheduled_Button.clicked.connect(self.listStudentsByScheduled)
        self.listStudentsByNotScheduled_Button.clicked.connect(self.listStudentsByNotScheduled)
        self.listStudentsByDidNotAttend_Button.clicked.connect(self.listStudentsByDidNotAttend)
        self.completeSession.clicked.connect(self.completeSessionFunction)

    def header_resize(self):
        header = self.listStudentsByDidNotAttend_tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header1 = self.tableSchedule.horizontalHeader()       
        header1.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header1.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header1.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)  
        header2 = self.resourcePlanningByWeek_tableWidget.horizontalHeader()       
        header2.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header2.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)  

    def Get_CurrentWeek(self):
        time = QDate.currentDate()
        t = time.weekNumber()
        return t[0]

    def clearScheduleTable(self):
        self.tableSchedule.setRowCount(0)

    def calendarDateChanged(self):
        # Extract selected date from calendarWidget
        dateselected = self.calendarWidget.selectedDate()
        date_in_string = str(dateselected.toPyDate())
        
        # Connect to database
        db=sqlite3.connect(resource_path("onboard.db"))
        cursor=db.cursor()
        
        # Get the course schedule on that date from the database
        call_by_date=''' SELECT c.name,f.name,s.date_schedule from session s join course c on c.id=s.course_id join facilitator f on f.id = s.facilitator_id WHERE strftime("%Y-%m-%d",s.date_schedule) = ? '''
        result=cursor.execute(call_by_date,(dateselected.toPyDate().strftime("%Y-%m-%d"),))

        # Display the course schedule in the table
        self.tableSchedule.setRowCount(0) #Clear table  first
        self.tableSchedule.setRowCount(50)
        tablerow = 0
        for r in result:
            self.tableSchedule.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(r[0]))
            self.tableSchedule.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(r[1]))
            self.tableSchedule.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(r[2]))
            tablerow+=1
        
    def get_data_ScheduleSessionTab(self):
        
        # Connect to Sqlite3 database to fill GUI table with data.
        db=sqlite3.connect(resource_path("onboard.db"))
        cursor=db.cursor()
        
        facilitators_query=''' SELECT name from facilitator '''
        courses_query=''' SELECT name from course '''
        students_query=''' SELECT name from student '''
        self.facilitators_comboBox.clear()
        self.courses_listWidget.clear()
        self.students_listWidget.clear()
        # Get all facilitators from database
        result_facilitators = cursor.execute(facilitators_query).fetchall()
        # Add facilitators to "facilitator" comboBox in UI
        for i in result_facilitators:
            self.facilitators_comboBox.addItem(str(i[0]))
        
        # Get all courses from database
        result_courses = cursor.execute(courses_query).fetchall()
        # Add courses to "courses" listWidget in UI
        for i in result_courses:
            self.courses_listWidget.addItem(str(i[0]))
            
        # Get all students from database
        result_students = cursor.execute(students_query).fetchall()
        # Add students to "students" listWidget in UI
        for i in result_students:
            self.students_listWidget.addItem(str(i[0]))
            
        # Close connection with database
        cursor.close()

    def get_data_RegistrationTab(self):
        # Connect to Sqlite3 database to fill GUI with data.
        db = sqlite3.connect(resource_path("onboard.db"))
        cursor = db.cursor()
        self.facilitators_comboBox_2.clear()
        self.facilitator_listWidget.clear()
        # Display facilitators in combo box
        facilitators_query = ''' SELECT name from facilitator '''
        # Get all facilitators from database
        result_facilitators = cursor.execute(facilitators_query).fetchall()
        # Add facilitators to "facilitator" comboBox in UI
        for i in result_facilitators:
            self.facilitators_comboBox_2.addItem(str(i[0]))
            self.facilitator_listWidget.addItem(str(i[0]))
            
        self.showCouresByFacilitator() # Show courses for the default facilitator
        
        # Get all courses from database
        self.courses_listWidget_2.clear()
        courses_query = ''' SELECT name from course '''
        result_courses = cursor.execute(courses_query).fetchall()
        # Add courses to "courses" listWidget in UI
        for i in result_courses:
            self.courses_listWidget_2.addItem(str(i[0]))
            
    def showCouresByFacilitator(self):    
        # Get selected facilitator from comboBox
        selected_fac = str(self.facilitators_comboBox_2.currentText())
        
        # Connect to Sqlite3 database to get the facilitator ID
        db = sqlite3.connect(resource_path("onboard.db"))
        cursor = db.cursor()
        # Get facilitator ID
        facilitator_id_query = ''' SELECT id from facilitator WHERE name=? '''
        cursor.execute(facilitator_id_query, (selected_fac,))
        try:    
            fac_id = int(cursor.fetchone()[0])
        

            # Get courses with this facilitator ID from the course_facilitator table
            courses_by_facilitator = ''' SELECT f.name, c.name from session s  join course c on c.id=s.course_id join facilitator f on f.id = s.facilitator_id WHERE  f.id  = ? '''
            result = cursor.execute(courses_by_facilitator,
                                    (fac_id,))

            # Display the facilitator's courses in the table
            self.coursesByFac_tableWidget.setRowCount(0)  # Clear table  first
            self.coursesByFac_tableWidget.setRowCount(50)
            tablerow = 0
            for r in result:
                self.coursesByFac_tableWidget.setItem(
                    tablerow, 0, QtWidgets.QTableWidgetItem(r[0]))
                self.coursesByFac_tableWidget.setItem(
                    tablerow, 1, QtWidgets.QTableWidgetItem(r[1]))
                tablerow += 1
        except:
            print("no fac in db")   
    def assignCourseToFacilitator(self):
        # Get selected facilitator from listWidget
        selected_fac = self.facilitator_listWidget.selectedItems()[0].text()
        # Get selected course from listWidget
        selected_course = self.courses_listWidget_2.selectedItems()[0].text()
        
        # Connect to Sqlite3 database
        db = sqlite3.connect(resource_path("onboard.db"))
        cursor = db.cursor()
        
        # Get the ID of the selected facilitator from "facilitatior" table
        facilitator_id_query = ''' SELECT id from facilitator WHERE name=? '''
        cursor.execute(facilitator_id_query, (selected_fac,))
        fac_id = int(cursor.fetchone()[0])
        cursor = db.cursor()

        # Get the ID of the selected course from "course" table
        course_id_query = ''' SELECT id from course WHERE name=? '''
        cursor.execute(course_id_query, (selected_course,))
        course_id = int(cursor.fetchone()[0])
        
        # Inserting row into "course_facilitator" table
        row = (course_id, fac_id)
        command = ''' INSERT INTO session (course_id,facilitator_id) VALUES (?,?)'''
        cursor.execute(command, row)
        
        db.commit()
        
        # Once adding to database is complete, display confirmation message
        msgBox = QMessageBox()
        msgBox.setText("Added to database")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        # Once OK is selected, reset all values
        if returnValue == QMessageBox.Ok:
            self.facilitator_listWidget.setCurrentRow(0)
            self.courses_listWidget_2.setCurrentRow(0)

    def add(self):
        
        # Connect to Sqlite3 database and fill GUI table with data.
        db=sqlite3.connect(resource_path("onboard.db"))
        cursor=db.cursor()
        
        # Get selected facilitator, course, and students/attendees from the UI
        selected_facilitator=self.facilitators_comboBox.currentText()
        selected_course = self.courses_listWidget.selectedItems()[0].text()
        selected_students = self.students_listWidget.selectedItems()
        
        # Extract date & week information from selected date 
        selected_dateTime = self.dateTimeEdit.dateTime()
        selected_schedule = selected_dateTime.toString("yyyy-MM-dd hh:mm:ss")
        week_ = selected_dateTime.toString("yyyyMd")
        status_ = str("scheduled")
        q = QDate.fromString(week_, 'yyyyMd')
        week = q.weekNumber()[0]

        # Get the ID of the selected facilitator from "facilitatior" table
        facilitator_id_query = ''' SELECT id from facilitator WHERE name=? '''
        cursor.execute(facilitator_id_query, (selected_facilitator,))
        fac_id=int(cursor.fetchone()[0])
        cursor=db.cursor()
        
        # Get the ID of the selected course from "course" table
        course_id_query=''' SELECT id from course WHERE name=? '''
        cursor.execute(course_id_query,(selected_course,))
        course_id=int(cursor.fetchone()[0])
    
        # Get the IDs of the selected students from "student" database
        student_names = []
        for student in selected_students:
            student_names.append(student.text())
        cursor.execute('SELECT id FROM student WHERE name IN (%s)' %','.join('?'*len(student_names)), tuple(student_names))
        student_ids=cursor.fetchall()

        # Inserting row into "course_facilitator" table 
        row=(course_id,fac_id,selected_schedule,week)
        command=''' INSERT INTO session (course_id,facilitator_id,date_schedule, week) VALUES (?,?,?,?)'''
        cursor.execute(command,row)
        sessionid = cursor.lastrowid
        
        # Insert row into "course_facilitator_student"
        for i in student_ids:
            row2 = (sessionid,i[0], status_)
            command=''' INSERT INTO session_student (session_id, student_id, status) VALUES (?,?,?)'''
            cursor.execute(command,row2)
        
        db.commit() 
        
        # Once adding to database is complete, display confirmation message
        msgBox = QMessageBox()
        msgBox.setText("Added to database")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        # Once OK is selected, reset all values
        if returnValue == QMessageBox.Ok:
            self.courses_listWidget.clearSelection()
            self.students_listWidget.clearSelection()
            self.facilitators_comboBox.setCurrentIndex(0)
            self.calendarDateChanged()

      
    def addFacilitator(self):
        # Get the name of the facilitator 
        facilitator = self.facilitator_lineEdit.text()
        
        # Connect to Sqlite3 database 
        db = sqlite3.connect(resource_path("onboard.db"))
        cursor = db.cursor()
        
        # Inserting row into "facilitator" table
        row = (facilitator,)
        command = ''' INSERT INTO facilitator (name) VALUES (?)'''
        cursor.execute(command, row)
        
        db.commit()
        
        # Once adding to database is complete, display confirmation message
        msgBox = QMessageBox()
        msgBox.setText("Added to database")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        # Once OK is selected, reset all values
        if returnValue == QMessageBox.Ok:
            self.facilitator_lineEdit.setText("")
            self.refresh()
            
    def addCourse(self):
        # Get the name of the course
        course = self.course_lineEdit.text()

        # Connect to Sqlite3 database
        db = sqlite3.connect(resource_path("onboard.db"))
        cursor = db.cursor()

        # Inserting row into "course" table
        row = (course,)
        command = ''' INSERT INTO course (name) VALUES (?)'''
        cursor.execute(command, row)

        db.commit()

        # Once adding to database is complete, display confirmation message
        msgBox = QMessageBox()
        msgBox.setText("Added to database")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        # Once OK is selected, reset all values
        if returnValue == QMessageBox.Ok:
            self.course_lineEdit.setText("")

        self.refresh()
    
    def addStudent(self):
        # Get the name of the student
        student = self.student_lineEdit.text()

        # Connect to Sqlite3 database
        db = sqlite3.connect(resource_path("onboard.db"))
        cursor = db.cursor()

        # Inserting row into "student" table
        row = (student,)
        command = ''' INSERT INTO student (name) VALUES (?)'''
        cursor.execute(command, row)

        db.commit()

        # Once adding to database is complete, display confirmation message
        msgBox = QMessageBox()
        msgBox.setText("Added to database")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        # Once OK is selected, reset all values
        if returnValue == QMessageBox.Ok:
            self.student_lineEdit.setText("")
    	
	self.refresh()

        
    def listStudentsByPercentCompleted(self):
        # Get % of completed courses from database
        query = '''SELECT s.name, 
            (CAST(COUNT(CASE WHEN ss.status = 'completed' THEN 1 END) as REAL) / COUNT(*))* 100  AS complete_percentage
            FROM session_student ss join student s on s.id = ss.student_id
            GROUP BY student_id;'''
            
        # Connect to database
        db = sqlite3.connect(resource_path("onboard.db"))
        cursor = db.cursor()
        
        # Execute the query
        result=cursor.execute(query)
        
        # Display the results in the table
        self.percentCompleted_tableWidget.setRowCount(0)  # Clear table  first
        self.percentCompleted_tableWidget.setRowCount(50)
        tablerow = 0
        for r in result:
            print(r)
            self.percentCompleted_tableWidget.setItem(
                tablerow, 0, QtWidgets.QTableWidgetItem(str(r[0])))
            self.percentCompleted_tableWidget.setItem(
                tablerow, 1, QtWidgets.QTableWidgetItem(str(r[1])))
            tablerow += 1
        
    def listStudentsByScheduled(self):
        # Get each student's scheduled courses from database
        query = '''SELECT DISTINCT s.name,  c.name  
            FROM session_student ss, session ses join course c on c.id = ses.course_id  join student s on s.id = ss.student_id
			WHERE ss.status="scheduled"
            ORDER BY s.name;'''
   
        # Connect to database
        db = sqlite3.connect(resource_path("onboard.db"))
        cursor = db.cursor()

        # Execute the query
        result = cursor.execute(query)
        
        # Display the results in the table
        self.listStudentsByScheduled_tableWidget.setRowCount(0)  # Clear table  first
        self.listStudentsByScheduled_tableWidget.setRowCount(50)
        tablerow = 0
        for r in result:
            self.listStudentsByScheduled_tableWidget.setItem(
                tablerow, 0, QtWidgets.QTableWidgetItem(str(r[0])))
            self.listStudentsByScheduled_tableWidget.setItem(
                tablerow, 1, QtWidgets.QTableWidgetItem(str(r[1])))
            tablerow += 1

    def listStudentsByNotScheduled(self):
        # Get courses for each student that they have not scheduled
        query = '''SELECT DISTINCT s.name,  c.name  
            FROM student s, course c
			WHERE c.id not in (SELECT ses.course_id FROM session ses join session_student ss on ses.session_id=ss.session_id WHERE ss.student_id = s.id )
			ORDER BY s.name;'''
   
        # Connect to database
        db = sqlite3.connect(resource_path("onboard.db"))
        cursor = db.cursor()

        # Execute the query
        result = cursor.execute(query)

        # Display the results in the table
        self.listStudentsByNotScheduled_tableWidget.setRowCount(0)  # Clear table  first
        self.listStudentsByNotScheduled_tableWidget.setRowCount(50)
        tablerow = 0
        for r in result:
            self.listStudentsByNotScheduled_tableWidget.setItem(
                tablerow, 0, QtWidgets.QTableWidgetItem(str(r[0])))
            self.listStudentsByNotScheduled_tableWidget.setItem(
                tablerow, 1, QtWidgets.QTableWidgetItem(str(r[1])))
            tablerow += 1
            
    def listStudentsByDidNotAttend(self):
        # Get each student's DNA courses from database
        query = ''' SELECT  st.name, c.name from session_student ss join student st on ss.student_id=st.id join session ses on ses.session_id=ss.session_id join course c on c.id=ses.course_id join facilitator f on f.id = ses.facilitator_id WHERE ss.status="DNA" ORDER BY st.name'''
        
        # Connect to database
        db = sqlite3.connect(resource_path("onboard.db"))
        cursor = db.cursor()

        # Execute the query
        result = cursor.execute(query)

        # Display the results in the table
        #self.listStudentsByDidNotAttend_tableWidget.setColumnWidth(0,250)
        #self.listStudentsByDidNotAttend_tableWidget.setColumnWidth(1,500)
        self.listStudentsByDidNotAttend_tableWidget.setRowCount(0)  
        # Clear table  first
        self.listStudentsByDidNotAttend_tableWidget.setRowCount(50)
        tablerow = 0
        for r in result:
            self.listStudentsByDidNotAttend_tableWidget.setItem(
                tablerow, 0, QtWidgets.QTableWidgetItem(str(r[0])))
            self.listStudentsByDidNotAttend_tableWidget.setItem(
                tablerow, 1, QtWidgets.QTableWidgetItem(str(r[1])))
            tablerow += 1

    
    def resourcePlanningByWeek(self):
        
         # Connect to Sqlite3 database to get the facilitator ID
        db = sqlite3.connect(resource_path("onboard.db"))
        cursor = db.cursor()

        selected_week = self.spin.value()

        # Get courses and facilitators
        query = ''' SELECT c.name, f.name, st.name from session_student ss join student st on ss.student_id=st.id join session ses on ses.session_id=ss.session_id join course c on c.id=ses.course_id join facilitator f on f.id = ses.facilitator_id WHERE ses.date_schedule is not null AND ses.week = ?'''
        
        
        result = cursor.execute(query, (selected_week,))

        # Display the facilitator's courses in the table
        self.resourcePlanningByWeek_tableWidget.setRowCount(0)  # Clear table  first
        self.resourcePlanningByWeek_tableWidget.setRowCount(100)
        tablerow = 0
        for r in result:
            self.resourcePlanningByWeek_tableWidget.setItem(
                tablerow, 0, QtWidgets.QTableWidgetItem(r[0]))
            self.resourcePlanningByWeek_tableWidget.setItem(
                tablerow, 1, QtWidgets.QTableWidgetItem(r[1]))
            self.resourcePlanningByWeek_tableWidget.setItem(
                tablerow, 2, QtWidgets.QTableWidgetItem(r[2]))
            
            tablerow += 1
            
    def refresh(self):
        self.get_data_ScheduleSessionTab()
        self.get_data_RegistrationTab()

    def getData_completeCourseTab(self):
        # Connect to Sqlite3 database to fill GUI with data.
        db = sqlite3.connect(resource_path("onboard.db"))
        cursor = db.cursor()
        
        #Get courses from database
        courses_query = ''' SELECT name from course '''
        result_courses = cursor.execute(courses_query).fetchall()
        # Add courses to "courses" comboBox in UI
        for i in result_courses:
            self.courses_comboBox.addItem(str(i[0]))
            
        # Get dates of default course    
        self.getDatesByCourse()
        cursor.close()
        
        self.getAllAttendants_completeScreen()
            
    def getDatesByCourse(self):
        # Clear comboBox before adding
        self.dateCourse_comboBox.clear()
        
        # Connect to Sqlite3 database to fill GUI with data.
        db = sqlite3.connect(resource_path("onboard.db"))
        cursor = db.cursor()
        
        # Get selected course from UI
        selected_course = self.courses_comboBox.currentText();
        
        # Get dates by course
        dates_by_courses = ''' SELECT s.date_schedule from session s  join course c on c.id=s.course_id WHERE c.name=? '''
    
        result = cursor.execute(dates_by_courses,
                                (selected_course,))

        for r in result:
            if r[0] is not None:
                self.dateCourse_comboBox.addItem(r[0])
            
        cursor.close()
        
        self.getAllAttendants_completeScreen()
        
    def getAllAttendants_completeScreen(self):
        # Clear listWidget before adding
        self.completedAttendents_listWidget.clear()
        self.dnaAttendants_listWidget.clear()

        # Connect to Sqlite3 database to fill GUI with data.
        db = sqlite3.connect(resource_path("onboard.db"))
        cursor = db.cursor()

          # Get selected course from UI
        selected_course = self.courses_comboBox.currentText()

        # Get selected date from UI
        selected_date = self.dateCourse_comboBox.currentText()

        # Get session_id of selected course
        session_id_query = ''' SELECT s.session_id from session s  join course c on c.id=s.course_id WHERE c.name=? AND s.date_schedule=? '''
        result_session_id = cursor.execute(session_id_query,
                                           (selected_course, selected_date,)).fetchone()

        if result_session_id is not None:
            result_session_id=result_session_id[0]        

        # Get list of all students
        students = ''' SELECT name from student s join session_student ss on s.id = ss.student_id WHERE ss.session_id = ?; '''
        result = cursor.execute(students, (result_session_id,)).fetchall()

        for r in result:
            self.completedAttendents_listWidget.addItem(r[0])
            self.dnaAttendants_listWidget.addItem(r[0])

    def completeSessionFunction(self):
        # Connect to Sqlite3 database to fill GUI with data.
        db = sqlite3.connect(resource_path("onboard.db"))
        cursor = db.cursor()

        # Get selected course from UI
        selected_course = self.courses_comboBox.currentText()

        # Get selected date from UI
        selected_date = self.dateCourse_comboBox.currentText()

        # Get session_id of selected course
        session_id_query = ''' SELECT s.session_id from session s  join course c on c.id=s.course_id WHERE c.name=? AND s.date_schedule=? '''
        result_session_id = cursor.execute(session_id_query,
                                           (selected_course, selected_date,)).fetchone()[0]
        
        # Insert/update into this session the students that attended
        selected_students_to_complete = self.completedAttendents_listWidget.selectedItems()
        for student in selected_students_to_complete:
            student_name = student.text()
            # Get student_id of this student
            students_query = ''' SELECT id from student s WHERE name = ? '''
            result_student_id = cursor.execute(students_query, (student_name,)).fetchone()[0]
            # Insert student as completed this session
            complete_query_insert = '''INSERT OR IGNORE INTO session_student (session_id, student_id, status) VALUES (?, ?, 'completed')'''
            cursor.execute(complete_query_insert, (result_session_id, result_student_id, ))
            complete_query_update = ''' UPDATE session_student SET status = "completed" WHERE session_id = ? AND student_id = ?'''
            cursor.execute(complete_query_update,
                           (result_session_id, result_student_id, ))
           
        db.commit()

        # Insert/update into this session the students that did not attend
        selected_students_to_complete = self.dnaAttendants_listWidget.selectedItems()
        for student in selected_students_to_complete:
            student_name = student.text()
            # Get student_id of this student
            students_query = ''' SELECT id from student s WHERE name = ? '''
            result_student_id = cursor.execute(
                students_query, (student_name,)).fetchone()[0]
            # Insert student as completed this session
            complete_query_insert = '''INSERT OR IGNORE INTO session_student (session_id, student_id, status) VALUES (?, ?, 'DNA')'''
            cursor.execute(complete_query_insert,
                           (result_session_id, result_student_id, ))
            complete_query_update = ''' UPDATE session_student SET status = "DNA" WHERE session_id = ? AND student_id = ?'''
            cursor.execute(complete_query_update,
                           (result_session_id, result_student_id, ))

        db.commit()
        
        # Once adding to database is complete, display confirmation message
        msgBox = QMessageBox()
        msgBox.setText("Added to database")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        # Once OK is selected, reset all values
        if returnValue == QMessageBox.Ok:
            self.completedAttendents_listWidget.clearSelection()
            self.dnaAttendants_listWidget.clearSelection()

        
def main():
    
    app=QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()
    

if __name__=='__main__':
    main()    
