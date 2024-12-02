import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class ViewUtils:
    @staticmethod
    def show_error_msg(msg_title, msg_content):
        messagebox.showerror(msg_title, msg_content)

    @staticmethod
    def show_info_msg(msg_title, msg_content):
        messagebox.showinfo(msg_title, msg_content)

    @staticmethod
    def show_warning_msg(msg_title, msg_content):
        messagebox.showwarning(msg_title, msg_content)

    @staticmethod
    def show_askyesno_msg(msg_tite, msg_content):
        return messagebox.askyesno(msg_tite, msg_content)
    
    @staticmethod
    def load_image(image_path, w, h):
        if not os.path.exists(image_path):
            image_path = "resources/images/default_img.png"
        try:
            img = Image.open(image_path)
            img = img.resize((w, h), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            return img_tk
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None
        # else:
        #     print(f"Image path does not exist: {image_path}")
        #     return None
