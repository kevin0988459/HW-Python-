#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 21:28:48 2020

@author: huangkevin
"""


##未實作exception，輸入重複值導致錯誤 sql unique constraints error，直接刪除db重新開始（Deadlock)
from Handler import StudentHandler

modifyTable = StudentHandler() ##操作物件
executeStatus = True ##執行狀態

com = ['列出成績', '新增學生','新增學生成績', '更新學生成績', '刪除學生成績','離開']
def command(): ## 指令
    for i in range (6):
        print(str(i+1)+'.',com[i])


def modify(): ##操作選擇
    print('')
    command()
    number = input('請選擇功能代號:')
    if number == '1':
        modifyTable.showGrades()
    elif number == '2':
        code = int(input('請輸入學生學號:'))
        name = input('請輸入學生名稱:')
        modifyTable.addStudent(code,name)
        print('------------完成------------')
    elif number == '3':
        code = int(input('請輸入學生學號:'))
        semester = int(input('請輸入學期:'))
        chinese = int(input('請輸入國文成績:'))
        english = int(input('請輸入英文成績:'))
        math = int(input('請輸入數學成績:'))
        modifyTable.addGrades(code,semester,chinese,english,math)
        print('------------完成------------')
    elif number == '4':
        code = int(input('請輸入學生學號:'))
        semester = int(input('請輸入學期:'))
        chinese = int(input('請輸入國文成績:'))
        english = int(input('請輸入英文成績:'))
        math = int(input('請輸入數學成績:'))
        modifyTable.updateGrade(code,semester,chinese,english,math)
        print('------------完成------------')
    elif number == '5':
        code = int(input('請輸入學生學號:'))
        semester = int(input('請輸入學期:'))
        modifyTable.deleteGrade(code,semester)
        print('完成------------------------')
    elif number == '6':
        modifyTable.quitProgram()
        global executeStatus 
        executeStatus = False
    else :
        print('please input 1 - 6')

while (executeStatus): ##執行直到輸入6
    modify()
    









