import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk

from controllers.hang_hoa_controller import HangHoaController
from utils.view_utils import ViewUtils


class HangHoaView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = HangHoaController()
        self.create_widgets()
        # self.apply_styles()
        self.load_default_image()
        self.load_data()

    def create_widgets(self):
        label = tk.Label(self.parent, text="Quản lý Hàng hóa", font=("Arial", 16))
        label.pack(pady=10)

        main_frame = tk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", padx=10)

        tk.Label(left_frame, text="Thêm Hàng Hóa", font=("Arial", 14)).pack(pady=5)

        tk.Label(left_frame, text="Mã Hàng*:").pack(anchor="w", pady=5)
        self.mahang_entry = tk.Entry(left_frame, width=50)
        self.mahang_entry.pack(fill="x", pady=5)
        self.mahang_error_label = tk.Label(left_frame, text="", fg="red")
        self.mahang_error_label.pack(anchor="w")

        tk.Label(left_frame, text="Tên Hàng*:").pack(anchor="w", pady=5)
        self.tenhang_entry = tk.Entry(left_frame)
        self.tenhang_entry.pack(fill="x", pady=5)
        self.tenhang_error_label = tk.Label(left_frame, text="", fg="red")
        self.tenhang_error_label.pack(anchor="w")

        tk.Label(left_frame, text="Mô Tả:").pack(anchor="w", pady=5)
        self.mota_entry = tk.Text(left_frame, height=5, width=30, wrap="word")
        self.mota_entry.pack(fill="x", pady=5)

        tk.Label(left_frame, text="Hình Ảnh:").pack(anchor="w", pady=5)
        self.image_frame = tk.Frame(left_frame)
        self.image_frame.pack(fill="x", pady=5)
        
        self.choose_image_button = tk.Button(self.image_frame, text="Chọn Hình", command=self.select_image)
        self.choose_image_button.pack(side="left")

        self.image_display = None
        self.image_label = tk.Label(self.image_frame, image=self.image_display, relief="sunken", bg="white", text="default_img.png")
        self.image_label.image = self.image_display
        self.image_label.pack(side="left", padx=10, pady=10)

        button_frame = tk.Frame(left_frame)
        button_frame.pack(fill="x", pady=10)

        self.add_button = tk.Button(button_frame, text="Thêm Hàng", command=self.add_hanghoa, bg="#0091ff", fg="white")
        self.add_button.pack(side="left", expand=True, fill="x", padx=5)

        self.delete_button = tk.Button(button_frame, text="Xóa", command=self.delete_hanghoa, bg="#ff3333", fg="white")
        self.delete_button.pack_forget()

        self.clear_form_btn = tk.Button(button_frame, text="Clear Form", command=self.clear_form)
        self.clear_form_btn.pack(side="left", expand=True, fill="x", padx=5)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=10)

        search_row_frame = tk.Frame(right_frame)
        search_row_frame.pack(anchor="w")

        tk.Label(search_row_frame, text="Mã hàng hoặc Tên hàng:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = tk.Entry(search_row_frame, width=50)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.search_button = tk.Button(search_row_frame, text="Tìm kiếm", command=self.search, bg="#0091ff", fg="white")
        self.search_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.reset_searchs_button = tk.Button(search_row_frame, text="X", command=self.reset_search)
        self.reset_searchs_button.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        tk.Label(right_frame, text="Danh Sách Hàng Hóa", font=("Arial", 14)).pack(pady=5)
        self.tree = ttk.Treeview(right_frame, columns=("Stt", "MaHang", "TenHang", "SoLuong", "MoTa"), show="headings")

        self.tree.heading("Stt", text="#")
        self.tree.heading("MaHang", text="Mã Hàng")
        self.tree.heading("TenHang", text="Tên Hàng")
        self.tree.heading("SoLuong", text="Số lượng")
        self.tree.heading("MoTa", text="Mô Tả")

        self.tree.column("Stt", width=50, anchor="center")
        self.tree.column("MaHang", width=100, anchor="center")
        self.tree.column("TenHang", width=200, anchor="w") 
        self.tree.column("SoLuong", width=100, anchor="w")
        self.tree.column("MoTa", width = 300, anchor="w")
     
        self.tree.bind("<ButtonRelease-1>", self.on_row_click)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)   

    def fill_tree(self, hang_hoa_list):
        for row in self.tree.get_children():
            self.tree.delete(row)
        i = 1
        for hang_hoa in hang_hoa_list:
            stt = i
            id_hang = hang_hoa[0]
            ma_hang = hang_hoa[1]
            ten_hang = hang_hoa[2]
            so_luong = hang_hoa[3]
            mo_ta = hang_hoa[4]
            image_name = hang_hoa[5]
            self.tree.insert("", "end", values=(stt, ma_hang, ten_hang, so_luong, mo_ta, image_name, id_hang))
            i+=1
    
    def load_data(self):
        self.fill_tree(self.controller.get_all_hang_hoa())

    def load_default_image(self):
        self.image_display = ViewUtils.load_image("resources/images/default_img.png", 150, 150)
        self.image_label.config(image=self.image_display, text="")    

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        self.show_img(file_path)

    def show_img(self, file_path):
        if file_path:
            self.image_display = ViewUtils.load_image(file_path, 150, 150)
            self.image_label.config(image=self.image_display, text= file_path)

    def add_hanghoa(self):
        ma_hang = self.mahang_entry.get()
        ten_hang = self.tenhang_entry.get()
        mo_ta = self.mota_entry.get("1.0", "end").strip()
        hinh_anh = self.image_label.cget("text")

        if(self.validation(ma_hang, ten_hang)):
            if self.controller.add_hang_hoa(ma_hang, ten_hang, mo_ta, hinh_anh):
                self.clear_form()
                self.load_data()
                ViewUtils.show_info_msg("Thành công", "Thêm hàng hóa thành công.")
            else:
                ViewUtils.show_error_msg("Lỗi", "Tên hàng không được để trống hoặc trùng lặp.")

    def on_row_click(self, event):
        try:
            item = self.tree.selection()[0]
            values = self.tree.item(item, "values")

            ma_hang = values[1] 
            ten_hang = values[2]
            # so_luong = values[3]
            mo_ta = values[4]
            img_path = f"resources/images/{values[5]}"
            id_hang = values[6]

            self.mahang_entry.delete(0, tk.END)
            self.mahang_entry.insert(0, ma_hang)

            self.tenhang_entry.delete(0, tk.END)
            self.tenhang_entry.insert(0, ten_hang)

            self.mota_entry.delete("1.0", "end")
            self.mota_entry.insert("1.0", mo_ta)
            
            self.show_img(img_path)

            self.delete_button.pack(side="left", expand=True, fill="x", padx=5)
            self.delete_button.config(command=lambda: self.delete_hanghoa(id_hang, img_path))

            self.add_button.config(text="Cập nhật", command=lambda: self.update_hang_hoa(id_hang))
        except Exception as e:
            pass    

    def clear_form(self):    
        self.mahang_entry.delete(0, tk.END)
        self.tenhang_entry.delete(0, tk.END)
        self.mota_entry.delete("1.0", "end")
        self.load_default_image()
        self.delete_button.pack_forget()
        self.add_button.config(text="Thêm Hàng", command=self.add_hanghoa)

    def update_hang_hoa(self, id):
        id_hang =  id
        ma_hang = self.mahang_entry.get()
        ten_hang = self.tenhang_entry.get()
        mo_ta = self.mota_entry.get("1.0", "end").strip()
        hinh_anh = self.image_label.cget("text")
        if(self.validation(ma_hang, ten_hang)):
            if self.controller.update_hang_hoa(id_hang, ma_hang, ten_hang, mo_ta, hinh_anh):
                self.clear_form()
                self.load_data()
                ViewUtils.show_info_msg("Thành công", "Update hàng hóa thành công.")
            else:
                ViewUtils.show_error_msg("Lỗi", "Tên và mã hàng không được để trống hoặc trùng lặp.")

    def delete_hanghoa(self, id, img_path):
        if(ViewUtils.show_askyesno_msg("Cảnh báo!!!", "Bạn có chắc chăn muốn xóa hàng hóa???")):
            # self.controller.soft_delete_hang_hoa(id)
            self.controller.hard_delete_hanghoa(id, img_path)
            self.clear_form()
            self.load_data()
            ViewUtils.show_info_msg("Thành công", "Delete hàng hóa thành công.")

    def search(self):
        keyword = self.search_entry.get()
        self.fill_tree(self.controller.get_hang_hoa_by(keyword))

    def reset_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_data()

    def validation(self, ma_hang, ten_hang):
        self.mahang_error_label.config(text="")
        self.tenhang_error_label.config(text="")
        if(ma_hang == ''):
            self.mahang_error_label.config(text="Mã hàng không được để trống!!!")
            return False
        if(ten_hang == ''):
            self.tenhang_error_label.config(text="Tên hàng không được để trống")
            return False
        return True   
