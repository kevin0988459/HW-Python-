from selenium import webdriver
from time import sleep
import requests

import json
import sqlite3
##登入取得驗證碼
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver 2')
url = 'https://opendata.cwb.gov.tw/userLogin'
driver.maximize_window()
driver.get(url);
driver.find_element_by_xpath('/html/body/div[1]/div/div/main/div[2]/div/div[2]/div[2]/div/div[4]/div/button').click()
email='zasx722@yahoo.com.tw'
password='kevinlove'
sleep(3)
before_win = driver.window_handles[0]
fb = driver.window_handles[1]
##輸入帳號
driver.switch_to_window(fb)
driver.find_element_by_id('email').send_keys(email)
driver.find_element_by_id('pass').send_keys(password)
driver.find_element_by_name('login').click()
sleep(3)
driver.switch_to_window(before_win)
##點擊並取得驗證碼
driver.find_element_by_xpath('//*[@id="content"]/div/div/main/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/button').click()
sleep(3)
dr = driver.find_element_by_xpath('//*[@id="content"]/div/div/main/div[2]/div/div[2]/div[2]/div/div[1]/div[2]')
authorityCode = dr.text
driver.quit()
##使用 requests 去 GET
apiUrl = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization='+authorityCode
weatherTW = requests.get(apiUrl)
##json
weatherJson = json.loads(weatherTW.text)
city = len(weatherJson["records"]['location'])
##處理json，將值放進list
locationNameList = []




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

    
    
    
    
    
    
    
    





    
    
    
    
    

