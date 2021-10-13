"""
@author: Jim
"""
from typing import ItemsView
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication


from time import sleep
import sys, os

from os import path, stat_result

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

from PyQt5.uic import loadUiType

FORM_CLASS,_=loadUiType(resource_path("main.ui"))

import sqlite3


class Main(QMainWindow, FORM_CLASS):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)
        self.Handel_Buttons()
        self.GET_DATA()
        self.calendarWidget.selectionChanged.connect(self.Calendar_Date)
        self.Get_CurrentWeek()

    def Handel_Buttons(self):
        self.add_btn.clicked.connect(self.ADD)
        self.clear_btn.clicked.connect(self.Clear_Schedule_table)

#Code Here
    def Get_CurrentWeek(self):
        time = QDate.currentDate()
        t = time.weekNumber()

    
    def Clear_Schedule_table(self):
        self.tableSchedule.setRowCount(0)

    def Calendar_Date(self):
        dateselected = self.calendarWidget.selectedDate()
        date_in_string = str(dateselected.toPyDate())
        #print(type(dateselected.toPyDate()))
        self.label_17.setText("Date Is : " + date_in_string)
        db=sqlite3.connect(resource_path("onboard.db"))
        cursor=db.cursor()
        call_by_date=''' SELECT c.name,f.name,cf.date_schedule from course_facilitator cf join course c on c.id=cf.course_id join facilitator f on f.id = cf.facilitator_id WHERE strftime("%Y-%m-%d",cf.date_schedule) = ? '''
        result=cursor.execute(call_by_date,(dateselected.toPyDate().strftime("%Y-%m-%d"),))

        self.tableSchedule.setRowCount(50)
        tablerow = 0
        for r in result:
            self.tableSchedule.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(r[0]))
            self.tableSchedule.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(r[1]))
            self.tableSchedule.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(r[2]))
            tablerow+=1
        #print(dateselected.toPyDate().strftime("%Y-%m-%d"))
        #r2=result.fetchall()
        #print(r2)

    def GET_DATA(self):
        
        # Connect to Sqlite3 database ad fill GUI table with data.
        db=sqlite3.connect(resource_path("onboard.db"))
        cursor1=db.cursor()
        cursor2=db.cursor()
        cursor3=db.cursor()

        
        fac1=''' SELECT name from facilitator '''
        course=''' SELECT name from course '''
        addendant=''' SELECT name from student '''
        
        result_fac=cursor1.execute(fac1)
        result_course=cursor2.execute(course)
        result_addendant=cursor3.execute(addendant)

        r2=result_fac.fetchall()
        r3=result_course.fetchall()
        r4=result_addendant.fetchall()
        
        # self.table.setRowCount(0) 
        
        # for row_number, row_data in enumerate(result):
        #     self.table.insertRow(row_number)
        #     for column_number, data in enumerate(row_data):
        #         self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        for i in r2:
            self.comboBox.addItem(str(i[0]))

        for i in r3:
            self.listWidget.addItem(str(i[0]))

        for i in r4:
            self.listWidget_2.addItem(str(i[0]))

    def ADD(self):

        db=sqlite3.connect("onboard.db")
        cursor=db.cursor()
        
        fac_name_=self.comboBox.currentText()
        course_name_=self.listWidget.selectedItems()[0].text()
        student_=self.listWidget_2.selectedItems()
        scheduled_=self.dateTimeEdit.dateTime()
        sched=scheduled_.toString("yyyy-MM-dd hh:mm:ss")
        week_=scheduled_.toString("yyyyMd")
        status_=str("scheduled")
        q = QDate.fromString(week_, 'yyyyMd')
        q1 = q.weekNumber()
        print(q1[0])
       # print(week_)


        fac_id_query=''' SELECT id from facilitator WHERE name=? '''
        cursor.execute(fac_id_query,(fac_name_,))
        fac_id=int(cursor.fetchone()[0])
        cursor=db.cursor()
        
        course_id_query=''' SELECT id from course WHERE name=? '''
        cursor.execute(course_id_query,(course_name_,))
        course_id=int(cursor.fetchone()[0])
    
        student_names=[]
        for student in student_:
            student_names.append(student.text())
      
        cursor.execute('SELECT id FROM student WHERE name IN (%s)' %','.join('?'*len(student_names)), tuple(student_names))
    
        student_ids=cursor.fetchall()
        #print(student_ids)

        row=(course_id,fac_id,sched)
        

        command=''' INSERT INTO course_facilitator (course_id,facilitator_id,date_schedule) VALUES (?,?,?)'''
                
        cursor.execute(command,row)
        for i in student_ids:
            row2=(course_id,i[0],fac_id,status_)
            command=''' INSERT INTO course_facilitator_student (course_id,student_id,facilitator_id,status) VALUES (?,?,?,?)'''

            cursor.execute(command,row2)
        
        db.commit()        


def main():
    
    app=QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()
    

if __name__=='__main__':
    main()    
