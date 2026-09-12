import flet as ft
import core_db
from datetime import datetime


def get_ui(page: ft.Page, on_back):
    core_db.init_sono_db()

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

    txt_ten = ft.TextField(label="Tên chủ nợ / Người mượn", bgcolor="#F2F2F7", border_color="transparent", filled=True)
    txt_sotien = ft.TextField(label="Số tiền (đ)", on_change=auto_format_money, keyboard_type="number",
                              bgcolor="#F2F2F7", border_color="transparent", filled=True)
    drop_loai = ft.Dropdown(label="Phân loại",
                            options=[ft.dropdown.Option("Mình đi mượn"), ft.dropdown.Option("Mình cho vay")],
                            bgcolor="#F2F2F7", border_color="transparent", filled=True)
    txt_hantra = ft.TextField(label="Hạn trả (dd/mm/yyyy)", value=datetime.now().strftime("%d/%m/%Y"),
                              bgcolor="#F2F2F7", border_color="transparent", filled=True)
    txt_error = ft.Text("", color="red", size=13, visible=False, italic=True)

    # ĐỔI LISTVIEW THÀNH COLUMN ĐỂ CUỘN MƯỢT TOÀN TRANG
    list_no = ft.Column(spacing=10)

    def phan_tich_do_nguy_hiem(sotien, loai, hantra_str):
        so_du = core_db.tinh_tong_so_du()
        try:
            hantra_date = datetime.strptime(hantra_str, "%d/%m/%Y")
            days_left = (hantra_date.date() - datetime.now().date()).days
        except ValueError:
            return "Sai định dạng ngày", "grey"

        if loai == "Mình cho vay":
            if days_left < 0:
                return f"Quá hạn {abs(days_left)} ngày! Đòi lẹ 🔴", "red"
            elif days_left <= 3:
                return "Sắp đến hạn đòi 🟠", "orange"
            else:
                return f"Còn {days_left} ngày 🟢", "green"
        else:
            if days_left < 0: return "💀 Nợ quá hạn! Trốn mau!", "red"
            if so_du >= sotien:
                if days_left <= 3:
                    return "🔵 Đủ lúa rồi, trả gấp đi!", "#007AFF"
                else:
                    return "🟢 Ví đủ tiền, an toàn", "green"
            else:
                if days_left <= 3:
                    return "🔴 Báo động đỏ: Cháy túi!", "red"
                else:
                    return "🟠 Thiếu tiền! Cày cuốc đi bro", "orange"

    def hien_thi_chi_tiet(item):
        id_no, ten, sotien, loai, hantra, trangthai = item
        msg_nguyhiem, color_code = phan_tich_do_nguy_hiem(sotien, loai, hantra)

        dlg = ft.AlertDialog(
            title=ft.Text("Chi Tiết Khoản", weight="bold"),
            content=ft.Column([
                ft.Text(f"👤 Đối tác: {ten}", size=15),
                ft.Text(f"💰 Số tiền: {sotien:,.0f} đ".replace(",", "."), size=18, weight="bold", color="#007AFF"),
                ft.Text(f"🏷️ Loại: {loai}", size=15),
                ft.Text(f"📅 Hạn trả: {hantra}", size=15),
                ft.Text(f"🚨 Trạng thái: {msg_nguyhiem}", size=15, color=color_code, weight="bold")
            ], tight=True),
            actions=[ft.TextButton("Đóng", on_click=lambda e: dong_dlg(dlg))]
        )

        def dong_dlg(d):
            d.open = False
            page.update()

        try:
            page.open(dlg)
        except AttributeError:
            page.dialog = dlg
            dlg.open = True
            page.update()

    def load_data():
        list_no.controls.clear()
        data = core_db.lay_tat_ca_no()

        if not data:
            list_no.controls.append(ft.Text("Chưa có khoản nợ nào. Đỉnh! 😎", color="grey"))
        else:
            for item in data:
                id_no, ten, sotien, loai, hantra, trangthai = item
                msg_nguyhiem, color_code = phan_tich_do_nguy_hiem(sotien, loai, hantra)

                loai_icon = "⬇️ Mượn của:" if loai == "Mình đi mượn" else "⬆️ Cho vay:"
                sotien_str = f"{sotien:,.0f} đ".replace(",", ".")

                def make_delete_func(item_id):
                    return lambda e: xoa_no(item_id)

                def make_detail_func(it):
                    return lambda e: hien_thi_chi_tiet(it)

                row_ui = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(loai_icon, size=12, color="grey"),
                            ft.Text(ten, weight="bold", size=15),
                            ft.Container(expand=True),
                            ft.GestureDetector(
                                on_tap=make_delete_func(id_no),
                                content=ft.Text("🗑️", size=18)
                            )
                        ]),
                        ft.Text(sotien_str, size=20, weight="bold", color="black"),
                        ft.Container(height=1, bgcolor="#E5E5EA"),
                        ft.Row([
                            ft.Text(f"Hạn: {hantra}", size=13),
                            ft.Text(msg_nguyhiem, size=13, weight="bold", color=color_code)
                        ], alignment="spaceBetween")
                    ]),
                    bgcolor="white", padding=15, border_radius=12,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=8, color="black12"),
                    ink=True,
                    on_click=make_detail_func(item)  # Bấm là bung chi tiết
                )
                list_no.controls.append(row_ui)
        page.update()

    def xoa_no(id_no):
        core_db.xoa_khoan_no(id_no)
        load_data()

    def luu_no(e):
        txt_error.visible = False
        try:
            sotien = lay_so_thuc(txt_sotien.value)
            if sotien <= 0:
                txt_error.value = "⚠️ Tiền nợ phải > 0!"
                txt_error.visible = True
                page.update()
                return
            if not drop_loai.value or not txt_ten.value:
                txt_error.value = "⚠️ Điền đủ tên và phân loại nhé bro!"
                txt_error.visible = True
                page.update()
                return

            datetime.strptime(txt_hantra.value.strip(), "%d/%m/%Y")
            core_db.them_khoan_no(txt_ten.value.strip(), sotien, drop_loai.value, txt_hantra.value.strip())

            txt_sotien.value = ""
            txt_ten.value = ""
            drop_loai.value = None
            load_data()
        except ValueError:
            txt_error.value = "⚠️ Hạn trả phải đúng định dạng dd/mm/yyyy"
            txt_error.visible = True
            page.update()

    layout = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.TextButton("← Quay lại", on_click=lambda e: on_back(), style=ft.ButtonStyle(color="#007AFF")),
                ft.Text("Quản Lý Nợ", size=18, weight="bold"),
                ft.Container(width=50)
            ], alignment="spaceBetween"),
            ft.Container(
                content=ft.Column([
                    ft.Text("Thêm khoản mới", weight="bold"),
                    txt_ten, txt_sotien, drop_loai, txt_hantra, txt_error,
                    ft.ElevatedButton("Lưu Khoản Nợ", on_click=luu_no, bgcolor="#007AFF", color="white", expand=True)
                ], tight=True),
                bgcolor="white", padding=15, border_radius=16,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black5")
            ),
            ft.Container(height=10),
            ft.Text("Danh sách nợ", weight="bold", size=16),
            list_no
        ], expand=True, scroll="auto"),  # BẬT CUỘN TOÀN TRANG Ở ĐÂY
        bgcolor="#F8F8F8", padding=20, expand=True
    )

    load_data()
    return layout