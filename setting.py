from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal

import requests
from bs4 import BeautifulSoup
from firebase_config import auth


class ChangePasswordCodePTITThread(QThread):
    update_status = pyqtSignal(str)
    finished = pyqtSignal(bool, str)  # (success, message)

    def __init__(self, username, old_password, new_password):
        super().__init__()
        self.username = username
        self.old_password = old_password
        self.new_password = new_password

    def run(self):
        session = requests.Session()
        login_url = "https://code.ptit.edu.vn/login"
        change_pw_url = "https://code.ptit.edu.vn/password/change"

        try:
            # Đăng nhập ngầm để xác thực mật khẩu cũ và lấy session
            get_login = session.get(login_url, timeout=10)
            soup_login = BeautifulSoup(get_login.text, "html.parser")
            token_login = soup_login.find("input", {"name": "_token"})
            csrf_token_login = token_login.get("value") if token_login else ""

            login_payload = {
                "username": self.username,
                "password": self.old_password,
                "_token": csrf_token_login,
            }

            post_login = session.post(login_url, data=login_payload, timeout=10)

            if post_login.url == login_url and "Đăng xuất" not in post_login.text:
                self.finished.emit(False, "❌ Mật khẩu cũ không đúng. Vui lòng kiểm tra lại!")
                return

            # Truy cập trang đổi mật khẩu để lấy token + tên input động
            get_pw = session.get(change_pw_url, timeout=10)
            soup_pw = BeautifulSoup(get_pw.text, "html.parser")

            token_pw = soup_pw.find("input", {"name": "_token"})
            csrf_token_pw = token_pw.get("value") if token_pw else ""

            pw_inputs = soup_pw.find_all("input", type="password")
            if len(pw_inputs) >= 3:
                name_old = pw_inputs[0].get("name")
                name_new = pw_inputs[1].get("name")
                name_confirm = pw_inputs[2].get("name")
            else:
                name_old = "old_password"
                name_new = "password"
                name_confirm = "password_confirmation"

            pw_payload = {
                "_token": csrf_token_pw,
                name_old: self.old_password,
                name_new: self.new_password,
                name_confirm: self.new_password,
            }

            post_pw = session.post(change_pw_url, data=pw_payload, timeout=10)
            soup_result = BeautifulSoup(post_pw.text, "html.parser")

            error_elem = soup_result.find("span", class_="invalid-feedback")
            if not error_elem:
                error_elem = soup_result.find("div", class_="alert-danger")

            actual_error = error_elem.text.strip() if error_elem else "Mật khẩu không hợp lệ"

            if post_pw.status_code == 200 and (
                "thành công" in post_pw.text.lower() or post_pw.url != change_pw_url
            ):
                self.finished.emit(True, "✅ Đổi mật khẩu thành công trên hệ thống CodePTIT!")
            else:
                self.finished.emit(False, actual_error)

        except requests.exceptions.RequestException:
            self.finished.emit(False, "Lỗi kết nối mạng!")
        except Exception as e:
            self.finished.emit(False, f"Lỗi: {e}")


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
            QPushButton {
                background: transparent;
                border: none;
                font-size: 16px;
                color: #6B7280;
            }
            QPushButton:hover {
                color: #C81E1E;
            }
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

    def text(self):
        return self.input.text().strip()

    def clear(self):
        self.input.clear()


class SettingsWidget(QtWidgets.QWidget):
    def __init__(
        self,
        auth_provider=None,
        email="",
        username="",
        full_name="",
        student_id="",
        phone=""
    ):
        super().__init__()

        self.auth_provider = auth_provider
        self.email = email
        self.username = username
        self.full_name = full_name
        self.student_id = student_id
        self.phone = phone

        self.change_pass_thread = None

        self.setObjectName("SettingsScreen")
        self.setStyleSheet("""
            QWidget#SettingsScreen {
                background-color: #F8F9FA;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                background: transparent;
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
            QLabel#providerLabel {
                font-size: 13px;
                font-weight: bold;
                color: #C81E1E;
                background-color: #FEF2F2;
                border: 1px solid #FECACA;
                border-radius: 6px;
                padding: 8px 12px;
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
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton.primaryBtn:hover {
                background-color: #A41616;
            }
            QPushButton.primaryBtn:disabled {
                background-color: #D1D5DB;
                color: #6B7280;
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

        self.provider_label = QtWidgets.QLabel(self.get_provider_text())
        self.provider_label.setObjectName("providerLabel")
        layout.addWidget(self.provider_label)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(20)

        grid.addWidget(self.create_label("Họ và tên"), 0, 0)
        self.inp_hoten = QtWidgets.QLineEdit(self.full_name or "Nguyen Dinh Nghia")
        grid.addWidget(self.inp_hoten, 1, 0)

        grid.addWidget(self.create_label("Mã sinh viên"), 0, 1)
        self.inp_masv = QtWidgets.QLineEdit(self.student_id or "B24DCVN012")
        self.inp_masv.setReadOnly(True)
        grid.addWidget(self.inp_masv, 1, 1)

        grid.addWidget(self.create_label("Email / Username"), 2, 0)
        display_account = self.email if self.email else self.username
        self.inp_email = QtWidgets.QLineEdit(display_account)
        self.inp_email.setReadOnly(True)
        grid.addWidget(self.inp_email, 3, 0)

        grid.addWidget(self.create_label("Số điện thoại"), 2, 1)
        self.inp_sdt = QtWidgets.QLineEdit(self.phone or "")
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

        self.security_provider_label = QtWidgets.QLabel(self.get_provider_text())
        self.security_provider_label.setObjectName("providerLabel")
        layout.addWidget(self.security_provider_label)

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

    def get_provider_text(self):
        if self.auth_provider == "firebase":
            return "Đăng nhập bằng: Firebase"
        if self.auth_provider == "ptit":
            return "Đăng nhập bằng: Code PTIT"
        return "Đăng nhập bằng: Chưa xác định"

    def switch_tab(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def handle_save(self):
        self.btn_luu.setText("✔ Đã lưu thành công!")
        self.btn_luu.setStyleSheet("background-color: #16A34A; color: white;")
        QtCore.QTimer.singleShot(2000, self.reset_save_btn)

    def reset_save_btn(self):
        self.btn_luu.setText("💾 Lưu thay đổi")
        self.btn_luu.setStyleSheet("")

    def validate_password_inputs(self):
        old_password = self.inp_pass_old.text()
        new_password = self.inp_pass_new.text()
        confirm_password = self.inp_pass_confirm.text()

        if not old_password or not new_password or not confirm_password:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ 3 ô mật khẩu.")
            return None

        if new_password != confirm_password:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp.")
            return None

        if len(new_password) < 6:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Mật khẩu mới phải có ít nhất 6 ký tự.")
            return None

        if old_password == new_password:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Mật khẩu mới không được trùng mật khẩu cũ.")
            return None

        return old_password, new_password, confirm_password

    def handle_change_pass(self):
        validated = self.validate_password_inputs()
        if not validated:
            return

        old_password, new_password, _ = validated

        if self.auth_provider == "firebase":
            self.change_password_firebase(old_password, new_password)
        elif self.auth_provider == "ptit":
            self.change_password_ptit(old_password, new_password)
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Lỗi",
                "Không xác định được loại tài khoản để đổi mật khẩu."
            )

    def set_change_pass_loading(self, is_loading, text=None):
        self.btn_doimk.setDisabled(is_loading)
        if text:
            self.btn_doimk.setText(text)
        else:
            self.btn_doimk.setText("🔑 Đổi mật khẩu" if not is_loading else "Đang xử lý...")

    def show_change_pass_success(self, message):
        self.btn_doimk.setText("✔ Đổi mật khẩu thành công!")
        self.btn_doimk.setStyleSheet("background-color: #16A34A; color: white;")
        QtWidgets.QMessageBox.information(self, "Thành công", message)
        self.clear_password_inputs()
        QtCore.QTimer.singleShot(2000, self.reset_change_pass_btn)

    def show_change_pass_error(self, message):
        QtWidgets.QMessageBox.warning(self, "Lỗi", message)
        self.reset_change_pass_btn()

    def reset_change_pass_btn(self):
        self.btn_doimk.setDisabled(False)
        self.btn_doimk.setText("🔑 Đổi mật khẩu")
        self.btn_doimk.setStyleSheet("")

    def clear_password_inputs(self):
        self.inp_pass_old.clear()
        self.inp_pass_new.clear()
        self.inp_pass_confirm.clear()

    def change_password_firebase(self, old_password, new_password):
        if not self.email:
            self.show_change_pass_error("Không tìm thấy email tài khoản Firebase.")
            return

        self.set_change_pass_loading(True, "Đang đổi mật khẩu Firebase...")

        try:
            user = auth.sign_in_with_email_and_password(self.email, old_password)
            id_token = user["idToken"]
            import requests
            from firebase_config import firebaseConfig

            url = (
                "https://identitytoolkit.googleapis.com/v1/accounts:update"
                f"?key={firebaseConfig['apiKey']}"
            )

            payload = {
                "idToken": id_token,
                "password": new_password,
                "returnSecureToken": True
            }

            response = requests.post(url, json=payload, timeout=15)
            data = response.json()

            if response.status_code == 200 and "idToken" in data:
                self.show_change_pass_success("Đổi mật khẩu Firebase thành công!")
            else:
                error_message = data.get("error", {}).get("message", "Không thể đổi mật khẩu Firebase.")
                self.show_change_pass_error(f"Lỗi Firebase: {error_message}")

        except Exception as e:
            self.show_change_pass_error(f"Không thể đổi mật khẩu Firebase: {e}")

    def change_password_ptit(self, old_password, new_password):
        if not self.username:
            self.show_change_pass_error("Không tìm thấy username Code PTIT.")
            return

        self.set_change_pass_loading(True, "Đang đổi mật khẩu Code PTIT...")

        self.change_pass_thread = ChangePasswordCodePTITThread(
            username=self.username,
            old_password=old_password,
            new_password=new_password
        )
        self.change_pass_thread.finished.connect(self.on_ptit_change_pass_finished)
        self.change_pass_thread.start()

    def on_ptit_change_pass_finished(self, success, message):
        if success:
            self.show_change_pass_success(message)
        else:
            self.show_change_pass_error(message)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = SettingsWidget(
        auth_provider="ptit",
        username="B24DCVN012",
        full_name="Nguyen Dinh Nghia",
        student_id="B24DCVN012",
        phone="0375853601"
    )
    window.resize(1000, 700)
    window.show()
    sys.exit(app.exec_())