import flet as ft
import core_db
from datetime import datetime


def get_view(page: ft.Page):
    core_db.init_db()

    def auto_format_money(e):
        raw_val = "".join(filter(str.isdigit, e.control.value))
        if raw_val:
            e.control.value = "{:,}".format(int(raw_val)).replace(",", ".")
        else:
            e.control.value = ""
        e.control.update()

    def lay_so_thuc(chuoi_tien):
        if not chuoi_tien: return 0
        return float("".join(filter(str.isdigit, str(chuoi_tien))))

    txt_tong_gio = ft.Text("0 h", size=18, weight="bold", color="black")
    txt_gio_du = ft.Text("0 h", size=18, weight="bold", color="orange")
    txt_thuc_nhan = ft.Text("0 đ", size=30, weight="bold", color="green")

    txt_luong_cb = ft.TextField(label="Lương cứng (đ)", on_change=auto_format_money, bgcolor="#F2F2F7",
                                border_color="transparent", filled=True, height=50)
    txt_gio_chuan = ft.TextField(label="Số giờ chuẩn", bgcolor="#F2F2F7", border_color="transparent", filled=True,
                                 height=50)
    txt_luong_1h = ft.TextField(label="Tiền 1 giờ dư (đ)", on_change=auto_format_money, bgcolor="#F2F2F7",
                                border_color="transparent", filled=True, height=50)

    today_str = datetime.now().strftime("%d/%m/%Y")
    txt_ngay_lam = ft.TextField(value=today_str, label="Ngày làm (Hôm nay)", bgcolor="#E5E5EA",
                                border_color="transparent", filled=True, read_only=True, color="#8E8E93")

    drop_sogio = ft.Dropdown(label="Chọn ca làm",
                             options=[ft.dropdown.Option("5"), ft.dropdown.Option("8"), ft.dropdown.Option("10"),
                                      ft.dropdown.Option("Khác")], bgcolor="#F2F2F7", border_color="transparent",
                             filled=True)
    txt_sogio_khac = ft.TextField(label="Nhập số giờ tự do", visible=False, bgcolor="#F2F2F7",
                                  border_color="transparent", filled=True)
    txt_error_chamcong = ft.Text("", color="red", size=13, visible=False, italic=True)

    list_history = ft.ListView(expand=True, spacing=5, height=180)
    full_history_list = ft.ListView(expand=True, spacing=8)

    def load_data():
        lcb, l1h, giochuan = core_db.lay_cai_dat_luong()
        # ÉP TRẮNG FORM NẾU DỮ LIỆU LÀ 0
        txt_luong_cb.value = "{:,}".format(int(lcb)).replace(",", ".") if lcb > 0 else ""
        txt_luong_1h.value = "{:,}".format(int(l1h)).replace(",", ".") if l1h > 0 else ""
        txt_gio_chuan.value = str(int(giochuan)) if giochuan > 0 else ""

        ca_lam_data = core_db.lay_tat_ca_ca_lam()
        list_history.controls.clear()
        full_history_list.controls.clear()

        tong_gio = 0
        if not ca_lam_data:
            list_history.controls.append(ft.Text("Tháng này chưa có ca làm nào.", color="grey"))
        else:
            for item in ca_lam_data:
                ngay, sogio = item[0], item[1]
                tong_gio += sogio
                row_ui = ft.Container(content=ft.Row([ft.Text(f"📅 {ngay}", size=14, weight="bold"),
                                                      ft.Text(f"+ {sogio} giờ", size=14, color="#007AFF",
                                                              weight="bold")], alignment="spaceBetween"), padding=12,
                                      bgcolor="#F8F9FA", border_radius=10)
                full_history_list.controls.append(row_ui)
            for item in ca_lam_data[:4]:
                ngay, sogio = item[0], item[1]
                list_history.controls.append(
                    ft.Container(content=ft.Row([ft.Text(f"📅 {ngay}", size=14, weight="bold"),
                                                 ft.Text(f"+ {sogio} giờ", size=14, color="#007AFF", weight="bold")],
                                                alignment="spaceBetween"), padding=12, bgcolor="#F8F9FA",
                                 border_radius=10)
                )

        gio_du = max(0, tong_gio - giochuan)
        thuc_nhan = lcb + (gio_du * l1h)
        txt_tong_gio.value = f"{tong_gio} h"
        txt_gio_du.value = f"{gio_du} h"
        txt_thuc_nhan.value = f"{thuc_nhan:,.0f} đ".replace(",", ".")
        page.update()

    def luu_cai_dat(e):
        try:
            core_db.cap_nhat_cai_dat_luong(lay_so_thuc(txt_luong_cb.value), lay_so_thuc(txt_luong_1h.value),
                                           lay_so_thuc(txt_gio_chuan.value))
            load_data()
        except ValueError:
            pass

    def on_drop_sogio_change(e):
        txt_sogio_khac.visible = (drop_sogio.value == "Khác")
        if not txt_sogio_khac.visible: txt_sogio_khac.value = ""
        page.update()

    drop_sogio.on_change = on_drop_sogio_change

    def cham_cong_ngay(e):
        txt_error_chamcong.visible = False
        ngay = txt_ngay_lam.value
        if core_db.kiem_tra_ngay_lam(ngay):
            txt_error_chamcong.value = f"⚠️ Hôm nay ({ngay}) ông đã chấm công rồi!"
            txt_error_chamcong.visible = True
            page.update()
            return

        try:
            sogio = float(txt_sogio_khac.value) if drop_sogio.value == "Khác" else float(drop_sogio.value)
            if sogio <= 0 or sogio > 24:
                txt_error_chamcong.value = "⚠️ Số giờ làm phải từ 1 đến 24h!"
                txt_error_chamcong.visible = True
                page.update()
                return

            core_db.them_ca_lam(ngay, sogio)
            drop_sogio.value = None
            txt_sogio_khac.visible = False
            txt_sogio_khac.value = ""
            load_data()
        except (ValueError, TypeError):
            txt_error_chamcong.value = "⚠️ Vui lòng chọn hoặc nhập số giờ!"
            txt_error_chamcong.visible = True
            page.update()

    def dong_chi_tiet(e):
        detail_overlay.visible = False
        page.update()

    def mo_chi_tiet(e):
        detail_overlay.visible = True
        page.update()

    detail_content = ft.Container(content=ft.Column([ft.Row(
        [ft.TextButton("← Đóng", on_click=dong_chi_tiet, style=ft.ButtonStyle(color="#007AFF")),
         ft.Text("Toàn Bộ Lịch Sử", size=18, weight="bold"), ft.Container(width=50)], alignment="spaceBetween"),
                                                     ft.Container(height=10), full_history_list], expand=True),
                                  bgcolor="white", padding=20, expand=True)
    detail_overlay = ft.Container(content=detail_content, visible=False, expand=True)

    card_luong = ft.Container(content=ft.Column(
        [ft.Row([ft.Text("Tổng số giờ làm:", color="grey"), txt_tong_gio], alignment="spaceBetween"),
         ft.Row([ft.Text("Số giờ làm dư:", color="grey"), txt_gio_du], alignment="spaceBetween"),
         ft.Container(height=1, bgcolor="#E5E5EA"), ft.Text("Thực Nhận Tháng Này", size=14, color="grey"),
         txt_thuc_nhan], alignment="center", horizontal_alignment="center", spacing=8), bgcolor="white",
                              border_radius=16, padding=20,
                              shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color="black12"))

    # Nút Xóa Dữ Liệu đã được gỡ bỏ khỏi đây
    card_caidat = ft.Container(content=ft.Column(
        [ft.Text("⚙️ Cấu Hình", weight="bold"), txt_luong_cb, txt_gio_chuan, txt_luong_1h,
         ft.ElevatedButton("Lưu Cấu Hình", on_click=luu_cai_dat, bgcolor="#E8F5E9", color="#2E7D32", expand=True)],
        tight=True), bgcolor="white", border_radius=16, padding=15, expand=True,
                               shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black5"))
    card_chamcong = ft.Container(content=ft.Column(
        [ft.Text("✍️ Chấm Công", weight="bold"), txt_ngay_lam, drop_sogio, txt_sogio_khac, txt_error_chamcong,
         ft.ElevatedButton("Lưu Ca Làm", on_click=cham_cong_ngay, bgcolor="#007AFF", color="white", expand=True)],
        tight=True), bgcolor="white", border_radius=16, padding=15, expand=True,
                                 shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black5"))

    header_gan_day = ft.Row([ft.Text("Gần đây", size=18, weight="bold"),
                             ft.TextButton("Xem chi tiết ➔", style=ft.ButtonStyle(color="#007AFF"),
                                           on_click=mo_chi_tiet)], alignment="spaceBetween")
    main_scroll = ft.ListView(
        controls=[ft.Text("Cày Cuốc", size=26, weight="bold", color="black"), ft.Container(height=10), card_luong,
                  ft.Container(height=15),
                  ft.Row([card_caidat, card_chamcong], alignment="spaceBetween", vertical_alignment="start",
                         spacing=10), ft.Container(height=20), header_gan_day, list_history], expand=True, padding=20)

    load_data()
    return ft.Stack([ft.Container(content=main_scroll, expand=True), detail_overlay], expand=True)