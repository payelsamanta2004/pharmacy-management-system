import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Payel12@",
    database="pharmacy_db"
)

cursor = conn.cursor()

while True:
    print("\n===== Pharmacy Management System =====")
    print("1. Add Medicine")
    print("2. View Medicines")
    print("3. Search Medicine")
    print("4. Update Medicine")
    print("5. Exit")
    print("6. Delete Medicine")
    print("7. Billing System")
    print("8. View Sales Report")
    print("9. Add Customer")
    print("10. View Customers")
    print("11. Add Supplier")
    print("12. View Suppliers")
    print("13. Purchase Medicine")
    print("14. View Purchase Report")

    choice = input("Enter your choice: ")
    print("You entered:", repr(choice))

    if choice == "1":
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

        cursor.execute(sql, (name, company, price, stock, expiry))
        conn.commit()

        print("Medicine Added Successfully!")
    elif choice == "2":
        cursor.execute("SELECT * FROM Medicines")
        records = cursor.fetchall()

        print("\n===== Medicine List =====")
        for row in records:
            print(row)

    elif choice == "3":
        name = input("Enter Medicine Name: ")

        cursor.execute(
            "SELECT * FROM Medicines WHERE medicine_name=%s",
            (name,)
        )

        record = cursor.fetchone()

        if record:
            print("\nMedicine Found:")
            print(record)
        else:
            print("Medicine Not Found!")

    elif choice == "4":
        medicine_id = int(input("Enter Medicine ID: "))
        new_stock = int(input("Enter New Stock: "))

        cursor.execute(
            "UPDATE Medicines SET stock=%s WHERE medicine_id=%s",
            (new_stock, medicine_id)
        )

        conn.commit()

        print("Stock Updated Successfully!")

    elif choice == "6":
        medicine_id = int(input("Enter Medicine ID to Delete: "))

        cursor.execute(
            "DELETE FROM Medicines WHERE medicine_id=%s",
            (medicine_id,)
        )

        conn.commit()
        print("Medicine Deleted Successfully!")

    elif choice == "7":
        medicine_id = int(input("Enter Medicine ID: "))
        quantity = int(input("Enter Quantity: "))

        cursor.execute(
            "SELECT stock, price FROM Medicines WHERE medicine_id=%s",
            (medicine_id,)
        )

        result = cursor.fetchone()

        if result:
            stock, price = result

            if stock >= quantity:
                total_price = price * quantity
                new_stock = stock - quantity

            else:
                print("Not enough stock!")

        else:
            print("Medicine not found!")
    elif choice == "8":
        cursor.execute("SELECT * FROM Sales")
        sales = cursor.fetchall()

        print("\n===== Sales Report =====")

        if sales:
            for row in sales:
                print(row)
        else:
            print("No Sales Found!")
    elif choice == "9":
        customer_name = input("Enter Customer Name: ")
        phone = input("Enter Phone Number: ")

        cursor.execute(
            "INSERT INTO Customers (customer_name, phone) VALUES (%s, %s)",
            (customer_name, phone)
        )

        conn.commit()

        print("Customer Added Successfully!")
    elif choice == "10":
        cursor.execute("SELECT * FROM Customers")
        customers = cursor.fetchall()

        print("\n===== Customer List =====")

        if customers:
            for row in customers:
                print(row)
        else:
            print("No Customers Found!")
    elif choice == "11":
        supplier_name = input("Enter Supplier Name: ")
        company = input("Enter Company Name: ")
        phone = input("Enter Phone Number: ")

        cursor.execute(
            "INSERT INTO Suppliers (supplier_name, company, phone) VALUES (%s, %s, %s)",
            (supplier_name, company, phone)
        )

        conn.commit()

        print("Supplier Added Successfully!")
    elif choice == "12":
        cursor.execute("SELECT * FROM Suppliers")
        suppliers = cursor.fetchall()

        print("\n===== Supplier List =====")

        if suppliers:
            for row in suppliers:
                print(row)
        else:
            print("No Suppliers Found!")
    elif choice == "13":
        medicine_id = int(input("Enter Medicine ID: "))
        supplier_id = int(input("Enter Supplier ID: "))
        quantity = int(input("Enter Purchase Quantity: "))
        purchase_date = input("Enter Purchase Date (YYYY-MM-DD): ")

        # Check medicine exists
        cursor.execute(
            "SELECT stock FROM Medicines WHERE medicine_id=%s",
            (medicine_id,)
        )

        result = cursor.fetchone()

        if result:
            current_stock = result[0]
            new_stock = current_stock + quantity

            # Update stock
            cursor.execute(
                "UPDATE Medicines SET stock=%s WHERE medicine_id=%s",
                (new_stock, medicine_id)
            )

            # Save purchase
            cursor.execute(
                """
                INSERT INTO Purchases
                (medicine_id, supplier_id, quantity, purchase_date)
                VALUES (%s, %s, %s, %s)
                """,
                (medicine_id, supplier_id, quantity, purchase_date)
            )

            conn.commit()

            print("Purchase Added Successfully!")
            print("New Stock =", new_stock)

        else:
            print("Medicine ID not found!")
    elif choice == "14":
        cursor.execute("SELECT * FROM Purchases")
        purchases = cursor.fetchall()

        print("\n===== Purchase Report =====")

        if purchases:
            for row in purchases:
                print(row)
        else:
            print("No Purchase Records Found!")

    elif choice == "5":
        print("Thank You!")
        break

    else:
        print("Invalid Choice!")

conn.close()