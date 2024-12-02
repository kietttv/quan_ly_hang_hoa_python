import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from views.hang_hoa_view import HangHoaView
from views.nhap_hang_view import NhapHangView
from views.ban_hang_view import BanHangView

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý bán hàng")
        self.create_tabs()

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        hanghoa_tab = tk.Frame(self.notebook)
        self.notebook.add(hanghoa_tab, text="Quản lý Hàng hóa")
        self.hang_hoa_view = HangHoaView(hanghoa_tab) 

        nhaphang_tab = tk.Frame(self.notebook)
        self.notebook.add(nhaphang_tab, text="Quản lý Nhập hàng")
        self.nhap_hang_view = NhapHangView(nhaphang_tab)

        banhang_tab = tk.Frame(self.notebook)
        self.notebook.add(banhang_tab, text="Quản lý Bán hàng")
        self.ban_hang_view = BanHangView(banhang_tab)

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        current_tab = self.notebook.index(self.notebook.select())

        if current_tab == 0:
            self.hang_hoa_view.load_data()
        elif current_tab == 1:
            self.nhap_hang_view.load_data()
        elif current_tab == 2:
            self.ban_hang_view.load_data()    
