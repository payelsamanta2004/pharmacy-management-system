import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

from database import conn, cursor
from medicine import save_medicine
from invoice import generate_invoice
from tkinter import scrolledtext
from ai_assistant import ai_assistant
USERNAME = "admin"
PASSWORD = "admin123"
def add_medicine():
    add_window = tk.Toplevel(root)
    add_window.title("Add Medicine")
    add_window.geometry("400x350")

    tk.Label(add_window, text="Medicine Name").pack(pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.pack()

    tk.Label(add_window, text="Company").pack(pady=5)
    company_entry = tk.Entry(add_window)
    company_entry.pack()

    tk.Label(add_window, text="Price").pack(pady=5)
    price_entry = tk.Entry(add_window)
    price_entry.pack()

    tk.Label(add_window, text="Stock").pack(pady=5)
    stock_entry = tk.Entry(add_window)
    stock_entry.pack()

    tk.Label(add_window, text="Expiry Date (YYYY-MM-DD)").pack(pady=5)
    expiry_entry = tk.Entry(add_window)
    expiry_entry.pack()

    def save_data():
        name = name_entry.get()
        company = company_entry.get()
        price = float(price_entry.get())
        stock = int(stock_entry.get())
        expiry = expiry_entry.get()

        save_medicine(name, company, price, stock, expiry)

        messagebox.showinfo("Success", "Medicine Added Successfully!")
        add_window.destroy()

    tk.Button(
        add_window,
        text="Save",
        command=save_data,
        bg="green",
        fg="white"
    ).pack(pady=15)
def view_medicines():
    view_window = tk.Toplevel(root)
    view_window.title("Medicine List")
    view_window.geometry("700x400")

    tree = ttk.Treeview(
        view_window,
        columns=("ID", "Name", "Company", "Price", "Stock", "Expiry"),
        show="headings"
    )

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Company", text="Company")
    tree.heading("Price", text="Price")
    tree.heading("Stock", text="Stock")
    tree.heading("Expiry", text="Expiry")

    cursor.execute("SELECT * FROM Medicines")
    records = cursor.fetchall()

    for row in records:
        tree.insert("", tk.END, values=row)

    tree.pack(fill="both", expand=True)
def search_medicine():
    search_window = tk.Toplevel(root)
    search_window.title("Search Medicine")
    search_window.geometry("400x250")

    tk.Label(
        search_window,
        text="Enter Medicine Name",
        font=("Arial", 12)
    ).pack(pady=10)

    name_entry = tk.Entry(search_window, width=30)
    name_entry.pack()

    def search():
        name = name_entry.get()

        cursor.execute(
            "SELECT * FROM Medicines WHERE medicine_name=%s",
            (name,)
        )

        result = cursor.fetchone()

        if result:
            messagebox.showinfo(
                "Medicine Found",
                f"ID: {result[0]}\n"
                f"Name: {result[1]}\n"
                f"Company: {result[2]}\n"
                f"Price: {result[3]}\n"
                f"Stock: {result[4]}\n"
                f"Expiry: {result[5]}"
            )
        else:
            messagebox.showerror(
                "Not Found",
                "Medicine not found!"
            )

    tk.Button(
        search_window,
        text="Search",
        command=search
    ).pack(pady=15)

def update_medicine():
    update_window = tk.Toplevel(root)
    update_window.title("Update Medicine")
    update_window.geometry("400x300")

    tk.Label(update_window, text="Medicine ID").pack()
    id_entry = tk.Entry(update_window)
    id_entry.pack()

    tk.Label(update_window, text="New Stock").pack()
    stock_entry = tk.Entry(update_window)
    stock_entry.pack()

    def update():
        medicine_id = id_entry.get()
        new_stock = stock_entry.get()

        cursor.execute(
            "UPDATE Medicines SET stock=%s WHERE medicine_id=%s",
            (new_stock, medicine_id)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Medicine Updated Successfully!"
        )

        update_window.destroy()

    tk.Button(
        update_window,
        text="Update",
        command=update
    ).pack(pady=15)

def delete_medicine():

    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Medicine")
    delete_window.geometry("400x220")

    tk.Label(
        delete_window,
        text="Enter Medicine ID"
    ).pack(pady=10)

    id_entry = tk.Entry(delete_window)
    id_entry.pack()

    def delete():

        medicine_id = id_entry.get().strip()

        if medicine_id == "":
            messagebox.showerror(
                "Error",
                "Please Enter Medicine ID"
            )
            return

        # Medicine আছে কিনা দেখুন
        cursor.execute(
            "SELECT * FROM Medicines WHERE medicine_id=%s",
            (medicine_id,)
        )

        result = cursor.fetchone()

        if result is None:
            messagebox.showerror(
                "Error",
                "Medicine ID Not Found"
            )
            return

        # Delete 
        cursor.execute(
            "DELETE FROM Medicines WHERE medicine_id=%s",
            (medicine_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Medicine Deleted Successfully!"
        )

        delete_window.destroy()

    tk.Button(
        delete_window,
        text="Delete",
        bg="red",
        fg="white",
        command=delete
    ).pack(pady=15)
def billing_system():

    bill_window = tk.Toplevel(root)
    bill_window.title("Billing System")
    bill_window.geometry("420x350")

    # Customer Name
    tk.Label(
        bill_window,
        text="Customer Name"
    ).pack(pady=5)

    customer_entry = tk.Entry(
        bill_window,
        width=35
    )
    customer_entry.pack()

    # Medicine Name
    tk.Label(
        bill_window,
        text="Medicine Name"
    ).pack(pady=5)

    cursor.execute("SELECT medicine_name FROM Medicines")
    medicine_list = [row[0] for row in cursor.fetchall()]

    medicine_entry = ttk.Combobox(
        bill_window,
        values=medicine_list,
        width=32,
        state="readonly"
    )
    medicine_entry.pack()

    # Quantity
    tk.Label(
        bill_window,
        text="Quantity"
    ).pack(pady=5)

    qty_entry = tk.Entry(
        bill_window,
        width=35
    )
    qty_entry.pack()

    # Generate Bill
    def generate_bill():

        customer = customer_entry.get().strip()
        medicine_name = medicine_entry.get().strip()

        if customer == "" or medicine_name == "":
            messagebox.showerror(
                "Error",
                "Please fill all fields"
            )
            return

        try:
            quantity = int(qty_entry.get())

        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter valid quantity"
            )
            return

        cursor.execute("""
        SELECT medicine_id, stock, price, barcode
        FROM Medicines
        WHERE medicine_name=%s
        """, (medicine_name,))

        result = cursor.fetchone()

        if not result:
            messagebox.showerror(
                "Error",
                "Medicine Not Found"
            )
            return

        medicine_id, stock, price, barcode_number = result

        if quantity > stock:
            messagebox.showerror(
                "Error",
                "Not Enough Stock"
            )
            return

        total = price * quantity

        cursor.execute("""
        UPDATE Medicines
        SET stock=%s
        WHERE medicine_id=%s
        """, (stock - quantity, medicine_id))

        cursor.execute("""
        INSERT INTO Sales
        (customer_id, medicine_id, quantity, total_amount)
        VALUES (%s,%s,%s,%s)
        """, (1, medicine_id, quantity, total))

        conn.commit()

        generate_invoice(
    customer,
    medicine_name,
    quantity,
    price,
    total,
    barcode_number
    )

        messagebox.showinfo(
            "Success",
            f"Bill Generated Successfully\n\nTotal = ₹{total}"
        )

        bill_window.destroy()

    tk.Button(
        bill_window,
        text="Generate Bill",
        bg="green",
        fg="white",
        width=20,
        command=generate_bill
    ).pack(pady=20)

def sales_report():
    report_window = tk.Toplevel(root)
    report_window.title("Sales Report")
    report_window.geometry("700x400")

    tree = ttk.Treeview(
        report_window,
        columns=("ID", "Medicine ID", "Quantity", "Total Price"),
        show="headings"
    )

    tree.heading("ID", text="Sale ID")
    tree.heading("Medicine ID", text="Medicine ID")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Total Price", text="Total Price")

    cursor.execute("SELECT * FROM Sales")

    records = cursor.fetchall()

    for row in records:
        tree.insert("", tk.END, values=row)

    tree.pack(fill="both", expand=True)
def add_customer():
    customer_window = tk.Toplevel(root)
    customer_window.title("Add Customer")
    customer_window.geometry("400x250")

    tk.Label(
        customer_window,
        text="Customer Name"
    ).pack(pady=5)

    name_entry = tk.Entry(customer_window)
    name_entry.pack()

    tk.Label(
        customer_window,
        text="Phone Number"
    ).pack(pady=5)

    phone_entry = tk.Entry(customer_window)
    phone_entry.pack()

    def save_customer():
        name = name_entry.get()
        phone = phone_entry.get()

        cursor.execute(
            "INSERT INTO Customers (customer_name, phone) VALUES (%s,%s)",
            (name, phone)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Customer Added Successfully!"
        )

        customer_window.destroy()

    tk.Button(
        customer_window,
        text="Save Customer",
        bg="green",
        fg="white",
        command=save_customer
    ).pack(pady=15)
def view_customers():
    customer_list_window = tk.Toplevel(root)
    customer_list_window.title("Customer List")
    customer_list_window.geometry("600x400")

    tree = ttk.Treeview(
        customer_list_window,
        columns=("ID", "Name", "Phone"),
        show="headings"
    )

    tree.heading("ID", text="Customer ID")
    tree.heading("Name", text="Customer Name")
    tree.heading("Phone", text="Phone Number")

    cursor.execute("SELECT * FROM Customers")

    records = cursor.fetchall()

    for row in records:
        tree.insert("", tk.END, values=row)

    tree.pack(fill="both", expand=True)
def add_supplier():
    supplier_window = tk.Toplevel(root)
    supplier_window.title("Add Supplier")
    supplier_window.geometry("400x300")

    tk.Label(
        supplier_window,
        text="Supplier Name"
    ).pack(pady=5)

    name_entry = tk.Entry(supplier_window)
    name_entry.pack()

    tk.Label(
        supplier_window,
        text="Company Name"
    ).pack(pady=5)

    company_entry = tk.Entry(supplier_window)
    company_entry.pack()

    tk.Label(
        supplier_window,
        text="Phone Number"
    ).pack(pady=5)

    phone_entry = tk.Entry(supplier_window)
    phone_entry.pack()

    def save_supplier():
        name = name_entry.get()
        company = company_entry.get()
        phone = phone_entry.get()

        cursor.execute(
            "INSERT INTO Suppliers (supplier_name, company, phone) VALUES (%s,%s,%s)",
            (name, company, phone)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Supplier Added Successfully!"
        )

        supplier_window.destroy()

    tk.Button(
        supplier_window,
        text="Save Supplier",
        bg="green",
        fg="white",
        command=save_supplier
    ).pack(pady=15)
def view_suppliers():
    supplier_list_window = tk.Toplevel(root)
    supplier_list_window.title("Supplier List")
    supplier_list_window.geometry("600x400")

    tree = ttk.Treeview(
        supplier_list_window,
        columns=("ID", "Name", "Company", "Phone"),
        show="headings"
    )

    tree.heading("ID", text="Supplier ID")
    tree.heading("Name", text="Supplier Name")
    tree.heading("Company", text="Company")
    tree.heading("Phone", text="Phone Number")

    cursor.execute("SELECT * FROM Suppliers")

    records = cursor.fetchall()

    for row in records:
        tree.insert("", tk.END, values=row)

    tree.pack(fill="both", expand=True)
def view_purchases():
    purchase_window = tk.Toplevel(root)
    purchase_window.title("Purchase List")
    purchase_window.geometry("700x400")

    tree = ttk.Treeview(
        purchase_window,
        columns=("ID", "Medicine ID", "Supplier ID", "Quantity", "Price", "Date"),
        show="headings"
    )

    tree.heading("ID", text="Purchase ID")
    tree.heading("Medicine ID", text="Medicine ID")
    tree.heading("Supplier ID", text="Supplier ID")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Price", text="Purchase Price")
    tree.heading("Date", text="Purchase Date")

    cursor.execute("SELECT * FROM Purchases")

    records = cursor.fetchall()

    for row in records:
        tree.insert("", tk.END, values=row)

    tree.pack(fill="both", expand=True)
def add_purchase():
    purchase_window = tk.Toplevel(root)
    purchase_window.title("Add Purchase")
    purchase_window.geometry("400x350")

    tk.Label(purchase_window, text="Medicine ID").pack()
    medicine_entry = tk.Entry(purchase_window)
    medicine_entry.pack()

    tk.Label(purchase_window, text="Supplier ID").pack()
    supplier_entry = tk.Entry(purchase_window)
    supplier_entry.pack()

    tk.Label(purchase_window, text="Quantity").pack()
    quantity_entry = tk.Entry(purchase_window)
    quantity_entry.pack()

    tk.Label(purchase_window, text="Purchase Price").pack()
    price_entry = tk.Entry(purchase_window)
    price_entry.pack()

    tk.Label(purchase_window, text="Purchase Date (YYYY-MM-DD)").pack()
    date_entry = tk.Entry(purchase_window)
    date_entry.pack()
    def save_purchase():
        medicine_id = medicine_entry.get()
        supplier_id = supplier_entry.get()
        quantity = quantity_entry.get()
        purchase_price = price_entry.get()
        purchase_date = date_entry.get()

        cursor.execute("""
            INSERT INTO Purchases
            (medicine_id, supplier_id, quantity, purchase_price, purchase_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            medicine_id,
            supplier_id,
            quantity,
            purchase_price,
            purchase_date
        ))

        conn.commit()
        cursor.execute("""
            UPDATE Medicines
            SET stock = stock + %s
            WHERE medicine_id = %s
        """, (quantity, medicine_id))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Purchase Added Successfully!"
        )

        purchase_window.destroy()
        tk.Button(
        purchase_window,
        text="Save Purchase",
        command=save_purchase,
        bg="green",
        fg="white"
    ).pack(pady=10)
from datetime import date, timedelta

def check_expiry():

    cursor.execute("SELECT medicine_name, expiry_date FROM Medicines")
    medicines = cursor.fetchall()

    message = ""

    today = date.today()
    warning_date = today + timedelta(days=30)

    for medicine in medicines:

        name = medicine[0]
        expiry = medicine[1]

        if expiry is None:
            continue

        if expiry < today:
            message += f"❌ {name} - EXPIRED ({expiry})\n"

        elif expiry <= warning_date:
            message += f"⚠ {name} - Expiring on {expiry}\n"

    if message != "":
        messagebox.showwarning(
            "Expiry Alert",
            message
        )
def expiry_report():

    report = tk.Toplevel(root)
    report.title("Expiry Alert")
    report.geometry("700x400")

    tk.Label(
        report,
        text="⚠ Expiry Report",
        font=("Arial",16,"bold"),
        fg="red"
    ).pack(pady=10)

    tree = ttk.Treeview(
        report,
        columns=("Medicine","Expiry Date","Status"),
        show="headings"
    )

    tree.heading("Medicine", text="Medicine")
    tree.heading("Expiry Date", text="Expiry Date")
    tree.heading("Status", text="Status")

    tree.column("Medicine", width=250)
    tree.column("Expiry Date", width=150)
    tree.column("Status", width=200)

    tree.pack(fill="both", expand=True)

    from datetime import date, timedelta

    today = date.today()
    warning = today + timedelta(days=30)

    cursor.execute("SELECT medicine_name, expiry_date FROM Medicines")

    medicines = cursor.fetchall()

    for medicine in medicines:

        name = medicine[0]
        expiry = medicine[1]

        if expiry is None:
            continue

        if expiry < today:

            status = "❌ Expired"

        elif expiry <= warning:

            status = "⚠ Expiring Soon"

        else:

            continue

        tree.insert("", "end", values=(name, expiry, status))
def low_stock_alert():

    low_stock = tk.Toplevel(root)
    low_stock.title("Low Stock Alert")
    low_stock.geometry("650x400")

    tk.Label(
        low_stock,
        text="🔴 Low Stock Medicines",
        font=("Arial",16,"bold"),
        fg="red"
    ).pack(pady=10)

    tree = ttk.Treeview(
        low_stock,
        columns=("Medicine","Stock"),
        show="headings"
    )

    tree.heading("Medicine", text="Medicine")
    tree.heading("Stock", text="Available Stock")

    tree.column("Medicine", width=300)
    tree.column("Stock", width=150)

    tree.pack(fill="both", expand=True)

    cursor.execute("""
        SELECT medicine_name, stock
        FROM Medicines
        WHERE stock <= 10
    """)

    medicines = cursor.fetchall()

    for medicine in medicines:

        tree.insert("", "end", values=medicine)
def logout():

    answer = messagebox.askyesno(
        "Logout",
        "Do you really want to logout?"
    )

    if answer:
        root.withdraw()

        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

        login_window.deiconify()
        login_window.lift()
        login_window.focus_force()


    
def toggle_theme():

    global theme

    if theme == "light":

        theme = "dark"

        root.configure(bg="#2C2C2C")
        button_frame.configure(bg="#2C2C2C")
        heading.configure(bg="#2C2C2C", fg="white")

    else:

        theme = "light"

        root.configure(bg="#E8F5E9")
        button_frame.configure(bg="#E8F5E9")
        heading.configure(bg="#E8F5E9", fg="#006400")
def dashboard():

    dashboard_window = tk.Toplevel(root)
    dashboard_window.title("Dashboard")
    dashboard_window.state("zoomed")
    dashboard_window.configure(bg="white")

    cursor.execute("SELECT COUNT(*) FROM Medicines")
    medicines = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Customers")
    customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Suppliers")
    suppliers = cursor.fetchone()[0]

    cursor.execute("SELECT IFNULL(SUM(total_amount),0) FROM Sales")
    sales = cursor.fetchone()[0]

    tk.Label(
        dashboard_window,
        text="📊 PHARMACY DASHBOARD",
        font=("Arial", 20, "bold"),
        bg="#F0F8FF",
        fg="#006400"
    ).pack(pady=20)

    tk.Label(
        dashboard_window,
        text=f"💊 Total Medicines : {medicines}",
        font=("Arial", 14, "bold"),
        bg="#90EE90",
         width=30,
         relief="raised"
    ).pack(pady=5)

    tk.Label(
        dashboard_window,
        text=f"👤 Total Customers : {customers}",
        font=("Arial", 14,"bold" ),
        bg="#ADD8E6",
        width=30,
        relief="raised"
    ).pack(pady=5)

    tk.Label(
        dashboard_window,
        text=f"🚚 Total Suppliers : {suppliers}",
        font=("Arial", 14,"bold"),
        
        bg="#FFD580",
        width=30,
        relief="raised"
    ).pack(pady=5)

    tk.Label(
        dashboard_window,
        text=f"💰 Total Sales : ₹{sales}",
        font=("Arial", 14, "bold"),
        bg="#FFB6C1",
        width=30,
        relief="raised"
    ).pack(pady=10)

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == USERNAME and password == PASSWORD:
        login_window.destroy()

        root.attributes("-alpha", 1)
        root.deiconify()

    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid Username or Password!"
        )
root = tk.Tk()
theme = "light"
root.withdraw()
root.attributes("-alpha", 0)
image = Image.open("pharmacy_logo.png")
image = image.resize((100, 100))

logo = ImageTk.PhotoImage(image)
login_window = tk.Toplevel()
login_window.grab_set()

login_window.title("Login")
login_window.geometry("350x250")
login_window.resizable(False, False)

tk.Label(login_window, text="Username").pack(pady=5)

username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Password").pack(pady=5)

password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Button(
    login_window,
    text="Login",
    command=login
).pack(pady=15)
root.title("🏥 Pharmacy Management System")
root.geometry("900x600")
root.state("zoomed")
root.configure(bg="#E8F5E9")
root.resizable(True, True)

button_frame = tk.Frame(root, bg="#E8F5E9")
button_frame.pack(side="top", anchor="n", pady=5)

image = Image.open("pharmacy_logo.png")
image = image.resize((100, 100))   # Logo size

logo = ImageTk.PhotoImage(image)

logo_label = tk.Label(
    button_frame,
    image=logo,
    bg="#E8F5E9"
)

logo_label.grid(row=0, column=0, columnspan=2, pady=2)
heading = tk.Label(
    button_frame,
    text="🏥 Pharmacy Management System",
    font=("Arial", 24, "bold"),
    bg="#E8F5E9",
    fg="#006400"
)
heading.grid(row=1, column=0, columnspan=2, pady=3)

search_btn = tk.Button(
    button_frame,
    text="🔍 Search Medicine",
    font=("Arial", 12, "bold"),
    width=25,
    bg="orange",
    fg="white",
    command=search_medicine
)

search_btn.grid(row=2, column=0, padx=30, pady=5)


add_btn = tk.Button(
    button_frame,
    text="➕ Add Medicine",
    font=("Arial", 12, "bold"),
    width=25,
    bg="green",
    fg="white",
    command=add_medicine
)

add_btn.grid(row=3, column=0, padx=30, pady=5)

update_btn = tk.Button(
    button_frame,
    text="✏️ Update Medicine",
    font=("Arial", 12, "bold"),
    width=25,
    bg="purple",
    fg="white",
    command=update_medicine
)
update_btn.grid(row=3, column=1, padx=30, pady=5)

delete_btn = tk.Button(
    button_frame,
    text="🗑 Delete Medicine",
    font=("Arial", 12, "bold"),
    width=25,
    bg="red",
    fg="white",
    command=delete_medicine
)

delete_btn.grid(row=4, column=0, padx=30, pady=5)

billing_btn = tk.Button(
    button_frame,
    text="🧾 Billing System",
    font=("Arial", 12, "bold"),
    width=25,
    bg="orange",
    fg="white",
    command=billing_system
)

billing_btn.grid(row=4, column=1, padx=30, pady=5)

sales_btn = tk.Button(
    button_frame,
    text="📊 Sales Report",
    font=("Arial", 12, "bold"),
    width=25,
    bg="brown",
    fg="white",
    command=sales_report
)

sales_btn.grid(row=5, column=0, padx=30, pady=5)

customer_btn = tk.Button(
    button_frame,
    text="👤 Add Customer",
    font=("Arial", 12, "bold"),
    width=25,
    bg="teal",
    fg="white",
    command=add_customer
)

customer_btn.grid(row=5, column=1, padx=30, pady=5)


view_customer_btn = tk.Button(
    button_frame,
    text="📋 View Customers",
    font=("Arial", 12, "bold"),
    width=25,
    bg="darkblue",
    fg="white",
    command=view_customers
)

view_customer_btn.grid(row=6, column=0, padx=30, pady=5)


view_btn = tk.Button(
    button_frame,
    text="📋 View Medicines",
    font=("Arial", 12, "bold"),
    width=25,
    bg="blue",
    fg="white",
    command=view_medicines
)

view_btn.grid(row=2, column=1, padx=30, pady=5)


supplier_btn = tk.Button(
    button_frame,
    text="🚚 Add Supplier",
    font=("Arial", 12, "bold"),
    width=25,
    bg="green",
    fg="white",
    command=add_supplier
)

supplier_btn.grid(row=6, column=1, padx=30, pady=5)


view_supplier_btn = tk.Button(
    button_frame,
    text="📋 View Suppliers",
    font=("Arial", 12, "bold"),
    width=25,
    bg="darkcyan",
    fg="white",
    command=view_suppliers
)

view_supplier_btn.grid(row=7, column=0, padx=30, pady=5)

purchase_btn = tk.Button(
    button_frame,
    text="🛒 Add Purchase",
    font=("Arial", 12, "bold"),
    width=25,
    bg="#8B4513",
    fg="white",
    command=add_purchase
)

purchase_btn.grid(row=7, column=1, padx=30, pady=5)

view_purchase_btn = tk.Button(
    button_frame,
    text="📋 View Purchases",
    font=("Arial", 12, "bold"),
    width=25,
    bg="darkgreen",
    fg="white",
    command=view_purchases
)

view_purchase_btn.grid(row=8, column=0, padx=30, pady=5)

dashboard_btn = tk.Button(
    button_frame,
    text="📊 Dashboard",
    font=("Arial", 12, "bold"),
    width=25,
    bg="purple",
    fg="white",
    command=dashboard
)

dashboard_btn.grid(row=8, column=1, padx=30, pady=5)

expiry_btn = tk.Button(
    button_frame,
    text="⚠ Expiry Alert",
    font=("Arial",12,"bold"),
    width=25,
    bg="red",
    fg="white",
    command=expiry_report
)

expiry_btn.grid(row=9, column=0, padx=30, pady=5)
low_stock_btn = tk.Button(
    button_frame,
    text="🔴 Low Stock",
    font=("Arial",12,"bold"),
    width=25,
    bg="darkred",
    fg="white",
    command=low_stock_alert
)

low_stock_btn.grid(row=9, column=1, padx=30, pady=5)
logout_btn = tk.Button(
    button_frame,
    text="🚪 Logout",
    font=("Arial",12,"bold"),
    width=25,
    bg="red",
    fg="white",
    command=logout
)

logout_btn.grid(row=10, column=0, padx=30, pady=5)
ai_btn = tk.Button(
    button_frame,
    text="🤖 AI Pharmacy Assistant",
    font=("Arial",12,"bold"),
    width=25,
    bg="blue",
    fg="white",
    command=lambda: ai_assistant(root, cursor)
)

ai_btn.grid(row=10, column=1, padx=30, pady=5)
theme_btn = tk.Button(
    button_frame,
    text="🌙 Dark / ☀ Light",
    font=("Arial", 12, "bold"),
    width=25,
    bg="#444",
    fg="white",
    command=toggle_theme
)

theme_btn.grid(row=11, column=0, padx=30, pady=5)
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
status = tk.Label(
    root,
    text="© Pharmacy Management System | Developed by Payel",
    bd=1,
    relief=tk.SUNKEN,
    anchor="w",
    font=("Arial", 10),
    bg="lightgray"
)

status.pack(side=tk.BOTTOM, fill=tk.X)
check_expiry()
root.mainloop()