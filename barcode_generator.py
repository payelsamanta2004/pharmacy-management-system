import random
import os
import barcode
from barcode.writer import ImageWriter


def generate_barcode():
    return str(random.randint(8900000000000, 8999999999999))


def create_barcode_image(code):

    folder = "barcodes"

    if not os.path.exists(folder):
        os.makedirs(folder)

    barcode_class = barcode.get_barcode_class("code128")

    my_barcode = barcode_class(
        code,
        writer=ImageWriter()
    )

    file_path = my_barcode.save(
        f"{folder}/{code}"
    )

    return file_path