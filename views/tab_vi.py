import flet as ft
import core_db
from datetime import datetime


def get_view(page: ft.Page):
    txt_sotien = ft.TextField(label="Số tiền (đ)", keyboard_type="number", bgcolor="#F2F2F7",
                              border_color="transparent", filled=True)
    drop_danhmuc = ft.Dropdown(label="Danh mục", options=[ft.dropdown.Option("Ăn uống"), ft.dropdown.Option("Học tập"),
                                                          ft.dropdown.Option("Khác")], bgcolor="#F2F2F7",
                               border_color="transparent", filled=True)
    txt_custom_danhmuc = ft.TextField(label="Nhập danh mục khác...", visible=False, bgcolor="#F2F2F7",
                                      border_color="transparent", filled=True)
    txt_ghichu = ft.TextField(label="Ghi chú (Tùy chọn)", bgcolor="#F2F2F7", border_color="transparent", filled=True)
    txt_error_vi = ft.Text("", color="red", size=13, visible=False, italic=True)

    def auto_format_money(e):
        raw_val = "".join(filter(str.isdigit, e.control.value))
        if raw_val:
            e.control.value = "{:,}".format(int(raw_val)).replace(",", ".")
        else:
            e.control.value = ""
        e.control.update()

    txt_sotien.on_change = auto_format_money

    def lay_so_thuc(chuoi):
        if not chuoi: return 0
        return float("".join(filter(str.isdigit, str(chuoi))))

    def on_danhmuc_change(e):
        txt_custom_danhmuc.visible = (drop_danhmuc.value == "Khác")
        page.update()

    drop_danhmuc.on_change = on_danhmuc_change

    loai_gd = "CHI"
    popup_title = ft.Text("Thêm Khoản Chi", size=20, weight="bold", color="#FF3B30")
    list_giaodich = ft.Column(spacing=10)
    txt_tong_so_du = ft.Text("0 đ", size=32, weight="bold", color="white")

    def dong_popup():
        popup_box.visible = False
        page.update()

    def mo_popup(loai):
        nonlocal loai_gd
        loai_gd = loai
        if loai == "NHAN":
            popup_title.value = "Thêm Tiền Nhận"
            popup_title.color = "#34C759"
            drop_danhmuc.options = [ft.dropdown.Option("Gia đình cho"), ft.dropdown.Option("Lương"),
                                    ft.dropdown.Option("Khác")]
        else:
            popup_title.value = "Thêm Khoản Chi"
            popup_title.color = "#FF3B30"
            drop_danhmuc.options = [ft.dropdown.Option("Ăn uống"), ft.dropdown.Option("Học tập"),
                                    ft.dropdown.Option("Khác")]

        txt_sotien.value = ""
        txt_ghichu.value = ""
        drop_danhmuc.value = None
        txt_custom_danhmuc.visible = False
        txt_error_vi.visible = False

        popup_box.visible = True
        page.update()

    def luu_giao_dich():
        sotien = lay_so_thuc(txt_sotien.value)
        if sotien <= 0:
            txt_error_vi.value = "⚠️ Số tiền phải lớn hơn 0!"
            txt_error_vi.visible = True
            page.update()
            return

        danhmuc = drop_danhmuc.value
        if danhmuc == "Khác":
            danhmuc = txt_custom_danhmuc.value.strip()
        if not danhmuc:
            txt_error_vi.value = "⚠️ Vui lòng chọn hoặc nhập danh mục!"
            txt_error_vi.visible = True
            page.update()
            return

        core_db.them_giao_dich(sotien, loai_gd, danhmuc, txt_ghichu.value.strip())
        dong_popup()
        load_data()

    def load_data():
        list_giaodich.controls.clear()
        sodu = core_db.tinh_tong_so_du()
        txt_tong_so_du.value = f"{sodu:,.0f} đ".replace(",", ".")

        data = core_db.lay_tat_ca_giao_dich()
        if not data:
            list_giaodich.controls.append(ft.Text("Chưa có giao dịch nào gần đây.", color="grey", italic=True))
        else:
            for item in data:
                sotien, loai, danhmuc, ghichu, ngaytao = item
                color = "#34C759" if loai == "NHAN" else "#FF3B30"
                dau = "+" if loai == "NHAN" else "-"

                list_giaodich.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text(danhmuc, weight="bold", size=15),
                                ft.Text(ngaytao, size=12, color="grey")
                            ], expand=True),
                            ft.Text(f"{dau}{sotien:,.0f} đ".replace(",", "."), weight="bold", color=color, size=15)
                        ], alignment="spaceBetween"),
                        bgcolor="white", padding=15, border_radius=12,
                        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black5")
                    )
                )
        page.update()

    # Thẻ Card ví chuẩn phong cách MVP ban đầu
    wallet_card = ft.Container(
        content=ft.Column([
            ft.Text("Số Dư Hiện Tại", size=13, weight="bold", color="#E5E5EA"),
            ft.Container(height=5),
            txt_tong_so_du,
            ft.Container(height=15),
            ft.Row([
                ft.ElevatedButton("↓ Nhận Tiền", bgcolor="white", color="#2E7D32", expand=True,
                                  on_click=lambda e: mo_popup("NHAN")),
                ft.ElevatedButton("↑ Chi Tiền", bgcolor="white", color="#FF3B30", expand=True,
                                  on_click=lambda e: mo_popup("CHI"))
            ])
        ]),
        bgcolor="#007AFF", padding=20, border_radius=20,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color="#007AFF40")
    )

    popup_box = ft.Container(
        content=ft.Column([
            popup_title, ft.Container(height=5), txt_sotien, drop_danhmuc, txt_custom_danhmuc, txt_ghichu, txt_error_vi,
            ft.Container(height=10),
            ft.Row([
                ft.ElevatedButton("Hủy", on_click=lambda e: dong_popup(),
                                  style=ft.ButtonStyle(bgcolor="#E5E5EA", color="black"), expand=True),
                ft.ElevatedButton("Lưu", on_click=lambda e: luu_giao_dich(), bgcolor="#007AFF", color="white",
                                  expand=True)
            ], alignment="spaceBetween")
        ], tight=True, spacing=12),
        bgcolor="white", padding=20, border_radius=20,
        margin=20, visible=False,
        shadow=ft.BoxShadow(spread_radius=10, blur_radius=30, color="black12")
    )

    main_layout = ft.Container(
        content=ft.Column([
            ft.Text("Ví Sinh Viên", size=26, weight="bold"),
            ft.Container(height=10),
            wallet_card,
            ft.Container(height=20),
            ft.Text("Gần đây", weight="bold", size=16),
            list_giaodich
        ], expand=True, scroll="auto"),
        padding=20, expand=True, bgcolor="#F8F8F8"
    )

    load_data()
    return ft.Stack([main_layout, popup_box], expand=True)