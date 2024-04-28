import secrets
import hashlib
import time
import qrcode

def generate_unique_key():
    random_string = secrets.token_hex(16)  
    timestamp = str(int(time.time()))
    combined_string = random_string + timestamp
    unique_key = hashlib.sha256(combined_string.encode()).hexdigest()
    return unique_key

def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

key = generate_unique_key()
print("Clé unique générée :", key)

generate_qr_code(key, "unique_key_qr_code.png")
print("QR code généré avec succès.")
