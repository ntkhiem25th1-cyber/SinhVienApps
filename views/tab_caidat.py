import flet as ft
import core_db


def get_view(page: ft.Page):
    # Overlay thông báo thành công
    success_overlay = ft.Container(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Đã dọn sạch! 🧹", size=18, weight="bold", color="#34C759"),
                ft.Container(height=5),
                ft.Text("Toàn bộ dữ liệu đã được xóa sạch. Hãy tải lại trang (Refresh) để làm mới app nhé!", size=14,
                        color="#333333", text_align="center"),
                ft.Container(height=15),
                ft.ElevatedButton("Đã hiểu", on_click=lambda e: dong_success(), bgcolor="#007AFF", color="white",
                                  width=200)
            ], horizontal_alignment="center", tight=True),
            bgcolor="white", padding=25, border_radius=20, width=320,
            shadow=ft.BoxShadow(spread_radius=10, blur_radius=30, color="black26")
        ),
        alignment=ft.Alignment(0, 0),
        bgcolor="#00000066",
        visible=False,
        expand=True
    )

    # Overlay xác nhận xóa
    confirm_overlay = ft.Container(
        content=ft.Container(
            content=ft.Column([
                ft.Text("⚠️ Cảnh Báo Xóa", size=18, weight="bold", color="#FF3B30"),
                ft.Container(height=5),
                ft.Text(
                    "Hành động này sẽ xóa vĩnh viễn toàn bộ Thu/Chi, Chấm Công, Sổ Nợ và Ghi Chú. Bạn có chắc chắn muốn xóa không?",
                    size=14, color="#333333", text_align="center"),
                ft.Container(height=15),
                ft.Row([
                    ft.ElevatedButton("Hủy", on_click=lambda e: dong_confirm(),
                                      style=ft.ButtonStyle(bgcolor="#E5E5EA", color="black"), expand=True),
                    ft.ElevatedButton("Xóa Sạch", on_click=lambda e: thuc_hien_xoa(), bgcolor="#FF3B30", color="white",
                                      expand=True)
                ], alignment="spaceBetween")
            ], horizontal_alignment="center", tight=True),
            bgcolor="white", padding=25, border_radius=20, width=320,
            shadow=ft.BoxShadow(spread_radius=10, blur_radius=30, color="black26")
        ),
        alignment=ft.Alignment(0, 0),
        bgcolor="#00000066",
        visible=False,
        expand=True
    )

    def mo_confirm(e):
        confirm_overlay.visible = True
        page.update()

    def dong_confirm():
        confirm_overlay.visible = False
        page.update()

    def thuc_hien_xoa():
        core_db.xoa_sach_du_lieu()
        confirm_overlay.visible = False
        success_overlay.visible = True
        page.update()

    def dong_success():
        success_overlay.visible = False
        page.update()

    dev_card = ft.Container(
        content=ft.Column([
            ft.Text("THÔNG TIN NHÀ PHÁT TRIỂN", size=13, weight="bold", color="grey"),
            ft.Container(height=5),
            ft.Text("Nguyễn Thái Khiêm", size=22, weight="bold", color="#007AFF"),
            ft.Text("👨‍💻 Kỹ sư Phần mềm | Sinh viên CNTT", size=14, color="#333333"),
            ft.Text("🏛️ Đại học Đồng Tháp", size=14, color="#333333"),
            ft.Text("📞 Hỗ trợ kỹ thuật: 0853686188", size=14, color="#333333"),
        ], spacing=5),
        bgcolor="white", padding=20, border_radius=16,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color="black12")
    )

    danger_zone = ft.Container(
        content=ft.Column([
            ft.Text("VÙNG NGUY HIỂM", size=13, weight="bold", color="red"),
            ft.Container(height=5),
            ft.Text("Xóa sạch toàn bộ dữ liệu người dùng trên hệ thống.", size=13, color="grey"),
            ft.Container(height=10),
            ft.ElevatedButton("Xóa Sạch Dữ Liệu", on_click=mo_confirm, bgcolor="#FF3B30", color="white",
                              width=float('inf'))
        ]),
        bgcolor="#FFF0F0", padding=20, border_radius=16,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black5")
    )

    main_content = ft.Container(
        content=ft.Column([
            ft.Text("Cài Đặt", size=26, weight="bold"),
            ft.Container(height=10),
            dev_card,
            ft.Container(height=20),
            danger_zone
        ], expand=True, scroll="auto"),
        padding=20, expand=True, bgcolor="#F8F8F8"
    )

    return ft.Stack([main_content, confirm_overlay, success_overlay], expand=True)