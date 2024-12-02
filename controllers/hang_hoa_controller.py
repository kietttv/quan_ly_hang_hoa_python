import os
from PIL import Image, ImageTk

from models.hang_hoa import HangHoa

class HangHoaController:
    def __init__(self):
        self.hang_hoa_model = HangHoa()

    def save_img(self, file_path, ma_hang):
        if file_path:
            try:
                img = Image.open(file_path)
                img = img.resize((150, 150), Image.LANCZOS) 
                img_name = f"{ma_hang}.png"
                img.save(f"resources/images/{img_name}")
                return img_name
            except Exception as e:
                return None

    def delete_image(self, image_path):
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"Đã xóa hình ảnh: {image_path}")
                return True
            else:
                print(f"Hình ảnh không tồn tại: {image_path}")
                return False
        except Exception as e:
            print(f"Lỗi khi xóa hình ảnh: {e}")
            return False            

    def add_hang_hoa(self, ma_hang, ten_hang, mo_ta, hinh_anh):
        try:
            self.hang_hoa_model.add_hanghoa(ma_hang, ten_hang, mo_ta, f"{ma_hang}.png")
            self.save_img(hinh_anh, ma_hang)
            return True
        except Exception as e:
            return False
        
    def get_all_hang_hoa(self):
        try:
            return self.hang_hoa_model.get_all_hanghoa()
        except Exception as e:
            print(e)
            return []
        
    def update_hang_hoa(self, id_hang,ma_hang, ten_hang, mo_ta, hinh_anh):
        try:
            self.hang_hoa_model.update_hang_hoa(id_hang, ma_hang, ten_hang, mo_ta, self.save_img(hinh_anh, ma_hang))
            return True
        except Exception as e:
            return False

    def hard_delete_hanghoa(self, id, img_path):
        try:
            self.hang_hoa_model.hard_delete_hang_hoa(id)
            self.delete_image(img_path)
            return True
        except Exception as e:
            print(e)
            return False
        
    def soft_delete_hang_hoa(self, id):
        try:
            self.hang_hoa_model.soft_delete_hanh_hoa(id)
            return True
        except Exception as e:
            print(e)
            return False    
        
    def get_hang_hoa_by(self, keyword):
        try:
            return self.hang_hoa_model.get_hanghoa_by(keyword)
        except Exception as e:
            print(e)
            return []   