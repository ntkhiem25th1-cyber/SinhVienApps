import flet as ft
import asyncio


def get_ui(page: ft.Page, on_back):
    state = {
        "time_left": 25 * 60,
        "is_running": False
    }

    txt_timer = ft.Text("25:00", size=70, weight="bold", color="#FF3B30")
    txt_btn = ft.Text("Bắt Đầu Trồng Cà Chua 🍅", color="white", weight="bold", size=15)

    def format_time(seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    async def countdown_loop():
        while state["is_running"] and state["time_left"] > 0:
            await asyncio.sleep(1)
            if not state["is_running"]:
                break
            state["time_left"] -= 1
            txt_timer.value = format_time(state["time_left"])
            page.update()

        if state["time_left"] <= 0:
            state["is_running"] = False
            state["time_left"] = 25 * 60
            txt_timer.value = "25:00"
            txt_btn.value = "Bắt Đầu Trồng Cà Chua 🍅"
            btn_box.bgcolor = "#FF3B30"
            page.update()

    def toggle_timer(e):
        if not state["is_running"]:
            state["is_running"] = True
            txt_btn.value = "Tạm Dừng ⏸️"
            btn_box.bgcolor = "#FF9500"
            page.update()
            # Chạy task bất đồng bộ native của Flet, không gây treo giao diện
            page.run_task(countdown_loop)
        else:
            state["is_running"] = False
            txt_btn.value = "Tiếp Tục 🍅"
            btn_box.bgcolor = "#34C759"
            page.update()

    def handle_back(e):
        state["is_running"] = False
        on_back()
        page.update()

    # Tự chế Button bằng Container, không lo Flet đổi cú pháp ElevatedButton
    btn_box = ft.Container(
        content=txt_btn,
        bgcolor="#FF3B30",
        alignment=ft.Alignment(0, 0),
        width=250,
        height=50,
        border_radius=12,
        ink=True,
        on_click=toggle_timer
    )

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.TextButton("← Quay lại", on_click=handle_back, style=ft.ButtonStyle(color="#007AFF")),
                ft.Text("Pomodoro", size=18, weight="bold"),
                ft.Container(width=50)
            ], alignment="spaceBetween"),
            ft.Container(height=50),
            ft.Container(
                content=ft.Column([
                    ft.Text("TẬP TRUNG", size=16, weight="bold", color="grey"),
                    txt_timer,
                    ft.Text("Hoàn thiện xong app rồi, ngả lưng thôi bro! 😴", size=14, color="#333333", italic=True,
                            text_align="center"),
                    ft.Container(height=30),
                    btn_box
                ], horizontal_alignment="center", alignment="center"),
                bgcolor="white", padding=40, border_radius=20, alignment=ft.Alignment(0, 0), width=float('inf'),
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color="#FF3B3030")
            )
        ], horizontal_alignment="center", scroll="auto", expand=True), # <--- Thêm scroll="auto", expand=True
        bgcolor="#F8F8F8", padding=20, expand=True
    )