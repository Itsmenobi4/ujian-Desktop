from tkinter import *
from tkinter import messagebox, ttk
import sqlite3

# Koneksi ke database SQLite
conn = sqlite3.connect('class_attendance.db')
cursor = conn.cursor()

# Buat tabel jika belum ada
cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    status TEXT NOT NULL)''')
conn.commit()

# Fungsi CRUD
def add_data():
    name = entry_name.get()
    date = entry_date.get()
    status = entry_status.get()

    if name and date and status:
        cursor.execute("INSERT INTO attendance (name, date, status) VALUES (?, ?, ?)", (name, date, status))
        conn.commit()
        fetch_data()
        messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
    else:
        messagebox.showerror("Error", "Semua field harus diisi!")

def update_data():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih data yang ingin diubah!")
        return

    item = tree.item(selected_item)
    record_id = item["values"][0]
    name = entry_name.get()
    date = entry_date.get()
    status = entry_status.get()

    if name and date and status:
        cursor.execute("UPDATE attendance SET name = ?, date = ?, status = ? WHERE id = ?", (name, date, status, record_id))
        conn.commit()
        fetch_data()
        messagebox.showinfo("Sukses", "Data berhasil diubah!")
    else:
        messagebox.showerror("Error", "Semua field harus diisi!")

def delete_data():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih data yang ingin dihapus!")
        return

    item = tree.item(selected_item)
    record_id = item["values"][0]

    cursor.execute("DELETE FROM attendance WHERE id = ?", (record_id,))
    conn.commit()
    fetch_data()
    messagebox.showinfo("Sukses", "Data berhasil dihapus!")

def search_data():
    name = entry_search.get()
    if name:
        cursor.execute("SELECT * FROM attendance WHERE name LIKE ?", ('%' + name + '%',))
        rows = cursor.fetchall()
        update_treeview(rows)
    else:
        fetch_data()

def fetch_data():
    cursor.execute("SELECT * FROM attendance")
    rows = cursor.fetchall()
    update_treeview(rows)

def update_treeview(rows):
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", "end", values=row)

# GUI utama
root = Tk()
root.title("Absensi Kelas")

# Fullscreen mode
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.state('zoomed')

# Canvas untuk background
canvas = Canvas(root, width=screen_width, height=screen_height, bg="#d3e5ff")
canvas.pack(fill="both", expand=True)

# Frame Input
frame_input = Frame(canvas, bg="#f7f7f7")
canvas.create_window(screen_width // 2 - 300, 50, window=frame_input, anchor="nw")

Label(frame_input, text="Nama Siswa:", bg="#f7f7f7", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky=W)
entry_name = Entry(frame_input, font=("Arial", 12), width=30)
entry_name.grid(row=0, column=1, padx=5, pady=5)

Label(frame_input, text="Tanggal:", bg="#f7f7f7", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky=W)
entry_date = Entry(frame_input, font=("Arial", 12), width=30)
entry_date.grid(row=1, column=1, padx=5, pady=5)

Label(frame_input, text="Status (Hadir/Tidak Hadir):", bg="#f7f7f7", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky=W)
entry_status = Entry(frame_input, font=("Arial", 12), width=30)
entry_status.grid(row=2, column=1, padx=5, pady=5)

# Frame Tombol
frame_buttons = Frame(canvas, bg="#f7f7f7")
canvas.create_window(screen_width // 2 - 300, 150, window=frame_buttons, anchor="nw")

Button(frame_buttons, text="Tambah Data", command=add_data, bg="#4caf50", fg="white", font=("Arial", 12), width=15).grid(row=0, column=0, padx=5, pady=5)
Button(frame_buttons, text="Ubah Data", command=update_data, bg="#2196f3", fg="white", font=("Arial", 12), width=15).grid(row=0, column=1, padx=5, pady=5)
Button(frame_buttons, text="Hapus Data", command=delete_data, bg="#f44336", fg="white", font=("Arial", 12), width=15).grid(row=0, column=2, padx=5, pady=5)

# Frame Pencarian
frame_search = Frame(canvas, bg="#f7f7f7")
canvas.create_window(screen_width // 2 - 300, 250, window=frame_search, anchor="nw")

Label(frame_search, text="Cari Nama Siswa:", bg="#f7f7f7", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
entry_search = Entry(frame_search, font=("Arial", 12), width=30)
entry_search.grid(row=0, column=1, padx=5, pady=5)

Button(frame_search, text="Cari", command=search_data, bg="#ff9800", fg="white", font=("Arial", 12), width=15).grid(row=0, column=2, padx=5, pady=5)

# Tabel Data
tree_frame = Frame(canvas, bg="#f7f7f7")
canvas.create_window(screen_width // 2 - 300, 350, window=tree_frame, anchor="nw")

tree = ttk.Treeview(tree_frame, columns=("ID", "Nama Siswa", "Tanggal", "Status"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nama Siswa", text="Nama Siswa")
tree.heading("Tanggal", text="Tanggal")
tree.heading("Status", text="Status")

tree.column("ID", width=50, anchor=CENTER)
tree.column("Nama Siswa", width=200)
tree.column("Tanggal", width=100, anchor=CENTER)
tree.column("Status", width=150)

tree.pack()

# Load data awal
fetch_data()

# Jalankan aplikasi
root.mainloop()