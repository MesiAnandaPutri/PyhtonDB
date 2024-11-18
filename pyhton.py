import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    #Menjalankan perintah sql untuk membuat tabel nilai
    cursor.execute("""          
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
         )
    """)
    conn.commit() #Menyimpan perubahan yang telah dilakukan pd database
    conn.close() # menutup koneksi ke database
    
#Fungsi untuk mengambil semua data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa") #Menjanlankan perinah sql unt mengambil semua data dr tabel nilai_siswa
    rows = cursor.fetchall() #Mengambil semua baris hasil query dan menyimpannya dalam rows.
    conn.close()
    return rows

#Fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    #Menjalankan query SQL untuk menyisipkan data ke dalam tabel.
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()
    
#Fungsi untuk memperbarui data di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    #Menjalankan query SQL untuk memperbarui nilai siswa pada kolom yang sesuai dengan ID yang diberikan.
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    conn.close()
    
#Fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    #Menjalankan query SQL untuk menghapus data berdasarkan ID yang diberikan.
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()
    
#Fungsi untuk menghitung prediksi fakultas
def calculate_prediction(biologi, fisika, inggris):
    #Jika nilai Biologi lebih besar dari Fisika dan Inggris, maka fakultas yang diprediksi adalah "Kedokteran".
    if biologi > fisika  and biologi > inggris:
        return "Kedokteran"
    #Jika nilai Fisika lebih besar, maka fakultas yang diprediksi adalah "Teknik".
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    #Jika nilai Inggris lebih besar, maka fakultas yang diprediksi adalah "Bahasa".
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    #Jika ada nilai yang sama atau tidak ada nilai yang lebih besar, maka fakultas yang diprediksi adalah "Tidak Diketahui".
    else:
        return "Tidak Diketahui"
    
#Fungsi untuk menangani tombol submit
def submit(): # fungsi ini akan berfungsi ketika tombol add ditekan
         #Saya menambahkan try-except khusus di dalam submit() untuk memastikan bahwa hanya huruf alih-alih angka) 
    try: #yang ditangani dengan pesan error "Nilai Biologi, Fisika, dan Inggris harus berupa angka."
        nama = nama_var.get()
        try:
            biologi = int(biologi_var.get())
            fisika = int(fisika_var.get())
            inggris = int(inggris_var.get())
        except ValueError:
            raise ValueError("Nilai Biologi, Fisika, dan Inggris harus berupa angka.")
       