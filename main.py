import flet as ft
import os
import core_db
from views import tab_vi, tab_cong, tab_trothu, tab_caidat


def main(page: ft.Page):
    core_db.init_db()
    page.title = "Ví Sinh Viên"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = "#FFFFFF"

    page.meta_tags = [
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"}
    ]

    try:
        page.window.width = 400
        page.window.height = 800
        page.window.resizable = False
        page.window.maximizable = False
    except AttributeError:
        pass

    # Danh sách hàm dựng view để gọi lại động mỗi khi chuyển tab
    view_builders = [
        tab_vi.get_view,
        tab_cong.get_view,
        tab_trothu.get_view,
        tab_caidat.get_view
    ]

    content_area = ft.Container(content=view_builders[0](page), expand=True)

    nav_icons = [
        ft.Text("👛", size=22),
        ft.Text("⏱️", size=22),
        ft.Text("🛠️", size=22),
        ft.Text("⚙️", size=22)
    ]

    nav_texts = [
        ft.Text("Ví", size=11, weight="bold", color="#007AFF"),
        ft.Text("Cày Cuốc", size=11, weight="bold", color="grey"),
        ft.Text("Trợ Thủ", size=11, weight="bold", color="grey"),
        ft.Text("Cài Đặt", size=11, weight="bold", color="grey")
    ]

    def switch_tab(index):
        # Gọi hàm dựng view mới tinh để load dữ liệu mới nhất từ Database
        content_area.content = view_builders[index](page)
        for i in range(4):
            is_active = (i == index)
            nav_texts[i].color = "#007AFF" if is_active else "grey"
        page.update()

    def make_nav_button(index):
        return ft.Container(
            content=ft.Column(
                [nav_icons[index], nav_texts[index]],
                alignment="center",
                horizontal_alignment="center",
                spacing=2
            ),
            ink=True,
            on_click=lambda e: switch_tab(index),
            padding=5,
            expand=True
        )

    bottom_bar = ft.Container(
        content=ft.Row(
            controls=[
                make_nav_button(0),
                make_nav_button(1),
                make_nav_button(2),
                make_nav_button(3),
            ],
            alignment="spaceAround"
        ),
        bgcolor="#F8F8F8",
        height=65
    )

    page.add(
        ft.Column(
            [
                content_area,
                ft.Container(height=1, bgcolor="#E5E5EA"),
                bottom_bar
            ],
            spacing=0,
            expand=True
        )
    )


if __name__ == "__main__":
    # Render sẽ cấp một cổng ngẫu nhiên qua biến môi trường PORT
    port = int(os.getenv("PORT", 8550))
    ft.run(main, port=port, view=ft.AppView.WEB_BROWSER, host="0.0.0.0")