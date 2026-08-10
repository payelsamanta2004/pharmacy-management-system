import mysql.connector

print("Program Started")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Payel12@",
    database="pharmacy_db"
)

print("Database Connected Successfully")

cursor = conn.cursor()

print("=== Add Medicine ===")

name = input("Medicine Name: ")
company = input("Company Name: ")
price = float(input("Price: "))
stock = int(input("Stock: "))
expiry = input("Expiry Date (YYYY-MM-DD): ")

sql = """
INSERT INTO Medicines
(medicine_name, company, price, stock, expiry_date)
VALUES (%s, %s, %s, %s, %s)
"""

values = (name, company, price, stock, expiry)

cursor.execute(sql, values)
conn.commit()

print("Medicine Added Successfully!")

cursor.execute("SELECT * FROM Medicines")

records = cursor.fetchall()

print("\n===== Medicine List =====")

for row in records:
    print(row)
    
    conn.close()