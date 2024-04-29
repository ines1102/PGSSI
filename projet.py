import secrets
import hashlib
import time
import qrcode
import sqlite3


conn = sqlite3.connect('user.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS patients
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                numero_unique TEXT UNIQUE)''')

conn.commit()

def generate_unique_key():
   
    random_string = secrets.token_hex(16)  # ici on sécurise

    
    timestamp = str(int(time.time()))

   
    combined_string = random_string + timestamp

    # ici on fait de la viande hachée
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

def add_patient(nom, prenom):
    # Générer un numéro unique pour le patient
    numero_unique = generate_unique_key()

    # Ajouter le patient à la base de données avec son numéro unique
    cursor.execute("INSERT INTO patients (nom, prenom, numero_unique) VALUES (?, ?, ?)", (nom, prenom, numero_unique))
    conn.commit()

    print("Patient ajouté avec succès. Numéro unique généré :", numero_unique)

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

# Ajouter un patient à la base de données
add_patient("Doe", "John")

# Génére un fucking QR code pour le patient ajouté
cursor.execute("SELECT numero_unique FROM patients WHERE nom='Doe' AND prenom='John'")
numero_unique = cursor.fetchone()[0]  # Récupérer le numéro unique du patient ajouté
generate_qr_code(numero_unique, "patient_qr_code.png")
print("QR code généré avec succès pour le patient ajouté.")

# Extraire le numéro identifié par le scanner de QR code pour trouver le patient
#  simuler le processus en utilisant simplement le numéro unique généré précédemment
# En pratique, vous devrez lire le numéro unique à partir du QR code scanné
numero_unique_scanner = numero_unique  # Ici, je simule en utilisant le même numéro unique
print("\nExtraction du numéro identifié par le scanner de QR code :", numero_unique_scanner)
find_patient_by_unique_number(numero_unique_scanner)

conn.close()