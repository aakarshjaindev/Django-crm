'''
import mysql.connector
dataBase = mysql.connector.connect(
	host = 'localhost',
	user = 'root',
	passwd = 'password123'
	)


# prepare a cursor object 
cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE IF NOT EXISTS elderco")

print('all done!')



'''

import pymysql

# connect
db = pymysql.connect(
    host="localhost",
    user="root",
    password="password123"
)

cursor = db.cursor()

# create database
cursor.execute("CREATE DATABASE IF NOT EXISTS elderco")

print("all done!")

cursor.close()
db.close()
