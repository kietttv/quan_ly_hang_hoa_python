import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date

from controllers.hang_hoa_controller import HangHoaController
from controllers.ban_hang_controller import BanHangController
from utils.view_utils import ViewUtils

class BanHangView:
    def __init__(self, parent):
        self.parent = parent
        self.hang_hoa_controller = HangHoaController()
        self.ban_hang_controller = BanHangController()
        self.ma_hang_values = []
        self.create_widgets()
        self.load_data()

    def get_ma_hang(self):
        hang_hoa_list = self.hang_hoa_controller.get_all_hang_hoa()
        self.ma_hang_map = {hang_hoa[0]: f"{hang_hoa[1]} - {hang_hoa[2]}" for hang_hoa in hang_hoa_list}
        self.mahang_combobox["values"] = list(self.ma_hang_map.values())
        self.mahang_search_combobox["values"] = list(self.ma_hang_map.values())
        self.ma_hang_values = list(self.ma_hang_map.values())

    def update_combobox(self, event, combobox, suggestion_frame, values):
        typed_text = combobox.get()

        for widget in suggestion_frame.winfo_children():
            widget.destroy()

        if typed_text == "":
            suggestion_frame.place_forget()
            return

        filtered_values = [value for value in values if typed_text.lower() in value.lower()]

        if filtered_values:
            for value in filtered_values:
                label = tk.Label(suggestion_frame, text=value, anchor="w", bg="white")
                label.pack(fill="x", padx=5, pady=2)

                label.bind("<Button-1>", lambda event, val=value: self.select_location(val, combobox, suggestion_frame))

            suggestion_frame.place(x=combobox.winfo_x(),
                                y=combobox.winfo_y() + combobox.winfo_height())
            suggestion_frame.lift()
        else:
            suggestion_frame.place_forget()

    def select_location(self, value, combobox, suggestion_frame):
        combobox.set(value)
        suggestion_frame.place_forget()

    def hide_suggestion_frame(self, suggestion_frame):
        suggestion_frame.place_forget()

    def on_mahang_selected(self, selected_value):
        selected_id = next((key for key, value in self.ma_hang_map.items() if value == selected_value), None)
        if selected_id is not None:
            return selected_id
        else:
            return None
        
    def fill_tree(self, nhap_hang_list):
        for row in self.tree.get_children():
            self.tree.delete(row)
        i = 1
        for nhap_hang in nhap_hang_list:
            stt = i
            id_ban_hang = nhap_hang[0]
            ma_hang = nhap_hang[1]
            ten_hang = nhap_hang[2]
            so_luong = nhap_hang[3]
            gia_ban = nhap_hang[4]
            ngay_ban = nhap_hang[5]
            self.tree.insert("", "end", values=(stt, ma_hang, ten_hang, so_luong, gia_ban, ngay_ban, id_ban_hang))
            i+=1    

    def load_data(self):
        self.get_ma_hang() 
        self.fill_tree(self.ban_hang_controller.get_ban_hang_by("", ""))

    def create_widgets(self):
        label = tk.Label(self.parent, text="Quản lý Bán hàng", font=("Arial", 16))
        label.pack(pady=10)

        main_frame = tk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", padx=10)

        tk.Label(left_frame, text="Thêm Hàng Hóa", font=("Arial", 14)).pack(pady=5)
        
        # self.selected_hang_id = None
        tk.Label(left_frame, text="Mã Hàng - Tên Hàng*:").pack(anchor="w", pady=5)
        self.mahang_combobox = ttk.Combobox(left_frame, width=50)
        self.mahang_combobox.pack(fill="x", pady=5)
        self.mahang_error_label = tk.Label(left_frame, text="", fg="red")
        self.mahang_error_label.pack(anchor="w")
        self.suggestion_mahang = ttk.Frame(left_frame)
        self.suggestion_mahang.place_forget()

        self.mahang_combobox.bind(
            "<KeyRelease>", 
            lambda event: self.update_combobox(event, self.mahang_combobox, self.suggestion_mahang, self.ma_hang_values)
        )
        self.mahang_combobox.bind(
            "<FocusOut>", 
            lambda event: self.hide_suggestion_frame(self.suggestion_mahang)
        )

        tk.Label(left_frame, text="Số lượng*: ").pack(anchor="w", pady=5)
        self.so_luong_entry = tk.Entry(left_frame)
        self.so_luong_entry.pack(fill="x", pady=5)
        self.soluong_error_label = tk.Label(left_frame, text="", fg="red")
        self.soluong_error_label.pack(anchor="w")

        tk.Label(left_frame, text="Giá Bán*: ").pack(anchor="w", pady=5)
        self.gia_ban_entry = tk.Entry(left_frame)
        self.gia_ban_entry.pack(fill="x", pady=5)
        self.gia_ban_error_label = tk.Label(left_frame, text="", fg="red")
        self.gia_ban_error_label.pack(anchor="w")

        tk.Label(left_frame, text="Ngày Bán*: ").pack(anchor="w", pady=5)
        self.ngay_ban_entry = DateEntry(left_frame, date_pattern="yyyy-mm-dd", state="readonly")
        self.ngay_ban_entry.pack(fill="x", pady=5)
        self.ngay_ban_error_label = tk.Label(left_frame, text="", fg="red")
        self.ngay_ban_error_label.pack(anchor="w")

        # Nút
        button_frame = tk.Frame(left_frame)
        button_frame.pack(fill="x", pady=10)

        self.add_button = tk.Button(button_frame, text="Bán Hàng", command=self.ban_hang, bg="#0091ff", fg="white")
        self.add_button.pack(side="left", expand=True, fill="x", padx=5)

        self.delete_button = tk.Button(button_frame, text="Xóa", command=self.delete_ban_hang, bg="#ff3333", fg="white")
        self.delete_button.pack_forget()

        self.clear_form_btn = tk.Button(button_frame, text="Clear Form", command=self.clear_form)
        self.clear_form_btn.pack(side="left", expand=True, fill="x", padx=5)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=10)

        search_row_frame = tk.Frame(right_frame)
        search_row_frame.pack(anchor="w")

        tk.Label(search_row_frame, text="Mã Hàng - Tên Hàng:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.mahang_search_combobox = ttk.Combobox(search_row_frame, width=30)
        self.mahang_search_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.suggestion_search_mahang = ttk.Frame(right_frame)
        self.suggestion_search_mahang.place_forget()
        self.mahang_search_combobox.bind(
            "<KeyRelease>", 
            lambda event: self.update_combobox(event, self.mahang_search_combobox, self.suggestion_search_mahang, self.ma_hang_values)
        )
        self.mahang_search_combobox.bind(
            "<FocusOut>", 
            lambda event: self.hide_suggestion_frame(self.suggestion_search_mahang)
        )

        tk.Label(search_row_frame, text="Giá Bán:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.gia_ban_search_entry = tk.Entry(search_row_frame, width=30)
        self.gia_ban_search_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.gia_ban_search_error_label = tk.Label(search_row_frame, text="", fg="red")
        self.gia_ban_search_error_label.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.search_button = tk.Button(search_row_frame, text="Tìm kiếm", command=self.search, bg="#0091ff", fg="white")
        self.search_button.grid(row=0, column=4, padx=5, pady=5, sticky="w")

        self.reset_searchs_button = tk.Button(search_row_frame, text="X", command=self.reset_search)
        self.reset_searchs_button.grid(row=0, column=5, padx=5, pady=5, sticky="w")

        tk.Label(right_frame, text="Danh Sách Bán Hàng", font=("Arial", 14)).pack(pady=5)
        self.tree = ttk.Treeview(right_frame, columns=("Stt", "MaHang", "TenHang", "SoLuong", "GiaBan", "NgayBan"), show="headings")

        self.tree.heading("Stt", text="#")
        self.tree.heading("MaHang", text="Mã Hàng")
        self.tree.heading("TenHang", text="Tên Hàng")
        self.tree.heading("SoLuong", text="Số lượng")
        self.tree.heading("GiaBan", text="Giá Bán")
        self.tree.heading("NgayBan", text="Ngày Bán")

        self.tree.column("Stt", width=100, anchor="center")
        self.tree.column("MaHang", width=100, anchor="center")
        self.tree.column("TenHang", width=200, anchor="w") 
        self.tree.column("SoLuong", width=100, anchor="w")
        self.tree.column("GiaBan", width = 100, anchor="w")
        self.tree.column("NgayBan", width = 200, anchor="w")

        style = ttk.Style()
        style.configure("Treeview",
                        font=("Helvetica", 10),
                        background="#f0f0f0", 
                        foreground="black")
        style.configure("Treeview.Heading",
                        font=("Helvetica", 12, 'bold'),
                        background="#d3d3d3",  
                        foreground="black")
        
        self.tree.bind("<ButtonRelease-1>", self.on_row_click)
        
        self.tree.pack(fill="both", expand=True, pady=5)

    def ban_hang(self):
        ma_hang = self.mahang_combobox.get()
        id_hang = self.on_mahang_selected(ma_hang)
        so_luong = self.so_luong_entry.get()
        gia_ban = self.gia_ban_entry.get()
        ngay_ban = self.ngay_ban_entry.get_date()

        if(self.form_validation(id_hang, ma_hang, so_luong, gia_ban, ngay_ban)):
            if(self.ban_hang_controller.add_ban_hang(id_hang = id_hang, so_luong = so_luong, gia_ban = gia_ban, ngay_ban=ngay_ban)):
                ViewUtils.show_info_msg("Thành Công", "Bán Hàng Thành Công!!!")
                self.load_data()
                self.clear_form()
            else:
                ViewUtils.show_error_msg("Thất Bại", "Nhập hàng thất bại!!!")    

    def cap_nhat_ban_hang(self, id_ban_hang):
        ma_hang = self.mahang_combobox.get()
        id_hang = self.on_mahang_selected(ma_hang)
        so_luong = int(self.so_luong_entry.get())
        gia_ban = float( self.gia_ban_entry.get())
        ngay_ban = self.ngay_ban_entry.get_date()

        if(self.form_validation(id_hang, ma_hang, so_luong, gia_ban, ngay_ban)):
            if(self.ban_hang_controller.update_ban_hang(
                id_ban_hang = id_ban_hang, id_hang = id_hang, so_luong = so_luong, gia_ban= gia_ban, ngay_ban=ngay_ban
                )):
                self.load_data()
                ViewUtils.show_info_msg("Thành Công", "Cập Nhật Nhập Bán Hàng Thành Công!!!")
            else:
                ViewUtils.show_error_msg("Thất Bại", "Cập Nhật Nhập Bán Hàng Thất Bại")    

    def delete_ban_hang(self, id_ban_hang):
        if(ViewUtils.show_askyesno_msg("Xóa Nhập Hàng???", "Bạn Có Chắc muốn xóa nhập hàng???")):
            self.ban_hang_controller.delete_ban_hang(id_ban_hang)
            self.clear_form()
            self.load_data()
            ViewUtils.show_info_msg("Thành Công", "Xóa Bán Hàng Thành Công!!!")

    def clear_form(self):
        self.mahang_combobox.delete(0, tk.END)
        self.so_luong_entry.delete(0, tk.END)
        self.gia_ban_entry.delete(0, tk.END)
        self.ngay_ban_entry.set_date(date.today())
        self.delete_button.pack_forget()
        self.add_button.config(text="Bán Hàng", command=self.ban_hang)

    def on_row_click(self, event):
        try:
            item = self.tree.selection()[0]
            values = self.tree.item(item, "values")

            # stt = values[0]
            ma_hang = values[1]
            ten_hang = values[2]
            so_luong = values[3]
            gia_ban = values[4]
            ngay_ban = values[5]
            id_ban_hang = values[6]

            self.mahang_combobox.delete(0, tk.END)
            self.mahang_combobox.insert(0, f"{ma_hang} - {ten_hang}")

            self.so_luong_entry.delete(0, tk.END)
            self.so_luong_entry.insert(0, so_luong)

            self.gia_ban_entry.delete(0, tk.END)
            self.gia_ban_entry.insert(0, gia_ban)

            self.ngay_ban_entry.set_date(ngay_ban)
            
            self.add_button.config(text="Cập Nhật", command=lambda: self.cap_nhat_ban_hang(id_ban_hang=id_ban_hang))
            
            self.delete_button.pack(side="left", expand=True, fill="x", padx=5)
            self.delete_button.config(command=lambda: self.delete_ban_hang(id_ban_hang=id_ban_hang))
        except Exception as e:
            pass    

    def search(self):
        id_ban = self.on_mahang_selected(self.mahang_search_combobox.get())
        gia_ban = self.gia_ban_search_entry.get()

        if(self.search_validation(gia_ban)):
            self.fill_tree(self.ban_hang_controller.get_ban_hang_by(id_ban, gia_ban))

    def reset_search(self):
        self.mahang_search_combobox.delete(0, tk.END)
        self.gia_ban_search_entry.delete(0, tk.END)
        self.gia_ban_error_label.config(text="")
        self.load_data()    

    def form_validation(self, id_hang, ma_hang, so_luong, gia_ban, ngay_ban):
        self.mahang_error_label.config(text="")
        self.soluong_error_label.config(text="")
        self.gia_ban_error_label.config(text="")
        self.ngay_ban_error_label.config(text="")

        if(ma_hang == ''):
             self.mahang_error_label.config(text="Mã hàng không được để trống")
             return False
        
        try:
            if int(so_luong) < 0:
                self.soluong_error_label.config(text="Số lượng phải là số nguyên dương")
                return False
            
            if not (self.ban_hang_controller.validation_ban_hang(id_hang, so_luong)):
                self.soluong_error_label.config(text="Số lượng hàng không đủ để thực hiện thao tác này!!!")
                return False
        except ValueError:
            if so_luong.strip() == "":
                self.soluong_error_label.config(text="Số lượng hàng không đủ để thực hiện thao tác này.")
                return False    
            if not so_luong.strip() == "":
                self.soluong_error_label.config(text="Số lượng phải là một số hợp lệ")
                return False
        
        try:
            if gia_ban.strip() == "":
                self.gia_ban_error_label.config(text="Giá nhập không được để trống")
                return False
            if float(gia_ban) < 0:
                self.gia_ban_error_label.config(text="Giá nhập phải là số dương")
                return False
        except ValueError:
            self.gia_ban_error_label.config(text="Giá nhập phải là một số hợp lệ")
            return False
        
        if(ngay_ban == ''):
             self.ngay_ban_error_label.config(text="Ngày Nhập không được để trống")
             return False
            
        return True
    
    def search_validation(self, gia_ban):
        self.gia_ban_search_error_label.config(text="")
        try:
            if float(gia_ban) < 0:
                self.gia_ban_search_error_label.config(text="Giá nhập phải là số dương")
                return False
        except ValueError:
            if not (gia_ban == ''):
                self.gia_ban_search_error_label.config(text="Giá nhập phải là một số hợp lệ")
                return False
        
        return True