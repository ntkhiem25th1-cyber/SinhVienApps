import flet as ft


def get_view(page: ft.Page):
    mini_app_overlay = ft.Container(visible=False, expand=True, bgcolor="white")

    def dong_mini_app():
        mini_app_overlay.visible = False
        mini_app_overlay.content = None
        page.update()

    def mo_app(module):
        mini_app_overlay.content = module.get_ui(page, dong_mini_app)
        mini_app_overlay.visible = True
        page.update()

    def mo_so_no(e):
        from views.trothu_views import so_no
        mo_app(so_no)

    def mo_chia_tien(e):
        from views.trothu_views import chia_tien
        mo_app(chia_tien)

    def mo_ghi_chu(e):
        from views.trothu_views import ghi_chu
        mo_app(ghi_chu)

    def mo_pomodoro(e):
        from views.trothu_views import pomodoro
        mo_app(pomodoro)

    def app_icon(emoji, ten_app, on_click_action):
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text(emoji, size=35), bgcolor="white", width=70, height=70, border_radius=18,
                    alignment=ft.Alignment(0, 0), shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color="black12")
                ),
                ft.Text(ten_app, size=12, weight="bold", color="#333333")
            ], alignment="center", horizontal_alignment="center", spacing=8),
            ink=True, border_radius=18, on_click=on_click_action
        )

    app_grid = ft.Row(
        wrap=True, spacing=25, run_spacing=20, alignment="start",
        controls=[
            app_icon("📒", "Sổ Nợ", mo_so_no),
            app_icon("💸", "Chia Tiền", mo_chia_tien),
            app_icon("📝", "Ghi Chú", mo_ghi_chu),
            app_icon("🍅", "Pomodoro", mo_pomodoro)
        ]
    )

    main_dashboard = ft.Container(
        content=ft.Column([
            ft.Text("Trợ Thủ Đắc Lực", size=26, weight="bold", color="black"),
            ft.Text("Bộ công cụ mini-apps hỗ trợ sinh viên", color="grey", size=14),
            ft.Container(height=20),
            app_grid
        ], expand=True), padding=20, expand=True
    )

    return ft.Stack([main_dashboard, mini_app_overlay], expand=True)