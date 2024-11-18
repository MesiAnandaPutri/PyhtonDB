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
        #memastikan nama tidak boleh kosong
        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")
        #untuk memastikan bahwa nilai tidak melebihi 100. Jika ya, maka ValueError akan dilempar 
        # dengan pesan yang sesuai "Nilai tidak boleh lebih dari 100 dan kurang dari nol."
        if biologi > 100 or fisika > 100 or inggris > 100:
            raise ValueError("Nilai tidak boleh lebih dari 100.")
        if biologi < 0 or fisika < 0 or inggris < 0:
            raise ValueError("Nilai tidak boleh kurang dari 0.")
        
        prediksi = calculate_prediction(biologi, fisika, inggris)
        save_to_database(nama, biologi, fisika, inggris, prediksi)
        
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_input()
        populate_table()
    
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

#   try:
  #      nama = nama_var.get()
   #     biologi = int(biologi_var.get())
    #    fisika = int(fisika_var.get())
     #   inggris = int(inggris_var.get())
        
      #  if not nama:
       #     raise Exception("Nama siswa tidak boleh kosong.")
        
        #prediksi = calculate_prediction(biologi, fisika, inggris)
        #save_to_database(nama, biologi, fisika, inggris, prediksi)
        
        #messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        #clear_input()
        #populate_table()
    #except ValueError:
     #   messagebox.showerror("Error", "Nilai Biologi, Fisika, dan Inggris harus berupa angka.") 
        
#Fungsi untuk menangani tombol update
def update(): # Memastikan bahwa data yang dipilih ada di tabel, kemudian memperbarui data tersebut di database.
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk di-update!")
        
        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())
        
        if not nama: # menampilkan eror ketika nama kosong
            raise ValueError("Nama siswa tidak boleh kosong.")
        
        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)
        
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!") # menampilkan pesan ketika data berhasil diperbarui
        clear_input()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")
        
#Fungsi untuk menangani tombol delete
def delete(): #Memastikan bahwa data yang dipilih ada di tabel, kemudian menghapus data tersebut dari database.
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")
        
        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_input()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")
        
#Fungsi unruk mengosongkan input
def clear_input(): #Fungsi ini membersihkan semua inputan di form (nama siswa, nilai-nilai mata pelajaran, dan ID yang dipilih).
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("") # selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih
       
#Fungsi untuk mengisi tabel dengan data dari database
def populate_table(): # Setiap baris diambil dan ditampilkan dalam tabel menggunakan tree.insert().
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_data():
        tree.insert("", "end", values=row)

#Fungsi untuk mengisi input dengan data dari tabel
def fill_inputs_from_table(event): #Ini dipicu saat pengguna mengklik baris di tabel.
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']
        
        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])  
        biologi_var.set(selected_row[2])   
        fisika_var.set(selected_row[3])   
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")
        
#inisialisasi database
create_database()
