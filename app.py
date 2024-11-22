from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import json
import mysql.connector
import os
from ocr import ocr_result
import re

app = Flask(__name__)

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="python"
)
cursor = conn.cursor()


@app.route("/ocr", methods=["POST"])
def ocr():
    global conn, cursor

    # Menerima gambar dari request
    image_file = request.files["files"]

    # Simpan gambar yang diunggah
    image_path = os.path.join("uploads", "image.png")
    image_file.save(image_path)

    # Mendapatkan hasil OCR
    data = ocr_result()

    # Extract fields from data
    nik = data[3]
    nama = data[4]
    tempat_tanggal_lahir = data[5]
    jenis_kelamin = data[6]
    alamat = data[7]
    rt_rw = data[8]
    kelurahan_desa = data[9]
    kecamatan = data[10]
    agama = data[11]
    status_perkawinan = data[12]
    pekerjaan = data[13]
    kewarganegaraan = data[16]
    berlaku_hingga = data[17]

    insert_query = """INSERT INTO `ktp` (`nik`, `nama`, `tempat_lahir`, `tanggal_lahir`, `jenis_kelamin`, `golongan_darah`, `alamat`, `rt`, `rw`, `kelurahan_atau_desa`, `kecamatan`, `agama`, `status_perkawinan`, `pekerjaan`, `kewarganegaraan`, `berlaku_hingga`) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    # Insert data into MySQL database
    # insert_query = """
    # INSERT INTO ktp (provinsi, kabupaten, nik, nama, tempat_tanggal_lahir, jenis_kelamin, alamat, rt_rw, kelurahan_desa, kecamatan, agama, status_perkawinan, pekerjaan, kewarganegaraan, berlaku_hingga)
    # VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    # """

    values = (
        nik,
        nama,
        tempat_tanggal_lahir,
        tempat_tanggal_lahir,
        jenis_kelamin,
        jenis_kelamin,
        alamat,
        rt_rw,
        rt_rw,
        kelurahan_desa,
        kecamatan,
        agama,
        status_perkawinan,
        pekerjaan,
        kewarganegaraan,
        berlaku_hingga,
    )
    cursor.execute(insert_query, values)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    return "Data telah disimpan ke dalam database."


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=True, port=port)
