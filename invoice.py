from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import barcode
from barcode.writer import ImageWriter

def generate_invoice(customer, medicine, quantity, price, total, barcode_number):

    file_name = "New_Bill.pdf"

    current_date = datetime.now().strftime("%d-%m-%Y %H:%M")
    invoice_no = "INV-" + datetime.now().strftime("%Y%m%d%H%M%S")

    # Barcode Image 
    code128 = barcode.get("code128", str(barcode_number), writer=ImageWriter())
    barcode_file = code128.save("barcode")

    pdf = canvas.Canvas(file_name, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(130, 760, "PHARMACY MANAGEMENT SYSTEM")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(150, 740, "Medical Store Invoice")
    pdf.drawString(150, 725, "ABC Medical Store")
    pdf.drawString(150, 710, "Kolkata, West Bengal")
    pdf.drawString(150, 695, "Phone : +91 9876543210")

    pdf.line(40, 680, 560, 680)

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 650, f"Customer Name : {customer}")
    pdf.drawString(350, 650, f"Invoice No : {invoice_no}")
    pdf.drawString(350, 630, f"Date : {current_date}")

    pdf.line(40, 610, 560, 610)

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 585, "Medicine Name")
    pdf.drawString(270, 585, "Quantity")
    pdf.drawString(370, 585, "Price")
    pdf.drawString(470, 585, "Total")

    pdf.line(40, 575, 560, 575)

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 550, str(medicine))
    pdf.drawString(290, 550, str(quantity))
    pdf.drawString(380, 550, f"₹{price}")
    pdf.drawString(480, 550, f"₹{total}")

    # Barcode Number
    pdf.drawString(50, 510, f"Barcode : {barcode_number}")

    # Barcode Image
    pdf.drawImage(barcode_file, 50, 400, width=220, height=70)

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(350, 370, f"Grand Total : ₹{total}")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(150, 340, "Thank You For Shopping!")
    pdf.drawString(120, 320, "Visit Again - ABC Medical Store")

    pdf.save()

    return file_name