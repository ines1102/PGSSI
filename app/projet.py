import sqlite3
import qrcode
import os

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

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


def generate_and_save_qr_code(numero_unique):
    # Générer le contenu du QR code
    contenu_qr_code = f"Numéro unique : {numero_unique}"

    # Générer le QR code
    qr_filename = f"{numero_unique}.png"
    qr_path = os.path.join('qr_codes', qr_filename)
    generate_qr_code(contenu_qr_code, qr_path)

    # Retourner le nom du fichier QR code généré
    return qr_filename


def find_patient_by_unique_number(numero_unique):
    # Trouver le patient correspondant au numéro unique
    cursor.execute("SELECT * FROM patients WHERE numero_unique=?", (numero_unique,))
    patient = cursor.fetchone()
    if patient:
        print("Patient trouvé :")
        print("ID :", patient[0])
        print("Nom :", patient[1])
        print("Prénom :", patient[2])
        print("Numéro unique :", patient[3])
    else:
        print("Aucun patient trouvé avec ce numéro unique.")

conn.close()