from database import conn, cursor
from barcode_generator import generate_barcode, create_barcode_image
from tkinter import messagebox


def save_medicine(name, company, price, stock, expiry):

    # Generate barcode
    barcode = generate_barcode()

    # Create barcode image
    create_barcode_image(barcode)


    sql = """
    INSERT INTO Medicines
    (
    medicine_name,
    company,
    price,
    stock,
    expiry_date,
    barcode
    )
    VALUES (%s,%s,%s,%s,%s,%s)
    """


    cursor.execute(
        sql,
        (
            name,
            company,
            price,
            stock,
            expiry,
            barcode
        )
    )


    conn.commit()


    messagebox.showinfo(
        "Success",
        f"""
Medicine Added Successfully

Medicine : {name}

Barcode : {barcode}
"""
    )