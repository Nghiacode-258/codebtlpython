import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from personal_info_service import get_or_create_personal_info, update_personal_info

STYLE_SHEET = """
    QWidget {
        background-color: white;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    QLabel#pageTitle {
        font-size: 16px;
        font-weight: bold;
        color: #111827;
        padding: 16px 24px 16px 24px;
        background-color: white;
    }
    QFrame#alertBanner {
        background-color: #EBF5FF;
        border: 1px solid #93C5FD;
        border-radius: 4px;
    }
    QLabel#alertText {
        color: #1E3A8A;
        font-size: 13px;
    }
    QLabel#cardMainTitle {
        font-size: 20px;
        color: #374151;
        margin-bottom: 24px;
    }
    QLabel.infoLabel {
        font-size: 13px;
        color: #111827;
    }
    QLabel.badgeBlue {
        background-color: #EBF5FF;
        color: #2563EB;
        border: 1px solid #93C5FD;
        border-radius: 4px;
        font-size: 11px;
        padding: 2px 6px;
        font-weight: 500;
    }
"""

OUTLINE_BTN_STYLE = """
    QPushButton {
        background-color: white;
        color: #374151;
        border: 1px solid #D1D5DB;
        border-radius: 4px;
        padding: 8px 16px;
        font-size: 13px;
    }
    QPushButton:hover {
        background-color: #F3F4F6;
    }
"""

PRIMARY_BTN_STYLE = """
    QPushButton {
        background-color: #DC2626;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: 500;
    }
    QPushButton:hover {
        background-color: #B91C1C;
    }
"""


class PersonalInfoWidget(QtWidgets.QWidget):
    def __init__(self, firebase_uid="", email="", full_name="", student_id="", phone=""):
        super().__init__()

        self.firebase_uid = firebase_uid
        self.email = email
        self.full_name = full_name
        self.student_id = student_id
        self.phone = phone

        if self.firebase_uid:
            self.profile = get_or_create_personal_info(
                firebase_uid=self.firebase_uid,
                email=self.email,
                full_name=self.full_name,
                student_id=self.student_id,
                phone=self.phone
            )
        else:
            self.profile = {}

        self.setStyleSheet(STYLE_SHEET)
        self.setup_ui()

    def value(self, key, default="Chưa cập nhật"):
        value = self.profile.get(key, "")
        return value if value not in (None, "") else default

    def setup_ui(self):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QtWidgets.QLabel("Thông tin cá nhân")
        header.setObjectName("pageTitle")
        root.addWidget(header)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setStyleSheet("background-color: #E5E7EB; max-height: 1px; border: none;")
        root.addWidget(line)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setStyleSheet("background: white;")

        content = QtWidgets.QWidget()
        content.setStyleSheet("background: white;")

        cl = QtWidgets.QVBoxLayout(content)
        cl.setContentsMargins(32, 24, 32, 32)
        cl.setSpacing(16)

        banner = QtWidgets.QFrame()
        banner.setObjectName("alertBanner")
        banner_layout = QtWidgets.QHBoxLayout(banner)
        banner_layout.setContentsMargins(20, 14, 20, 14)

        alert_text = QtWidgets.QLabel(
            'Đợt cập nhật hồ sơ <b>"Đợt cập nhật hồ sơ"</b> từ ngày <b>01/11/2024</b> đến ngày <b>31/03/2028</b>'
        )
        alert_text.setObjectName("alertText")
        banner_layout.addWidget(alert_text)
        cl.addWidget(banner)

        action_bar = QtWidgets.QHBoxLayout()
        action_bar.setSpacing(12)

        self.btn_hoc_ba = QtWidgets.QPushButton("☰ Học bạ số")
        self.btn_hoc_ba.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_hoc_ba.setStyleSheet(OUTLINE_BTN_STYLE)
        action_bar.addWidget(self.btn_hoc_ba)

        self.btn_cap_nhat_anh = QtWidgets.QPushButton("⟲ Cập nhật ảnh nhận diện")
        self.btn_cap_nhat_anh.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cap_nhat_anh.setStyleSheet(OUTLINE_BTN_STYLE)
        action_bar.addWidget(self.btn_cap_nhat_anh)

        self.btn_cap_nhat_ho_so = QtWidgets.QPushButton("✎ Cập nhật hồ sơ")
        self.btn_cap_nhat_ho_so.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cap_nhat_ho_so.setStyleSheet(PRIMARY_BTN_STYLE)
        self.btn_cap_nhat_ho_so.clicked.connect(self.open_update_dialog)
        action_bar.addWidget(self.btn_cap_nhat_ho_so)

        action_bar.addStretch()
        cl.addLayout(action_bar)

        cl.addSpacing(32)

        title = QtWidgets.QLabel("SƠ YẾU LÝ LỊCH")
        title.setObjectName("cardMainTitle")
        title.setAlignment(QtCore.Qt.AlignCenter)
        cl.addWidget(title)

        body = QtWidgets.QHBoxLayout()
        body.setSpacing(48)
        body.setAlignment(QtCore.Qt.AlignTop)

        avatar_lbl = QtWidgets.QLabel()
        avatar_lbl.setFixedSize(150, 190)
        avatar_lbl.setStyleSheet(
            "background-color: #2D3748; border: 1px solid #E5E7EB; border-radius: 4px;"
        )

        avatar_wrapper = QtWidgets.QVBoxLayout()
        avatar_wrapper.addWidget(avatar_lbl)
        avatar_wrapper.addStretch()
        body.addLayout(avatar_wrapper)

        self.info_container = QtWidgets.QWidget()
        self.info_container_layout = QtWidgets.QVBoxLayout(self.info_container)
        self.info_container_layout.setContentsMargins(0, 0, 0, 0)
        self.info_container_layout.setSpacing(0)

        self.render_info_grid()
        body.addWidget(self.info_container, 1)

        cl.addLayout(body)
        cl.addStretch()

        scroll.setWidget(content)
        root.addWidget(scroll, 1)

    def render_info_grid(self):
        while self.info_container_layout.count():
            item = self.info_container_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        grid_widget = QtWidgets.QWidget()
        grid_widget.setLayout(self._build_info_grid())
        self.info_container_layout.addWidget(grid_widget)

    def _lbl(self, html):
        lbl = QtWidgets.QLabel(html)
        lbl.setProperty("class", "infoLabel")
        lbl.setWordWrap(True)
        lbl.setTextFormat(QtCore.Qt.RichText)
        return lbl

    def _badge(self, text):
        lbl = QtWidgets.QLabel(text)
        lbl.setProperty("class", "badgeBlue")
        return lbl

    def _build_info_grid(self):
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(18)
        grid.setVerticalSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(2, 2)

        ma_sinh_vien = self.value("ma_sinh_vien")
        ho_ten = self.value("ho_ten")
        gioi_tinh = self.value("gioi_tinh")
        ngay_sinh = self.value("ngay_sinh")
        trang_thai_hoc = self.value("trang_thai_hoc", "Đang học")
        cccd = self.value("cccd")
        ngay_cap_cccd = self.value("ngay_cap_cccd")
        noi_cap_cccd = self.value("noi_cap_cccd")
        so_dien_thoai = self.value("so_dien_thoai")
        email_hoc_tap = self.value("email_hoc_tap")
        khoa_nganh = self.value("khoa_nganh")
        chuyen_nganh = self.value("chuyen_nganh")
        quoc_tich = self.value("quoc_tich", "Việt Nam")
        dan_toc = self.value("dan_toc")
        ton_giao = self.value("ton_giao")
        tinh_thanh = self.value("tinh_thanh")
        xa_phuong = self.value("xa_phuong")
        dia_chi_chi_tiet = self.value("dia_chi_chi_tiet")
        ngay_vao_dang_du_bi = self.value("ngay_vao_dang_du_bi")
        ngay_vao_dang_chinh_thuc = self.value("ngay_vao_dang_chinh_thuc")
        so_bao_hiem = self.value("so_bao_hiem")
        ma_benh_vien = self.value("ma_benh_vien")
        ten_ngan_hang = self.value("ten_ngan_hang")
        so_tai_khoan = self.value("so_tai_khoan")

        grid.addWidget(self._lbl(f"<b>1. Mã sinh viên:</b> {ma_sinh_vien}"), 0, 0)
        grid.addWidget(self._lbl(f"<b>2. Họ và tên:</b> {ho_ten}"), 0, 1, 1, 2)

        grid.addWidget(self._lbl(f"<b>3. Giới tính:</b> {gioi_tinh}"), 1, 0)
        grid.addWidget(self._lbl(f"<b>4. Ngày sinh:</b> {ngay_sinh}"), 1, 1)

        trang_thai_layout = QtWidgets.QHBoxLayout()
        trang_thai_layout.addWidget(self._lbl("<b>5. Trạng thái học:</b>"))
        trang_thai_layout.addWidget(self._badge(trang_thai_hoc))
        trang_thai_layout.addStretch()

        w = QtWidgets.QWidget()
        w.setLayout(trang_thai_layout)
        trang_thai_layout.setContentsMargins(0, 0, 0, 0)
        grid.addWidget(w, 1, 2)

        grid.addWidget(
            self._lbl(
                f"<b>6. CCCD/CMND:</b> {cccd}, Ngày cấp: {ngay_cap_cccd}, Nơi cấp: {noi_cap_cccd}"
            ),
            2, 0, 1, 3
        )

        grid.addWidget(self._lbl(f"<b>7. Số điện thoại:</b> {so_dien_thoai}"), 3, 0)
        grid.addWidget(self._lbl(f"<b>8. Email:</b> {email_hoc_tap}"), 3, 1, 1, 2)

        khoa_layout = QtWidgets.QHBoxLayout()
        khoa_layout.addWidget(self._lbl(f"<b>9. Khóa ngành đào tạo:</b> {khoa_nganh}"))
        khoa_layout.addWidget(self._badge(trang_thai_hoc))
        khoa_layout.addWidget(self._lbl(f"(Chuyên ngành: <i>{chuyen_nganh}</i>)"))
        khoa_layout.addStretch()

        w_khoa = QtWidgets.QWidget()
        w_khoa.setLayout(khoa_layout)
        khoa_layout.setContentsMargins(0, 0, 0, 0)
        grid.addWidget(w_khoa, 4, 0, 1, 3)

        grid.addWidget(self._lbl(f"<b>10. Quốc tịch:</b> {quoc_tich}"), 5, 0)
        grid.addWidget(self._lbl(f"<b>11. Dân tộc:</b> {dan_toc}"), 5, 1)
        grid.addWidget(self._lbl(f"<b>12. Tôn giáo:</b> {ton_giao}"), 5, 2)

        grid.addWidget(self._lbl("<b>13. Địa chỉ thường trú:</b>"), 6, 0, 1, 3)
        grid.addWidget(self._lbl(f"Tỉnh/Thành phố: {tinh_thanh}"), 7, 0)
        grid.addWidget(self._lbl(f"Xã/Phường/Đặc khu: {xa_phuong}"), 7, 1)
        grid.addWidget(self._lbl(f"Địa chỉ: {dia_chi_chi_tiet}"), 7, 2)

        grid.addWidget(self._lbl("<b>14. Đảng:</b>"), 8, 0, 1, 3)
        grid.addWidget(self._lbl(f"Ngày vào Đảng dự bị: {ngay_vao_dang_du_bi}"), 9, 0)
        grid.addWidget(self._lbl(f"Ngày vào Đảng chính thức: {ngay_vao_dang_chinh_thuc}"), 9, 2)

        grid.addWidget(self._lbl(f"<b>15. Số bảo hiểm sinh viên:</b> {so_bao_hiem}"), 10, 0)
        grid.addWidget(self._lbl(f"<b>16. Mã bệnh viện khám chữa bệnh:</b> {ma_benh_vien}"), 10, 1, 1, 2)

        grid.addWidget(self._lbl("<b>17. Tài khoản ngân hàng:</b>"), 11, 0, 1, 3)
        grid.addWidget(self._lbl(f"Tên ngân hàng: {ten_ngan_hang}"), 12, 0)
        grid.addWidget(self._lbl(f"Số tài khoản: {so_tai_khoan}"), 12, 2)

        return grid

    def open_update_dialog(self):
        if not self.firebase_uid:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Không tìm thấy tài khoản đăng nhập.")
            return

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Cập nhật hồ sơ")
        dialog.resize(720, 680)
        dialog.setStyleSheet("""
            QDialog {
                background: white;
            }
            QLabel {
                font-size: 13px;
                color: #374151;
            }
            QLineEdit, QComboBox {
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 8px 10px;
                background: white;
                color: #111827;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #DC2626;
            }
        """)

        main_layout = QtWidgets.QVBoxLayout(dialog)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)

        form_widget = QtWidgets.QWidget()
        form_layout = QtWidgets.QFormLayout(form_widget)
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        form_layout.setFormAlignment(QtCore.Qt.AlignTop)
        form_layout.setSpacing(12)

        inputs = {}

        def add_line(label_text, key):
            line = QtWidgets.QLineEdit()
            line.setText(self.profile.get(key, ""))
            line.setMinimumHeight(36)
            inputs[key] = line
            form_layout.addRow(label_text, line)

        add_line("Mã sinh viên:", "ma_sinh_vien")
        add_line("Họ và tên:", "ho_ten")

        gender_box = QtWidgets.QComboBox()
        gender_box.addItems(["", "Nam", "Nữ", "Khác"])
        gender_box.setCurrentText(self.profile.get("gioi_tinh", ""))
        gender_box.setMinimumHeight(36)
        inputs["gioi_tinh"] = gender_box
        form_layout.addRow("Giới tính:", gender_box)

        add_line("Ngày sinh:", "ngay_sinh")

        status_box = QtWidgets.QComboBox()
        status_box.addItems(["Đang học", "Bảo lưu", "Thôi học", "Tốt nghiệp"])
        status_box.setCurrentText(self.profile.get("trang_thai_hoc", "Đang học"))
        status_box.setMinimumHeight(36)
        inputs["trang_thai_hoc"] = status_box
        form_layout.addRow("Trạng thái học:", status_box)

        add_line("CCCD/CMND:", "cccd")
        add_line("Ngày cấp CCCD:", "ngay_cap_cccd")
        add_line("Nơi cấp CCCD:", "noi_cap_cccd")
        add_line("Số điện thoại:", "so_dien_thoai")
        add_line("Email:", "email_hoc_tap")
        add_line("Khóa ngành đào tạo:", "khoa_nganh")
        add_line("Chuyên ngành:", "chuyen_nganh")
        add_line("Quốc tịch:", "quoc_tich")
        add_line("Dân tộc:", "dan_toc")
        add_line("Tôn giáo:", "ton_giao")
        add_line("Tỉnh/Thành phố:", "tinh_thanh")
        add_line("Xã/Phường:", "xa_phuong")
        add_line("Địa chỉ chi tiết:", "dia_chi_chi_tiet")
        add_line("Ngày vào Đảng dự bị:", "ngay_vao_dang_du_bi")
        add_line("Ngày vào Đảng chính thức:", "ngay_vao_dang_chinh_thuc")
        add_line("Số bảo hiểm:", "so_bao_hiem")
        add_line("Mã bệnh viện:", "ma_benh_vien")
        add_line("Tên ngân hàng:", "ten_ngan_hang")
        add_line("Số tài khoản:", "so_tai_khoan")

        scroll.setWidget(form_widget)
        main_layout.addWidget(scroll)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QtWidgets.QPushButton("Hủy")
        cancel_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        cancel_btn.setStyleSheet(OUTLINE_BTN_STYLE)
        cancel_btn.setMinimumHeight(36)

        save_btn = QtWidgets.QPushButton("Lưu")
        save_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        save_btn.setStyleSheet(PRIMARY_BTN_STYLE)
        save_btn.setMinimumHeight(36)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        main_layout.addLayout(btn_layout)

        cancel_btn.clicked.connect(dialog.reject)

        def save_data():
            data = {}
            for key, widget in inputs.items():
                if isinstance(widget, QtWidgets.QComboBox):
                    data[key] = widget.currentText().strip()
                else:
                    data[key] = widget.text().strip()

            update_personal_info(self.firebase_uid, data)
            self.profile.update(data)
            self.render_info_grid()

            QtWidgets.QMessageBox.information(self, "Thành công", "Đã cập nhật hồ sơ.")
            dialog.accept()

        save_btn.clicked.connect(save_data)
        dialog.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QtGui.QFont("Segoe UI", 10))

    window = PersonalInfoWidget()
    window.setWindowTitle("Thông tin cá nhân")
    window.resize(1200, 700)
    window.show()

    sys.exit(app.exec_())