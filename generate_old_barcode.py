from database import cursor
from barcode_generator import create_barcode_image


cursor.execute(
    "SELECT barcode FROM Medicines WHERE barcode IS NOT NULL"
)

data = cursor.fetchall()

for row in data:
    barcode = row[0]
    create_barcode_image(barcode)
    print("Created:", barcode)