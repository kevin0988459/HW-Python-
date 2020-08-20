from selenium import webdriver
from time import sleep
import requests
import json
import sqlite3
##登入取得驗證碼
authorityCode = 'CWB-31A42EC1-B9CF-47B8-8997-4439A3C914C1'
##使用 requests 去 GET
apiUrl = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization='+authorityCode
weatherTW = requests.get(apiUrl)
##json
weatherJson = json.loads(weatherTW.text)
city = len(weatherJson["records"]['location'])
##處理json，將值放進list
locationNameList = []



##print to console
for i in range(city):
    print(weatherJson["records"]['location'][i]['locationName'])
    locationNameList.append(weatherJson["records"]['location'][i]['locationName'])
    for y in range(len(weatherJson["records"]['location'][i]['weatherElement'])):
        for x in range(len(weatherJson["records"]['location'][i]['weatherElement'][y]['time'])):
            
            print("start: "+weatherJson["records"]['location'][i]['weatherElement'][y]['time'][x]['startTime'],end=" ")
            
            print("end : "+weatherJson["records"]['location'][i]['weatherElement'][y]['time'][x]['endTime'],end= " ")
            
            print("paramaterName: " + weatherJson["records"]['location'][i]['weatherElement'][y]['time'][x]['parameter']['parameterName'],end=' ')
            if "parameterValue" in weatherJson["records"]['location'][i]['weatherElement'][y]['time'][x]['parameter']:
                print("paramaterValue: " + weatherJson["records"]['location'][i]['weatherElement'][y]['time'][x]['parameter']['parameterValue'])
                
            else:
                print('null')
                


##連接sqlite3資料庫

conn = sqlite3.connect('/Users/huangkevin/Desktop/weather.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS location')
cursor.execute('CREATE TABLE IF NOT EXISTS location('
               'locationName char(5), '
               'startTime char(20), '
               'endTime char(20), '
               'parameterName char(10),'
               'parameterValue char(5))')


##存入資料



for i in range(city):
    for y in range(len(weatherJson["records"]['location'][i]['weatherElement'])):
        for x in range(len(weatherJson["records"]['location'][i]['weatherElement'][y]['time'])):
            values = locationNameList[i]
            startValues = weatherJson["records"]['location'][i]['weatherElement'][y]['time'][x]['startTime']
            endValues = weatherJson["records"]['location'][i]['weatherElement'][y]['time'][x]['endTime']
            pName = weatherJson["records"]['location'][i]['weatherElement'][y]['time'][x]['parameter']['parameterName']
            if  "parameterValue" in weatherJson["records"]['location'][i]['weatherElement'][y]['time'][x]['parameter']:
                pValues = weatherJson["records"]['location'][i]['weatherElement'][y]['time'][x]['parameter']['parameterValue']
            else:
                pValues = "null"
            cursor.execute("INSERT INTO location(locationName, startTime, endTime, parameterName, parameterValue)\
                           VALUES (?,?,?,?,?)" , (values,startValues, endValues,pName,pValues))

conn.commit() 
conn.close()   

    
    
    
    
    
    
    
    





    
    
    
    
    

