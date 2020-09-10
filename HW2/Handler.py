#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 19:09:33 2020

@author: huangkevin
"""


# 學生有 學號(code) 姓名(name)
import sqlite3, sys
DB_NAME = 'db.sqlite' # 定義全域變數
conn = sqlite3.connect('/Users/huangkevin/Desktop/'+DB_NAME+'.db')
cursor = conn.cursor()

class Grade(object):
    
    def __init__(self, semester, chinese, english, mathematics, student):
        self.semester = semester
        self.chinese = chinese
        self.english = english
        self.mathematics = mathematics
        self.student = student
        
class Student(object):
    
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.grades = []
    
        
class StudentHandler(object):
    def __init__(self):
        self.students = []
    def showGrades (self):    ##列出成績/可用fetchall()
        allStudents = cursor.execute("SELECT Student.code ,Student.name ,Grade.semester, Grade.chinese, Grade.english, Grade.mathematics \
                             FROM Student LEFT JOIN Grade ON Student.code = Grade.student; ")
        allStu = list(allStudents)
        for row in allStu:
            print("學號: ",row[0],","," 姓名: ", row[1],sep = '')
            print("第",row[2],"學期: ","國文",row[3],"英文",row[4],"數學",row[5])
    def addStudent (self, Code, Name): ##增加學生
        newSt = Student(Code, Name)
        cursor.execute("INSERT INTO Student (code,name) \
                       VALUES (%d, '%s')" %(Code, Name))
        conn.commit()
        self.students.append(newSt)
    def addGrades (self, Code, Semester, Chinese, English, Math): ##增加成績
        ID = cursor.execute("SELECT MAX(id) FROM Grade").fetchone()
        if ID[0] == None :
            cursor.execute("INSERT INTO Grade(id,semester,chinese,english,mathematics,student)\
                       VALUES (%d, %d, %d, %d, %d, %d )" % (1, Semester, Chinese, English, Math, Code))
        else:
            nextID = int(ID[0])+1
            cursor.execute("INSERT INTO Grade(id,semester,chinese,english,mathematics,student)\
                       VALUES (%d, %d, %d, %d, %d, %d )" % (nextID, Semester, Chinese, English, Math, Code))
        conn.commit()
        
    def updateGrade(self, Code, Semester, Chinese, English, Math): ##修改成績
        cursor.execute("UPDATE Grade SET chinese = %d ,english = %d, mathematics = %d WHERE student = %d AND semester = %d" % (Chinese, English, Math, Code, Semester))
        conn.commit()
    def deleteGrade(self, Code, Semester):##刪除成績
        cursor.execute("DELETE FROM Grade WHERE student = %d AND semester = %d" % (Code, Semester))
        conn.commit()
    def quitProgram(self):
        print('已離開程式')
        conn.close()
    

##創Student table       
cursor.execute('CREATE TABLE IF NOT EXISTS Student ('
                    'code  INTEGER PRIMARY KEY,'
                    'name  TEXT)')         
# 成績有 學期(semeste) 國文(chinese) 英文(english) 數學(mathematics) 學生(student) 且 UNIQUE(semester, student)
cursor.execute('CREATE TABLE IF NOT EXISTS Grade ('
    'id INTEGER PRIMARY KEY AUTOINCREMENT,'
    'semester INTEGER,'
    'chinese INTEGER,'
    'english INTEGER,'
    'mathematics INTEGER,'
    'student INTEGER,'
    'FOREIGN KEY(student) REFERENCES Student(code)'
    'UNIQUE(semester, student))')
'''
cursor.execute("INSERT INTO Student (code,name) \
     VALUES (100, 'bwfv' )")

cursor.execute("INSERT INTO Grade (id,semester,chinese,english,mathematics,student) \
      VALUES (101,3,45,49,90,100 )")
'''



conn.commit()


