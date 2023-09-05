import qrcode
import multiprocessing
from multiprocessing import freeze_support
import os
import concurrent.futures


# Example usage
def read_file_as_string(filename):
    with open(filename, "r") as f:
        return f.read()


def generate_qr_code(data, filename, version=10):
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_path = os.path.join("qr_codes", filename)  # Save in 'qr_codes' directory
    img.save(img_path)
    return img_path


def divide_into_chunks(data, chunk_size):
    chunks = [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]
    return chunks


# Example usage
# Example usage
text = "Hello, World!"
filename = "qr_code_{}.png"
data = read_file_as_string("./input.hex")
chunk_size = 1000


# Create 'qr_codes' directory if it doesn't exist
os.makedirs("qr_codes", exist_ok=True)

chunks = divide_into_chunks(data, chunk_size)

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = []
    for i, chunk in enumerate(chunks):
        qr_filename = filename.format(i)
        result = executor.submit(generate_qr_code, chunk, qr_filename, 10)
        results.append(result)

    for result in concurrent.futures.as_completed(results):
        img_path = result.result()
        print("QR code generated:", img_path)

print("QR codes generated successfully.")
