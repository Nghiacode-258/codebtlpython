from PyQt5 import QtCore, QtGui, QtWidgets

class PasswordField(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.input = QtWidgets.QLineEdit()
        self.input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.input)

        self.eye_btn = QtWidgets.QPushButton("👁")
        self.eye_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.eye_btn.setFixedWidth(30)
        self.eye_btn.setStyleSheet("""
            QPushButton { background: transparent; border: none; font-size: 16px; color: #6B7280; }
            QPushButton:hover { color: #C81E1E; }
        """)
        self.eye_btn.clicked.connect(self.toggle_echo)
        layout.addWidget(self.eye_btn)

        self.is_visible = False

    def toggle_echo(self):
        self.is_visible = not self.is_visible
        if self.is_visible:
            self.input.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.eye_btn.setText("🙈")
        else:
            self.input.setEchoMode(QtWidgets.QLineEdit.Password)
            self.eye_btn.setText("👁")

    # Hàm hỗ trợ lấy text từ bên ngoài
    def text(self):
        return self.input.text()

# --- GIAO DIỆN CHÍNH ---
class SettingsWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel#pageTitle {
                font-size: 24px;
                font-weight: bold;
                color: #111827;
            }
            QLabel#pageSubtitle {
                font-size: 14px;
                color: #6B7280;
            }
            QWidget#tabContainer {
                background-color: #F3F4F6;
                border-radius: 10px;
            }
            QPushButton.tabButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                color: #4B5563;
                font-weight: bold;
            }
            QPushButton.tabButton:hover {
                background-color: #E5E7EB;
            }
            QPushButton.tabButton:checked {
                background-color: white;
                color: #C81E1E; 
                border: 1px solid #E5E7EB;
            }
            QFrame.cardFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }
            QLabel.cardTitle {
                font-size: 16px;
                font-weight: bold;
                color: #111827;
            }
            QLabel.cardSubtitle {
                font-size: 13px;
                color: #6B7280;
            }
            QLabel.inputLabel {
                font-size: 13px;
                font-weight: bold;
                color: #374151;
            }
            QLineEdit {
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 10px;
                background-color: white;
                font-size: 14px;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #C81E1E; 
            }
            QLineEdit:read-only {
                background-color: #F3F4F6; 
                color: #6B7280;
            }
            QPushButton.primaryBtn {
                background-color: #C81E1E;
                color: white;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton.primaryBtn:hover {
                background-color: #A41616;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(20)

        self.title_label = QtWidgets.QLabel("Cài đặt")
        self.title_label.setObjectName("pageTitle")
        self.subtitle_label = QtWidgets.QLabel("Quản lý tài khoản và tùy chọn của bạn")
        self.subtitle_label.setObjectName("pageSubtitle")
        
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.subtitle_label)

        self.tab_container = QtWidgets.QWidget()
        self.tab_container.setObjectName("tabContainer")
        self.tab_layout = QtWidgets.QHBoxLayout(self.tab_container)
        self.tab_layout.setContentsMargins(5, 5, 5, 5)

        self.btn_taikhoan = QtWidgets.QPushButton("👤 Tài khoản")
        self.btn_taikhoan.setProperty("class", "tabButton")
        self.btn_taikhoan.setCheckable(True)
        self.btn_taikhoan.setChecked(True)
        self.btn_taikhoan.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.btn_baomat = QtWidgets.QPushButton("🛡️ Bảo mật")
        self.btn_baomat.setProperty("class", "tabButton")
        self.btn_baomat.setCheckable(True)
        self.btn_baomat.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.tab_btn_group = QtWidgets.QButtonGroup(self)
        self.tab_btn_group.addButton(self.btn_taikhoan, 0) 
        self.tab_btn_group.addButton(self.btn_baomat, 1)   
        self.tab_btn_group.buttonClicked[int].connect(self.switch_tab)

        self.tab_layout.addWidget(self.btn_taikhoan)
        self.tab_layout.addWidget(self.btn_baomat)
        self.tab_layout.addStretch()

        self.main_layout.addWidget(self.tab_container)

        self.stacked_widget = QtWidgets.QStackedWidget()
        
        self.page_taikhoan = self.create_taikhoan_page()
        self.page_baomat = self.create_baomat_page()
        
        self.stacked_widget.addWidget(self.page_taikhoan)
        self.stacked_widget.addWidget(self.page_baomat)   

        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.addStretch()

    def create_taikhoan_page(self):
        frame = QtWidgets.QFrame()
        frame.setProperty("class", "cardFrame")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QtWidgets.QLabel("Thông tin cá nhân")
        title.setProperty("class", "cardTitle")
        subtitle = QtWidgets.QLabel("Cập nhật thông tin cá nhân của bạn")
        subtitle.setProperty("class", "cardSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(20)

        grid.addWidget(self.create_label("Họ và tên"), 0, 0)
        self.inp_hoten = QtWidgets.QLineEdit("Nguyen Dinh Nghia")
        grid.addWidget(self.inp_hoten, 1, 0)

        grid.addWidget(self.create_label("Mã sinh viên"), 0, 1)
        self.inp_masv = QtWidgets.QLineEdit("B24DCVN012")
        self.inp_masv.setReadOnly(True)
        grid.addWidget(self.inp_masv, 1, 1)

        grid.addWidget(self.create_label("Email"), 2, 0)
        self.inp_email = QtWidgets.QLineEdit("nghia@ptit.edu.vn")
        grid.addWidget(self.inp_email, 3, 0)

        grid.addWidget(self.create_label("Số điện thoại"), 2, 1)
        self.inp_sdt = QtWidgets.QLineEdit("0375 853 601")
        grid.addWidget(self.inp_sdt, 3, 1)

        layout.addLayout(grid)
        layout.addSpacing(15)

        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_luu = QtWidgets.QPushButton("💾 Lưu thay đổi")
        self.btn_luu.setProperty("class", "primaryBtn")
        self.btn_luu.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        self.btn_luu.clicked.connect(self.handle_save)
        
        btn_layout.addWidget(self.btn_luu)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        return frame

    def create_baomat_page(self):
        frame = QtWidgets.QFrame()
        frame.setProperty("class", "cardFrame")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QtWidgets.QLabel("Đổi mật khẩu")
        title.setProperty("class", "cardTitle")
        subtitle = QtWidgets.QLabel("Cập nhật mật khẩu để bảo vệ tài khoản")
        subtitle.setProperty("class", "cardSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)

        # --- SỬ DỤNG COMPONENT PasswordField MỚI TẠO ---
        layout.addWidget(self.create_label("Mật khẩu hiện tại"))
        self.inp_pass_old = PasswordField()
        layout.addWidget(self.inp_pass_old)

        layout.addWidget(self.create_label("Mật khẩu mới"))
        self.inp_pass_new = PasswordField()
        layout.addWidget(self.inp_pass_new)

        layout.addWidget(self.create_label("Xác nhận mật khẩu"))
        self.inp_pass_confirm = PasswordField()
        layout.addWidget(self.inp_pass_confirm)

        layout.addSpacing(15)

        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_doimk = QtWidgets.QPushButton("🔑 Đổi mật khẩu")
        self.btn_doimk.setProperty("class", "primaryBtn")
        self.btn_doimk.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        self.btn_doimk.clicked.connect(self.handle_change_pass)
        
        btn_layout.addWidget(self.btn_doimk)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        return frame

    def create_label(self, text):
        lbl = QtWidgets.QLabel(text)
        lbl.setProperty("class", "inputLabel")
        return lbl

    def switch_tab(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def handle_save(self):
        self.btn_luu.setText("✔ Đã lưu thành công!")
        self.btn_luu.setStyleSheet("background-color: #16A34A; color: white;") 
        QtCore.QTimer.singleShot(2000, self.reset_save_btn)

    def reset_save_btn(self):
        self.btn_luu.setText("💾 Lưu thay đổi")
        self.btn_luu.setStyleSheet("")

    def handle_change_pass(self):
        self.btn_doimk.setText("✔ Đã cập nhật mật khẩu!")
        self.btn_doimk.setStyleSheet("background-color: #16A34A; color: white;")
        QtCore.QTimer.singleShot(2000, self.reset_change_pass_btn)

    def reset_change_pass_btn(self):
        self.btn_doimk.setText("🔑 Đổi mật khẩu")
        self.btn_doimk.setStyleSheet("")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = SettingsWidget()
    window.resize(1000, 700)
    window.show()
    sys.exit(app.exec_())