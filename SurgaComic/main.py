import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import csv
import tkinter.messagebox
import os
from tkinter import filedialog

class PerpustakaanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Surga Comic App")

        self.root.attributes('-fullscreen',True)

        style = ttk.Style()
        style.element_create("Custom.TNotebook.Tab", "from", "default")
        style.layout("Black.TNotebook", [("Custom.TNotebook.Tab", {"sticky": "nswe"})])
        style.configure('Black.TNotebook.Tab', background='black', foreground='black', font=('Helvetica', 12))

        self.tab_control = ttk.Notebook(root, style='Black.TNotebook')

        self.home_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.home_tab, text="\n                               Home                               \n")
        self.create_home_page(self.home_tab)

        self.borrow_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.borrow_tab, text="\n                           Peminjaman                           \n")
        self.create_borrow_form(self.borrow_tab)

        self.return_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.return_tab, text="\n                           Pengembalian                           \n")
        self.create_return_form(self.return_tab)

        self.invoice_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.invoice_tab, text="\n                              History                              \n")
        self.create_invoice_page(self.invoice_tab)

        self.rule_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.rule_tab, text="\n                            Peraturan                            \n")
        self.create_rule_page(self.rule_tab)

        self.tab_control.pack(expand=1, fill="both")

    def read_csv_data(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        return data

    def write_csv_data(self, file_path, fieldnames, data):
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def create_home_page(self, tab):
        label = tk.Label(tab, text="Selamat Datang di Surga Comic", font=("Arial Black", 50))
        label.pack(pady=0)

        # Tambahkan fitur filter komik
        filter_label = tk.Label(tab, text="Cari Judul Komik", font=('Cascadia Code Light', 15))
        filter_label.pack(pady=5)

        filter_entry = tk.Entry(tab, justify="center", font=('Cascadia Code Semibold', 15))
        filter_entry.pack(side="top", ipadx=35, ipady=10)

        filter_button = tk.Button(tab, text="         Filter          ", font=('Cascadia Code Semibold', 16),
                                    command=lambda: self.filter_comics(filter_entry.get()))
        filter_button.pack(pady=10)

        # Frame for canvas and scrollbar
        frame_canvas = tk.Frame(tab)
        frame_canvas.pack(side="top", fill="none", expand=False)

        # Canvas
        self.canvas = tk.Canvas(frame_canvas, height=600, width=300)  # Adjust height as needed
        self.canvas.pack(side="top", fill="none", expand=False)

        # Frame inside the canvas
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((self.canvas.winfo_reqwidth() / 2, 0), window=self.frame, anchor="n")

        # Simpan semua data buku pada awal program
        self.all_book_data = self.read_csv_data('database/data_buku.csv')

        # Menampilkan semua data buku pada awal program
        self.show_all_books()

        # Tambahkan scrollbar untuk canvas
        scrollbar = tk.Scrollbar(frame_canvas, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="left", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Update tampilan setelah melakukan filter atau menampilkan semua buku
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Bind scrollbar's command to canvas's yview
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Bind mouse wheel to canvas scrolling
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))




    def read_csv_data(self, csv_file):
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        return data

    def filter_comics(self, filter_text):
        # Hapus elemen-elemen sebelumnya di dalam frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Membuat list kosong untuk menyimpan data buku yang sesuai dengan filter
        filtered_books = []

        for book in self.all_book_data:
            # Jika judul mengandung teks filter, tambahkan ke list
            if filter_text.lower() in book['Judul'].lower():
                filtered_books.append(book)

        # Menampilkan buku yang sesuai dengan filter
        self.show_books(filtered_books)

    def show_all_books(self):
        # Menampilkan semua data buku
        self.show_books(self.all_book_data)

    def show_books(self, book_data):
        for book in book_data:
            # Menampilkan buku pada frame
            label_text = f"{book['Judul']} - {book['Penulis']}"
            label = tk.Label(self.frame, text=label_text, font=('Cascadia Code Light', 10))
            label.pack()

            image_path = book.get("ImagePath", "")
            if image_path and os.path.exists(image_path):
                image = Image.open(image_path)
                image.thumbnail((420, 420))
                photo = ImageTk.PhotoImage(image)
                img_label = tk.Label(self.frame, image=photo)
                img_label.image = photo
                img_label.pack()

            label_text = f"\n"
            label = tk.Label(self.frame, text=label_text)
            label.pack()

        # Update tampilan setelah melakukan filter atau menampilkan semua buku
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        


        

    def create_borrow_form(self, tab):
        label = tk.Label(tab, text="Form Peminjaman", font=('Arial Black', 50))
        label.pack()

        style = ttk.Style()
        style.configure('TEntry', foreground='green')

        nama_label = tk.Label(tab, text="Nama", font=('Cascadia Code Light', 10))
        nama_label.pack()
        nama_entry = tk.Entry(tab, justify="center", font=('Cascadia Code Semibold', 15))
        nama_entry.focus_force()
        nama_entry.pack(side="top", ipadx=35, ipady=10)

        nomor_label = tk.Label(tab, text="Nomor Member", font=('Cascadia Code Light', 10))
        nomor_label.pack()
        nomor_entry = tk.Entry(tab, justify="center", font=('Cascadia Code Semibold', 15))
        nomor_entry.focus_force()
        nomor_entry.pack(side="top", ipadx=35, ipady=10)

        book_data = self.read_csv_data('database/data_buku.csv')
        judul_label = tk.Label(tab, text="Pilih Judul Komik", font=('Cascadia Code Light', 10))
        judul_label.pack()
        judul_var = tk.StringVar()
        judul_dropdown = ttk.Combobox(tab, textvariable=judul_var, values=[book['Judul'] for book in book_data],
                                      justify="center", font=('Cascadia Code Semibold', 10))
        judul_dropdown.pack(side="top", ipadx=300, ipady=8)

        pinjam_button = tk.Button(tab, text="       Pinjam       ", font=('Cascadia Code Semibold', 25),
                                  command=lambda: self.pinjam_buku(nama_entry.get(), nomor_entry.get(), judul_var.get()))
        pinjam_button.pack(pady=10)

    def pinjam_buku(self, nama, nomor_mahasiswa, judul):
        if nama and nomor_mahasiswa and judul:
            borrow_data = self.read_csv_data('database/data_peminjaman.csv')

            borrow_data.append({'Nama': nama, 'Nomor Mahasiswa': nomor_mahasiswa, 'Judul Buku': judul, 'Status': 'Dipinjam'})

            self.write_csv_data('database/data_peminjaman.csv', fieldnames=['Nama', 'Nomor Mahasiswa', 'Judul Buku', 'Status'],
                                data=borrow_data)

            tkinter.messagebox.showinfo("Sukses", "Peminjaman berhasil!")

    def create_return_form(self, tab):
        self.return_tab = tab
        label = tk.Label(tab, text="Form Pengembalian", font=('Arial Black', 50))
        label.pack(pady=10)

        nama_label = tk.Label(tab, text="Nama", font=('Cascadia Code Light', 10))
        nama_label.pack()
        nama_entry = tk.Entry(tab, justify="center", font=('Cascadia Code Semibold', 15))
        nama_entry.focus_force()
        nama_entry.pack(side="top", ipadx=35, ipady=10)

        nomor_label = tk.Label(tab, text="Nomor Member", font=('Cascadia Code Light', 10))
        nomor_label.pack()
        nomor_entry = tk.Entry(tab, justify="center", font=('Cascadia Code Semibold', 15))
        nomor_entry.focus_force()
        nomor_entry.pack(side="top", ipadx=35, ipady=10)

        nomor_label = tk.Label(tab, text="", font=('Cascadia Code Light', 10))
        nomor_label.pack()

        update_button = tk.Button(tab, text="Konfirmasi", font=('Cascadia Code Semibold', 10), command=lambda: self.update_dropdown(judul_dropdown, nama_entry.get(), nomor_entry.get()))
        update_button.pack()

        judul_label = tk.Label(tab, text="\nPilih Judul Buku", font=('Cascadia Code Light', 10))
        judul_label.pack()
        judul_var = tk.StringVar()
        judul_dropdown = ttk.Combobox(tab, textvariable=judul_var, justify="center", font=('Cascadia Code Semibold', 10))
        judul_dropdown.pack(side="top", ipadx=300, ipady=8)

        kembalikan_button = tk.Button(tab, text="     Kembalikan     ", font=('Cascadia Code Semibold', 25), command=lambda: self.kembalikan_buku(nama_entry.get(), nomor_entry.get(), judul_var.get()))
        kembalikan_button.pack(pady=10)

    def update_dropdown(self, judul_dropdown, nama, nomor_mahasiswa):
        return_data = self.read_csv_data('database/data_peminjaman.csv')
        dipinjam_books = [book['Judul Buku'] for book in return_data if
                          book['Nama'] == nama and book['Nomor Mahasiswa'] == nomor_mahasiswa and book['Status'] == 'Dipinjam']
        judul_dropdown['values'] = dipinjam_books

        judul_dropdown = ttk.Combobox(tab, textvariable=judul_var)
        judul_dropdown.pack()

        update_button = tk.Button(tab, text="Update Dropdown", command=update_dropdown)
        update_button.pack()

    def kembalikan_buku(self, nama, nomor_mahasiswa, judul):
        if nama and nomor_mahasiswa and judul:
            borrow_data = self.read_csv_data('database/data_peminjaman.csv')

            for book in borrow_data:
                if book['Nama'] == nama and book['Nomor Mahasiswa'] == nomor_mahasiswa and book['Judul Buku'] == judul and book['Status'] == 'Dipinjam':
                    book['Status'] = 'Dikembalikan'

            self.write_csv_data('database/data_peminjaman.csv', fieldnames=['Nama', 'Nomor Mahasiswa', 'Judul Buku', 'Status'], data=borrow_data)

            tkinter.messagebox.showinfo("Sukses", "Pengembalian berhasil!")

            judul_dropdown = self.return_tab.children["!frame2"].children["!combobox"]
            self.update_dropdown(judul_dropdown, nama, nomor_mahasiswa)


    def create_invoice_page(self, tab):
        label = tk.Label(tab, text="Cetak History", font=('Arial Black', 50))
        label.pack(pady=10)

        nama_label = tk.Label(tab, text="Nama", font=('Cascadia Code Light', 10))
        nama_label.pack()
        nama_entry = tk.Entry(tab, justify="center", font=('Cascadia Code Semibold', 15))
        nama_entry.focus_force()
        nama_entry.pack(side="top", ipadx=35, ipady=10)

        nomor_label = tk.Label(tab, text="Nomor Member", font=('Cascadia Code Light', 10))
        nomor_label.pack()
        nomor_entry = tk.Entry(tab, justify="center", font=('Cascadia Code Semibold', 15))
        nomor_entry.focus_force()
        nomor_entry.pack(side="top", ipadx=35, ipady=10)

        cetak_button = tk.Button(tab, text="   Cetak History   ", font=('Cascadia Code Semibold', 25),
                                 command=lambda: self.cetak_invoice(nama_entry.get(), nomor_entry.get()))
        cetak_button.pack(pady=10)

    def cetak_invoice(self, nama, nomor_mahasiswa):
        if nama and nomor_mahasiswa:
            borrow_data = self.read_csv_data('database/data_peminjaman.csv')

            filtered_data = [book for book in borrow_data if book['Nama'] == nama and book[
                'Nomor Mahasiswa'] == nomor_mahasiswa]

            message = "Daftar Buku:\n"
            for book in filtered_data:
                message += f"{book['Judul Buku']} - Status: {book['Status']}\n"

            tkinter.messagebox.showinfo("History", message)

    def create_rule_page(self, tab):
        # Read text from a text file
        label = tk.Label(tab, text="Peraturan Surga Comic", font=("Arial Black", 50))
        label.pack(pady=0)

        try:
            with open('database/peraturan.txt', 'r', encoding='utf-8') as file:
                peraturan_text = file.read()
        except FileNotFoundError:
            peraturan_text = "Peraturan file not found."

        # Display the text in a label
        label = tk.Label(tab, text=peraturan_text, justify="left", font=('Cascadia Code Extralight', 10))
        label.pack(pady=0)

if __name__ == "__main__":
    root = tk.Tk()
    app = PerpustakaanApp(root)
    root.mainloop()
