import mysql.connector
import pytesseract
from PIL import Image

class KTPInformation(object):
    def __init__(self):
        self.nik = ""
        self.nama = ""
        self.tempat_lahir = ""
        self.tanggal_lahir = ""
        self.jenis_kelamin = ""
        self.golongan_darah = ""
        self.alamat = ""
        self.rt = ""
        self.rw = ""
        self.kelurahan_atau_desa = ""
        self.kecamatan = ""
        self.agama = ""
        self.status_perkawinan = ""
        self.pekerjaan = ""
        self.kewarganegaraan = ""
        self.berlaku_hingga = "" 

def extract_data_from_image(image_path):
    try:
        # Load the image using Pillow (Python Imaging Library)
        with Image.open(image_path) as img:
            # Extract text from the image using pytesseract
            extracted_text = pytesseract.image_to_string(img)
            return extracted_text
    except Exception as e:
        print("Failed to extract data from the image:", e)
        return None

def parse_ktp_data(extracted_text):
    ktp_info = KTPInformation()

    # Split the text into lines
    lines = extracted_text.split('\n')

    # Loop through each line to find the corresponding data
    for line in lines:
        # Check if the line contains NIK information
        if "NIK" in line:
            ktp_info.nik = line.split(":")[1].strip()
        # Check if the line contains Name information
        elif "Nama" in line:
            ktp_info.nama = line.split(":")[1].strip()
        # Check if the line contains Place of Birth information
        elif "Tempat Lahir" in line:
            ktp_info.tempat_lahir = line.split(":")[1].strip()
        # Check if the line contains Date of Birth information
        elif "Tanggal Lahir" in line:
            ktp_info.tanggal_lahir = line.split(":")[1].strip()
        # Check if the line contains Gender information
        elif "Jenis Kelamin" in line:
            ktp_info.jenis_kelamin = line.split(":")[1].strip()
        # Check if the line contains Blood Type information
        elif "Gol. Darah" in line:
            ktp_info.golongan_darah = line.split(":")[1].strip()
        # Check if the line contains Address information
        elif "Alamat" in line:
            ktp_info.alamat = line.split(":")[1].strip()
        # Check if the line contains RT information
        elif "RT" in line:
            ktp_info.rt = line.split(":")[1].strip()
        # Check if the line contains RW information
        elif "RW" in line:
            ktp_info.rw = line.split(":")[1].strip()
        # Check if the line contains Village or Subdistrict information
        elif "Kel/Desa" in line:
            ktp_info.kelurahan_atau_desa = line.split(":")[1].strip()
        # Check if the line contains District information
        elif "Kecamatan" in line:
            ktp_info.kecamatan = line.split(":")[1].strip()
        # Check if the line contains Religion information
        elif "Agama" in line:
            ktp_info.agama = line.split(":")[1].strip()
        # Check if the line contains Marital Status information
        elif "Status Perkawinan" in line:
            ktp_info.status_perkawinan = line.split(":")[1].strip()
        # Check if the line contains Occupation information
        elif "Pekerjaan" in line:
            ktp_info.pekerjaan = line.split(":")[1].strip()
        # Check if the line contains Nationality information
        elif "Kewarganegaraan" in line:
            ktp_info.kewarganegaraan = line.split(":")[1].strip()
        # Check if the line contains Valid Until information
        elif "Berlaku Hingga" in line:
            ktp_info.berlaku_hingga = line.split(":")[1].strip()

    return ktp_info

def save_to_database(ktp_info):
    try:
        # Establish connection to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your username
            password="",  # Replace with your password
            database="python"  # Replace with your database name
        )

        if conn.is_connected():
            print("Successfully connected to the database!")
            cursor = conn.cursor()

            # SQL query to insert data into ktp table
            sql = """INSERT INTO ktp (
                        nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, 
                        golongan_darah, alamat, rt, rw, kelurahan_atau_desa, 
                        kecamatan, agama, status_perkawinan, pekerjaan, 
                        kewarganegaraan, berlaku_hingga
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )"""
            
            # Execute the query with the values from the KTPInformation object
            cursor.execute(sql, (
                ktp_info.nik, ktp_info.nama, ktp_info.tempat_lahir, ktp_info.tanggal_lahir,
                ktp_info.jenis_kelamin, ktp_info.golongan_darah, ktp_info.alamat, ktp_info.rt,
                ktp_info.rw, ktp_info.kelurahan_atau_desa, ktp_info.kecamatan, ktp_info.agama,
                ktp_info.status_perkawinan, ktp_info.pekerjaan, ktp_info.kewarganegaraan,
                ktp_info.berlaku_hingga
            ))
            conn.commit()
            print("Data successfully saved to ktp table!")

            # Close cursor and connection
            cursor.close()
            conn.close()
    except mysql.connector.Error as error:
        print("Failed to save data to ktp table:", error)

# Example usage:
ktp_info = KTPInformation()
ktp_info.nik = "1234567890123456"
ktp_info.nama = "John Doe"
ktp_info.tempat_lahir = "Jakarta"
ktp_info.tanggal_lahir = "1990-01-01"
ktp_info.jenis_kelamin = "Laki-laki"
ktp_info.golongan_darah = "A"
ktp_info.alamat = "Jalan Jenderal Sudirman No. 1"
ktp_info.rt = "001"
ktp_info.rw = "002"
ktp_info.kelurahan_atau_desa = "Grogol"
ktp_info.kecamatan = "Kebayoran Lama"
ktp_info.agama = "Islam"
ktp_info.status_perkawinan = "Belum Kawin"
ktp_info.pekerjaan = "Pegawai Swasta"
ktp_info.kewarganegaraan = "WNI"
ktp_info.berlaku_hingga = "BERLAKU SEUMUR HIDUP"

# Path to the KTP image
image_path = "ktpocr/dataset/ktp_test.png"

# Extract data from the image
extracted_text = extract_data_from_image(image_path)

if extracted_text:
    # Parse KTP text data
    ktp_info = parse_ktp_data(extracted_text)

    # Save data to the database
    save_to_database(ktp_info)
else:
    print("Failed to extract data from the KTP image.")