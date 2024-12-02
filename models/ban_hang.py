from models.database import Database

class BanHang:
    def __init__(self):
        self.db = Database()
        self.create_table()

    def create_table(self):
        """Tạo bảng BanHang nếu chưa có"""
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS BanHang (
                MaBan INTEGER PRIMARY KEY AUTOINCREMENT,
                IdHang INTEGER NOT NULL,
                SoLuong INTEGER NOT NULL,
                GiaBan REAL NOT NULL,
                NgayBan TEXT NOT NULL,
                FOREIGN KEY (IdHang) REFERENCES HangHoa(IdHang)
            )
        """)

    def add_banhang(self, id_hang, so_luong, gia_ban, ngay_ban):
        self.db.execute("""
            INSERT INTO BanHang (IdHang, SoLuong, GiaBan, NgayBan)
            VALUES (?, ?, ?, ?)
        """, (id_hang, so_luong, gia_ban, ngay_ban))

    def update_banhang(self, id_ban_hang, id_hang, so_luong, gia_ban, ngay_ban):
        query = f"""
            UPDATE 
                BanHang
            SET
                IdHang = {id_hang},
                SoLuong = {so_luong},
                GiaBan = {gia_ban},
                NgayBan = "{ngay_ban}"
            WHERE 
                MaBan = {id_ban_hang}
                """
        self.db.execute(query = query) 

    def delete_banhang(self, id_ban_hang):
        self.db.execute(f"""
            DELETE FROM
                BanHang
            WHERE 
                MaBan =  {id_ban_hang}
                        """)        
        
    def get_all_banhang(self):
        self.db.execute("""
            SELECT 
                nh.MaBan,        
                h.MaHang,
                h.TenHang,
                bh.SoLuong,
                bh.GiaBan,
                bh.NgayBan
            FROM 
                BanHang bh
            JOIN 
                HangHoa h
            ON 
                bh.IdHang = h.IdHang
            WHERE 
                h.Status != "deleted";
                        """)
        return self.db.fetchall()
    
    def get_ban_hang_by(self, id_hang, gia_nhap):
        query = """
            SELECT 
                bh.MaBan,        
                h.MaHang,
                h.TenHang,
                bh.SoLuong,
                bh.GiaBan,
                bh.NgayBan
            FROM 
                BanHang bh
            JOIN 
                HangHoa h
            ON 
                bh.IdHang = h.IdHang
            WHERE 
                h.Status != "deleted"
                AND (? IS NULL OR h.IdHang = ?)
                AND (? IS NULL OR bh.GiaBan = ?);
        """
        self.db.execute(query, (id_hang, id_hang, gia_nhap, gia_nhap))
        return self.db.fetchall()

    def get_banhang_by_mahang(self, ma_hang):
        self.db.execute("SELECT * FROM BanHang WHERE MaHang = ?", (ma_hang,))
        return self.db.fetchall()

    def get_total_sales(self, ma_hang):
        self.db.execute("""
            SELECT SUM(SoLuong * GiaBan) FROM BanHang WHERE MaHang = ?
        """, (ma_hang,))
        return self.db.fetchall()[0][0] or 0
    
    def validate_ban_hang(self, id_hang, so_luong):
        try:
            query = """
                SELECT 
                    COALESCE(SUM(nh.SoLuong), 0) - COALESCE(SUM(bh.SoLuong), 0) AS SoLuongTon
                FROM 
                    HangHoa h
                LEFT JOIN NhapHang nh ON h.IdHang = nh.IdHang
                LEFT JOIN BanHang bh ON h.IdHang = bh.IdHang
                WHERE 
                    h.IdHang = ?
                GROUP BY 
                    h.IdHang;
            """
            self.db.execute(query, (id_hang,))
            stock_quantity = self.db.fetchone()[0]

            print(stock_quantity)

            if stock_quantity >= float(so_luong):
                return True
            else:
                return False
        except Exception as e:
            return False
