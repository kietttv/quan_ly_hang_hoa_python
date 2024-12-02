from models.ban_hang import BanHang

class BanHangController:
    def __init__(self):
        self.ban_hang_model = BanHang()

    def add_ban_hang(self, id_hang, so_luong, gia_ban, ngay_ban):
        try:
            self.ban_hang_model.add_banhang(id_hang, so_luong, gia_ban, ngay_ban)    
            return True
        except Exception as e:
            return False

    def update_ban_hang(self, id_ban_hang, id_hang, so_luong, gia_ban, ngay_ban):
        try:
            self.ban_hang_model.update_banhang(id_ban_hang = id_ban_hang, id_hang = id_hang, so_luong = so_luong, gia_ban= gia_ban, ngay_ban= ngay_ban)
            return True
        except Exception as e:
            print(e)
            return False

    def delete_ban_hang(self, id_ban_hang):
        try:
            self.ban_hang_model.delete_banhang(id_ban_hang)    
            return True
        except Exception as e:
            return False
        
    def get_ban_hang_by(self, id_hang, gia_ban):
        try:
            if id_hang == "" or id_hang is None:
                id_hang = None
            if gia_ban == "" or gia_ban is None:
                gia_ban = None
            return self.ban_hang_model.get_ban_hang_by(id_hang, gia_ban)
        except Exception as e:
            print(e)
            return []
        
    def validation_ban_hang(self, id_hang, so_luong):
        return self.ban_hang_model.validate_ban_hang(id_hang, so_luong)
    

        

