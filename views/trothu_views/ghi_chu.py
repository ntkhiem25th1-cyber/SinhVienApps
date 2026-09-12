import flet as ft
import core_db


def get_ui(page: ft.Page, on_back):
    core_db.init_ghichu_db()

    txt_noidung = ft.TextField(label="Nhập ghi chú mới...", bgcolor="#F2F2F7", border_color="transparent", filled=True,
                               expand=True)
    list_gc = ft.ListView(expand=True, spacing=10)

    def load_data():
        list_gc.controls.clear()
        data = core_db.lay_tat_ca_ghi_chu()
        if not data:
            list_gc.controls.append(ft.Text("Chưa có ghi chú nào. Đóng máy ngủ thôi!", color="grey"))
        else:
            for item in data:
                id_gc, noidung, ngaytao = item

                def make_del(i): return lambda e: xoa_gc(i)

                list_gc.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Column(
                                [ft.Text(noidung, size=15, weight="bold"), ft.Text(ngaytao, size=11, color="grey")],
                                expand=True),
                            ft.GestureDetector(on_tap=make_del(id_gc), content=ft.Text("🗑️", size=18))
                        ], alignment="spaceBetween"),
                        bgcolor="white", padding=15, border_radius=12,
                        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black5")
                    )
                )
        page.update()

    def xoa_gc(id_gc):
        core_db.xoa_ghi_chu(id_gc)
        load_data()

    def luu_gc(e):
        if txt_noidung.value.strip():
            core_db.them_ghi_chu(txt_noidung.value.strip())
            txt_noidung.value = ""
            load_data()

    layout = ft.Container(
        content=ft.Column([
            ft.Row([ft.TextButton("← Quay lại", on_click=lambda e: on_back(), style=ft.ButtonStyle(color="#007AFF")),
                    ft.Text("Ghi Chú", size=18, weight="bold"), ft.Container(width=50)], alignment="spaceBetween"),
            ft.Row(
                [txt_noidung, ft.ElevatedButton("Lưu", on_click=luu_gc, bgcolor="#007AFF", color="white", height=50)],
                alignment="spaceBetween"),
            ft.Container(height=10), list_gc
        ], expand=True), bgcolor="#F8F8F8", padding=20, expand=True
    )
    load_data()
    return layout