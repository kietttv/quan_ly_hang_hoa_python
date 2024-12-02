
from models.nhap_hang import NhapHang

class NhapHangController:
    def __init__(self):
        self.nhap_hang_model = NhapHang()

    def add_nhap_hang(self, id_hang, so_luong, gia_nhap, ngay_nhap):
        try:
            self.nhap_hang_model.add_nhaphang(id_hang, so_luong, gia_nhap, ngay_nhap)    
            return True
        except Exception as e:
            return False
        
    def update_nhap_hang(self, id_nhap_hang, id_hang, so_luong, gia_nhap, ngay_nhap):
        try:
            self.nhap_hang_model.update_nhaphang(id_nhap_hang = id_nhap_hang, id_hang = id_hang, so_luong = so_luong, gia_nhap = gia_nhap, ngay_nhap = ngay_nhap)
            return True
        except Exception as e:
            print(e)
            return False
        
    def delete_nhap_hang(self, id_nhap_hang):
        try:
            self.nhap_hang_model.delete_nhaphang(id_nhap_hang)    
            return True
        except Exception as e:
            print(e)
            return False

    def get_nhap_hang_by(self, id_hang, gia_nhap):
        try:
            if id_hang == "" or id_hang is None:
                id_hang = None
            if gia_nhap == "" or gia_nhap is None:
                gia_nhap = None

            return self.nhap_hang_model.get_nhap_hang_by(id_hang, gia_nhap)
        except Exception as e:
            print(e)
            return []

    def get_all_nhap_hang(self):
        try:
            return self.nhap_hang_model.get_all_nhaphang()
        except Exception as e:
            print(e)
            return []

        