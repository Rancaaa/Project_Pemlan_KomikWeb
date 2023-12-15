    def create_home_page(self, tab):
        # ... (existing code)

        # Tambahkan fitur filter komik
        filter_label = tk.Label(tab, text="Cari Judul Komik", font=('Cascadia Code Light', 10))
        filter_label.pack(pady=5)

        filter_entry = tk.Entry(tab, justify="center", font=('Cascadia Code Semibold', 15))
        filter_entry.pack(side="top", ipadx=35, ipady=10)

        filter_button = tk.Button(tab, text="       Filter         ", font=('Cascadia Code Semibold', 16),
                                    command=lambda: self.filter_comics(filter_entry.get()))
        filter_button.pack(pady=10)

        # Frame for canvas and scrollbar
        frame_canvas = tk.Frame(tab)
        frame_canvas.pack(side="top", fill="both", expand=True)

        # Canvas
        self.canvas = tk.Canvas(frame_canvas, height=600, width=300)  # Adjust height as needed
        self.canvas.pack(side="left", fill="both", expand=True)

        # Frame inside the canvas
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((self.canvas.winfo_reqwidth() / 2, 0), window=self.frame, anchor="n")

        # Simpan semua data buku pada awal program
        self.all_book_data = self.read_csv_data('database/data_buku.csv')

        # Menampilkan semua data buku pada awal program
        self.show_all_books()

        # Tambahkan scrollbar untuk canvas
        scrollbar = tk.Scrollbar(frame_canvas, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Update tampilan setelah melakukan filter atau menampilkan semua buku
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Bind scrollbar's command to canvas's yview
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Bind mouse wheel to canvas scrolling
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
