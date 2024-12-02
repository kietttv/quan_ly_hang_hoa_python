from models.database import Database

class NhapHang:
    def __init__(self):
        self.db = Database()
        self.create_table()

    def create_table(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS NhapHang (
                MaNhap INTEGER PRIMARY KEY AUTOINCREMENT,
                MaHang INTEGER NOT NULL,
                SoLuong INTEGER NOT NULL,
                GiaNhap REAL NOT NULL,
                NgayNhap TEXT NOT NULL,
                FOREIGN KEY (MaHang) REFERENCES HangHoa(MaHang)
            )
        """)

    def add_nhaphang(self, id_hang, so_luong, gia_nhap, ngay_nhap):
        self.db.execute("""
            INSERT INTO NhapHang (IdHang, SoLuong, GiaNhap, NgayNhap)
            VALUES (?, ?, ?, ?)
        """, (id_hang, so_luong, gia_nhap, ngay_nhap))

    def update_nhaphang(self, id_nhap_hang, id_hang, so_luong, gia_nhap, ngay_nhap):
        query = f"""
            UPDATE 
                NhapHang
            SET
                IdHang = {id_hang},
                SoLuong = {so_luong},
                GiaNhap = {gia_nhap},
                NgayNhap = "{ngay_nhap}"
            WHERE 
                MaNhap = {id_nhap_hang}
        """
        self.db.execute(query = query)

    def delete_nhaphang(self, id_nhap_hang):
        self.db.execute(f"""
            DELETE FROM
                NhapHang
            WHERE 
                MaNhap =  {id_nhap_hang}
                        """)    

    def get_all_nhaphang(self):
        self.db.execute("""
            SELECT 
                nh.MaNhap,        
                h.MaHang,
                h.TenHang,
                nh.SoLuong,
                nh.GiaNhap,
                nh.NgayNhap
            FROM 
                NhapHang nh
            JOIN 
                HangHoa h
            ON 
                nh.IdHang = h.IdHang
            WHERE 
                h.Status != "deleted";
                        """)
        return self.db.fetchall()
    
    def get_nhap_hang_by(self, id_hang, gia_nhap):
        query = """
            SELECT 
                nh.MaNhap,        
                h.MaHang,
                h.TenHang,
                nh.SoLuong,
                nh.GiaNhap,
                nh.NgayNhap
            FROM 
                NhapHang nh
            JOIN 
                HangHoa h
            ON 
                nh.IdHang = h.IdHang
            WHERE 
                h.Status != "deleted"
                AND (? IS NULL OR h.IdHang = ?)
                AND (? IS NULL OR nh.GiaNhap = ?);
        """
        self.db.execute(query, (id_hang, id_hang, gia_nhap, gia_nhap))
        return self.db.fetchall()

    def get_nhaphang_by_mahang(self, ma_hang):
        self.db.execute("SELECT * FROM NhapHang WHERE MaHang = ?", (ma_hang,))
        return self.db.fetchall()

    def get_total_quantity(self, ma_hang):
        self.db.execute("""
            SELECT SUM(SoLuong) FROM NhapHang WHERE MaHang = ?
        """, (ma_hang,))
        return self.db.fetchall()[0][0] or 0
