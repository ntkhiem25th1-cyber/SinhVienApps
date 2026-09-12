import inspect
import threading
from datetime import datetime

_thread_local = threading.local()
_fallback_memory = {}

def _resolve_page(page=None):
    """Tự động xác định đúng phiên làm việc (Page) của từng thiết bị đang truy cập."""
    if page and hasattr(page, "client_storage"):
        return page
    if hasattr(_thread_local, "page") and _thread_local.page:
        return _thread_local.page
    frame = inspect.currentframe()
    try:
        while frame:
            if "page" in frame.f_locals:
                val = frame.f_locals["page"]
                if hasattr(val, "client_storage"):
                    return val
            if "e" in frame.f_locals:
                e_val = frame.f_locals["e"]
                if hasattr(e_val, "page") and hasattr(e_val.page, "client_storage"):
                    return e_val.page
                if hasattr(e_val, "control") and hasattr(e_val.control, "page") and hasattr(e_val.control.page, "client_storage"):
                    return e_val.control.page
            if frame.f_code.co_freevars:
                for name, cell in zip(frame.f_code.co_freevars, frame.f_closure or []):
                    if name == "page" and hasattr(cell.cell_contents, "client_storage"):
                        return cell.cell_contents
            frame = frame.f_back
    finally:
        del frame
    return None

def _get_data(key, page=None, default=None):
    p = _resolve_page(page)
    if p and hasattr(p, "client_storage"):
        val = p.client_storage.get(key)
        if val is not None:
            return val
    return _fallback_memory.get(key, default if default is not None else [])

def _set_data(key, val, page=None):
    p = _resolve_page(page)
    if p and hasattr(p, "client_storage"):
        p.client_storage.set(key, val)
    else:
        _fallback_memory[key] = val

# Khởi tạo tương thích
def init_db(page=None):
    pass

def init_sono_db():
    pass

def init_ghichu_db():
    pass

# ==========================================
# CÁC HÀM CỦA TAB VÍ
# ==========================================
def them_giao_dich(so_tien, loai, danh_muc, ghi_chu, page=None):
    items = _get_data("giao_dich", page, default=[])
    ngay_tao = datetime.now().strftime("%d/%m/%Y")
    items.insert(0, [so_tien, loai, danh_muc, ghi_chu, ngay_tao])
    _set_data("giao_dich", items, page)

def lay_tat_ca_giao_dich(page=None):
    return _get_data("giao_dich", page, default=[])

def tinh_tong_so_du(page=None):
    items = _get_data("giao_dich", page, default=[])
    return sum(item[0] if item[1] == "NHAN" else -item[0] for item in items)

# ==========================================
# CÁC HÀM CỦA TAB CÀY CUỐC
# ==========================================
def them_ca_lam(ngay, so_gio, page=None):
    items = _get_data("ca_lam", page, default=[])
    items.insert(0, [ngay, so_gio])
    _set_data("ca_lam", items, page)

def lay_tat_ca_ca_lam(page=None):
    return _get_data("ca_lam", page, default=[])

def kiem_tra_ngay_lam(ngay, page=None):
    items = _get_data("ca_lam", page, default=[])
    return any(item[0] == ngay for item in items)

def cap_nhat_cai_dat_luong(lcb, l1h, giochuan, page=None):
    _set_data("cai_dat_luong", [lcb, l1h, giochuan], page)

def lay_cai_dat_luong(page=None):
    data = _get_data("cai_dat_luong", page, default=[0, 0, 0])
    return tuple(data) if data else (0, 0, 0)

# ==========================================
# CÁC HÀM CỦA TAB TRỢ THỦ - SỔ NỢ & GHI CHÚ
# ==========================================
def them_khoan_no(ten, sotien, loai, hantra, page=None):
    items = _get_data("so_no", page, default=[])
    new_id = int(datetime.now().timestamp() * 1000)
    items.insert(0, [new_id, ten, sotien, loai, hantra, 0])
    _set_data("so_no", items, page)

def lay_tat_ca_no(page=None):
    return _get_data("so_no", page, default=[])

def xoa_khoan_no(id_no, page=None):
    items = _get_data("so_no", page, default=[])
    items = [x for x in items if x[0] != id_no]
    _set_data("so_no", items, page)

def them_ghi_chu(noidung, page=None):
    items = _get_data("ghi_chu", page, default=[])
    new_id = int(datetime.now().timestamp() * 1000)
    ngay_tao = datetime.now().strftime("%d/%m - %H:%M")
    items.insert(0, [new_id, noidung, ngay_tao])
    _set_data("ghi_chu", items, page)

def lay_tat_ca_ghi_chu(page=None):
    return _get_data("ghi_chu", page, default=[])

def xoa_ghi_chu(id_gc, page=None):
    items = _get_data("ghi_chu", page, default=[])
    items = [x for x in items if x[0] != id_gc]
    _set_data("ghi_chu", items, page)

# ==========================================
# CÀI ĐẶT CHUNG - RESET DỮ LIỆU CÁ NHÂN
# ==========================================
def xoa_sach_du_lieu(page=None):
    p = _resolve_page(page)
    if p and hasattr(p, "client_storage"):
        p.client_storage.remove("giao_dich")
        p.client_storage.remove("ca_lam")
        p.client_storage.remove("so_no")
        p.client_storage.remove("ghi_chu")
        p.client_storage.remove("cai_dat_luong")
    global _fallback_memory
    _fallback_memory = {}