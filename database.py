import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Payel12@",
    database="pharmacy_db"
)

cursor = conn.cursor()