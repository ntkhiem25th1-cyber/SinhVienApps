import sqlite3
from datetime import datetime

DB_NAME = "sinhvien_finance.db"


# ==========================================
# KHỞI TẠO CÁC BẢNG DỮ LIỆU
# ==========================================
def init_sono_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS SoNo (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    TenNguoi TEXT,
                    SoTien REAL,
                    Loai TEXT,
                    HanTra TEXT,
                    TrangThai INTEGER
                )''')
    conn.commit()
    conn.close()


def init_ghichu_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS GhiChuApp (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    NoiDung TEXT,
                    NgayTao TEXT
                )''')
    conn.commit()
    conn.close()


def init_db():
    init_sono_db()
    init_ghichu_db()

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Bảng Ví
    c.execute('''CREATE TABLE IF NOT EXISTS GiaoDich (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    SoTien REAL,
                    Loai TEXT,
                    DanhMuc TEXT,
                    GhiChu TEXT,
                    NgayTao TEXT
                )''')

    # Bảng Chấm Công
    c.execute('''CREATE TABLE IF NOT EXISTS CaLam (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    NgayLam TEXT,
                    SoGio REAL
                )''')

    # Bảng Cài đặt lương
    c.execute('''CREATE TABLE IF NOT EXISTS CaiDatLuong (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    LuongCoBan REAL,
                    LuongGio REAL,
                    GioChuan REAL
                )''')

    c.execute("SELECT COUNT(*) FROM CaiDatLuong")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO CaiDatLuong (LuongCoBan, LuongGio, GioChuan) VALUES (0, 0, 0)")

    conn.commit()
    conn.close()


# ==========================================
# CÁC HÀM CỦA TAB VÍ
# ==========================================
def them_giao_dich(so_tien, loai, danh_muc, ghi_chu):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    ngay_tao = datetime.now().strftime("%d/%m/%Y")
    c.execute("INSERT INTO GiaoDich (SoTien, Loai, DanhMuc, GhiChu, NgayTao) VALUES (?, ?, ?, ?, ?)",
              (so_tien, loai, danh_muc, ghi_chu, ngay_tao))
    conn.commit()
    conn.close()


def lay_tat_ca_giao_dich():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT SoTien, Loai, DanhMuc, GhiChu, NgayTao FROM GiaoDich ORDER BY Id DESC")
    data = c.fetchall()
    conn.close()
    return data


def tinh_tong_so_du():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT SUM(CASE WHEN Loai='NHAN' THEN SoTien ELSE -SoTien END) FROM GiaoDich")
    result = c.fetchone()[0]
    conn.close()
    return result if result is not None else 0


# ==========================================
# CÁC HÀM CỦA TAB CÀY CUỐC
# ==========================================
def them_ca_lam(ngay, so_gio):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO CaLam (NgayLam, SoGio) VALUES (?, ?)", (ngay, so_gio))
    conn.commit()
    conn.close()


def lay_tat_ca_ca_lam():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT NgayLam, SoGio FROM CaLam ORDER BY Id DESC")
    data = c.fetchall()
    conn.close()
    return data


def kiem_tra_ngay_lam(ngay):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM CaLam WHERE NgayLam = ?", (ngay,))
    count = c.fetchone()[0]
    conn.close()
    return count > 0


def cap_nhat_cai_dat_luong(lcb, l1h, giochuan):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE CaiDatLuong SET LuongCoBan=?, LuongGio=?, GioChuan=? WHERE Id=1", (lcb, l1h, giochuan))
    conn.commit()
    conn.close()


def lay_cai_dat_luong():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT LuongCoBan, LuongGio, GioChuan FROM CaiDatLuong WHERE Id=1")
    data = c.fetchone()
    conn.close()
    return data if data else (0, 0, 0)


# ==========================================
# CÁC HÀM CỦA TAB TRỢ THỦ - SỔ NỢ & GHI CHÚ
# ==========================================
def them_khoan_no(ten, sotien, loai, hantra):
    init_sono_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO SoNo (TenNguoi, SoTien, Loai, HanTra, TrangThai) VALUES (?, ?, ?, ?, 0)",
              (ten, sotien, loai, hantra))
    conn.commit()
    conn.close()


def lay_tat_ca_no():
    init_sono_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT Id, TenNguoi, SoTien, Loai, HanTra, TrangThai FROM SoNo ORDER BY Id DESC")
    data = c.fetchall()
    conn.close()
    return data


def xoa_khoan_no(id_no):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM SoNo WHERE Id=?", (id_no,))
    conn.commit()
    conn.close()


def them_ghi_chu(noidung):
    init_ghichu_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO GhiChuApp (NoiDung, NgayTao) VALUES (?, ?)",
              (noidung, datetime.now().strftime("%d/%m - %H:%M")))
    conn.commit()
    conn.close()


def lay_tat_ca_ghi_chu():
    init_ghichu_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT Id, NoiDung, NgayTao FROM GhiChuApp ORDER BY Id DESC")
    data = c.fetchall()
    conn.close()
    return data


def xoa_ghi_chu(id_gc):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM GhiChuApp WHERE Id=?", (id_gc,))
    conn.commit()
    conn.close()


# ==========================================
# CÀI ĐẶT CHUNG - RESET DỮ LIỆU AN TOÀN
# ==========================================
def xoa_sach_du_lieu():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Dùng try-except bọc từng bảng để tránh gián đoạn nếu bảng chưa tồn tại
    tables = ["GiaoDich", "CaLam", "SoNo", "GhiChuApp"]
    for table in tables:
        try:
            c.execute(f"DELETE FROM {table}")
        except sqlite3.OperationalError:
            pass

    try:
        c.execute("UPDATE CaiDatLuong SET LuongCoBan=0, LuongGio=0, GioChuan=0 WHERE Id=1")
    except sqlite3.OperationalError:
        pass

    try:
        c.execute("DELETE FROM sqlite_sequence")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()
# Tự động khởi tạo toàn bộ bảng khi server import database
init_db()