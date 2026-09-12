import flet as ft

def get_ui(page: ft.Page, on_back):
    def auto_format_money(e):
        raw_val = "".join(filter(str.isdigit, e.control.value))
        if raw_val: e.control.value = "{:,}".format(int(raw_val)).replace(",", ".")
        else: e.control.value = ""
        e.control.update()

    def lay_so_thuc(chuoi):
        if not chuoi: return 0
        return float("".join(filter(str.isdigit, str(chuoi))))

    txt_tong = ft.TextField(label="Tổng thiệt hại (đ)", on_change=auto_format_money, keyboard_type="number", bgcolor="#F2F2F7", border_color="transparent", filled=True)
    txt_nguoi = ft.TextField(label="Số người chia", keyboard_type="number", bgcolor="#F2F2F7", border_color="transparent", filled=True)
    txt_ketqua = ft.Text("0 đ", size=35, weight="bold", color="#007AFF")
    txt_error = ft.Text("", color="red", size=13, visible=False, italic=True)

    def tinh_toan(e):
        txt_error.visible = False
        try:
            tong = lay_so_thuc(txt_tong.value)
            nguoi = int(txt_nguoi.value)
            if tong <= 0 or nguoi <= 0:
                txt_error.value = "⚠️ Nhập số đàng hoàng đi bro!"
                txt_error.visible = True
            else:
                chia = tong / nguoi
                txt_ketqua.value = f"{chia:,.0f} đ".replace(",", ".")
        except ValueError:
            txt_error.value = "⚠️ Dữ liệu không hợp lệ!"
            txt_error.visible = True
        page.update()

    return ft.Container(
        content=ft.Column([
            ft.Row([ft.TextButton("← Quay lại", on_click=lambda e: on_back(), style=ft.ButtonStyle(color="#007AFF")), ft.Text("Chia Tiền", size=18, weight="bold"), ft.Container(width=50)], alignment="spaceBetween"),
            ft.Container(
                content=ft.Column([
                    ft.Text("Nhập thông tin Bill", weight="bold"),
                    txt_tong, txt_nguoi, txt_error,
                    ft.ElevatedButton("Bổ Đồng", on_click=tinh_toan, bgcolor="#007AFF", color="white", expand=True)
                ], tight=True),
                bgcolor="white", padding=20, border_radius=16, shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black5")
            ),
            ft.Container(height=20),
            ft.Container(
                content=ft.Column([
                    ft.Text("Mỗi người phải trả:", size=14, color="grey"), txt_ketqua,
                    ft.Text("Chuyển khoản lẹ không bạn đánh!", size=12, color="grey", italic=True)
                ], horizontal_alignment="center"),
                bgcolor="#F8F9FA", padding=20, border_radius=16, alignment=ft.Alignment(0,0), width=float('inf')
            )
        ], expand=True), bgcolor="#F8F8F8", padding=20, expand=True
    )