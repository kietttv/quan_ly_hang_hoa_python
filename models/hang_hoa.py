from models.database import Database

class HangHoa:
    def __init__(self,):
        self.db = Database()
        self.create_table()

    def create_table(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS HangHoa (
                IdHang INTEGER PRIMARY KEY AUTOINCREMENT,       
                MaHang TEXT NOT NULL UNIQUE,
                TenHang TEXT NOT NULL UNIQUE,
                MoTa TEXT,
                HinhAnh TEXT,
                Status TEXT DEFAULT ""        
            )
        """)

    def add_hanghoa(self, ma_hang, ten_hang, mo_ta, hinh_anh):
        self.db.execute("INSERT INTO HangHoa (MaHang, TenHang, MoTa, HinhAnh) VALUES (?, ?, ?, ?)", (ma_hang, ten_hang, mo_ta, hinh_anh)) 

    def update_hang_hoa(self, id_hang,ma_hang, ten_hang, mo_ta, hinh_anh):
        self.db.execute(f"""
            UPDATE HangHoa
            SET
                MaHang = "{ma_hang}",
                TenHang = "{ten_hang}",
                MoTa = "{mo_ta}",
                HinhAnh = "{hinh_anh}"
            WHERE
                IdHang = {id_hang}
                        """)  
        # self.db.commit()      

    def hard_delete_hang_hoa(self, id_hang):
        self.db.execute("DELETE FROM NhapHang WHERE IdHang = ?", (id_hang,))
        self.db.execute("DELETE FROM BanHang WHERE IdHang = ?", (id_hang,))
        self.db.execute("DELETE FROM HangHoa WHERE IdHang = ?", (id_hang,))

    def soft_delete_hanh_hoa(self, id):
        self.db.execute(f"""
            UPDATE HangHoa
            SET
                Status = "deleted"
            WHERE
                IdHang = {id}
                        """)

    def get_all_hanghoa(self):
        self.db.execute("""
            SELECT 
                h.IdHang, 
                h.MaHang, 
                h.TenHang, 
                COALESCE(SUM(nh.SoLuong), 0) - COALESCE(SUM(bh.SoLuong), 0) AS SoLuong, 
                h.MoTa,
                h.HinhAnh
            FROM 
                HangHoa h
            LEFT JOIN NhapHang nh ON h.IdHang = nh.IdHang
            LEFT JOIN BanHang bh ON h.IdHang = bh.IdHang
            WHERE
                h.Status != "deleted"
            GROUP BY 
                h.IdHang, 
                h.MaHang, 
                h.TenHang, 
                h.MoTa,
                h.HinhAnh;
                        """)
        return self.db.fetchall()
    
    def get_hanghoa_by(self, keyword):
        self.db.execute(f"""
                SELECT 
                    h.IdHang, 
                    h.MaHang, 
                    h.TenHang, 
                    COALESCE(SUM(nh.SoLuong), 0) - COALESCE(SUM(bh.SoLuong), 0) AS SoLuong, 
                    h.MoTa,
                    h.HinhAnh
                FROM 
                    HangHoa h
                LEFT JOIN NhapHang nh ON h.IdHang = nh.IdHang
                LEFT JOIN BanHang bh ON h.IdHang = bh.IdHang
                WHERE
                    h.Status != "deleted"
                    AND (LOWER(h.MaHang) LIKE LOWER('%{keyword}%') OR LOWER(h.TenHang) LIKE LOWER('%{keyword}%'))
                GROUP BY 
                    h.IdHang, 
                    h.MaHang, 
                    h.TenHang, 
                    h.MoTa,
                    h.HinhAnh;
                        """)
        return self.db.fetchall()
