import sys
from PyQt5 import QtWidgets, QtCore, QtGui

from login import Ui_MainWindow as LoginUI
from signup import Ui_MainWindow as SignUpUI
from student import StudentWindow
import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyCxms2ug17qh4GwP5qq0fgBTBfhvLOWLQ8",
  'authDomain': "kawaii-f2f0c.firebaseapp.com",
  'databaseURL': "https://kawaii-f2f0c-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "kawaii-f2f0c",
  'storageBucket': "kawaii-f2f0c.firebasestorage.app",
  'messagingSenderId': "1014671314187",
  'appId': "1:1014671314187:web:2c62b562d17f68b5ed660e",
  'measurementId': "G-7Z43834BQR"
};

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = LoginUI()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.handle_login)
        self.to_signup = QtWidgets.QPushButton(self.ui.centralwidget)
        self.to_signup.setText("Don't have an account? Sign up")
        self.to_signup.setGeometry(110, 550, 250, 60)
        self.to_signup.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: #4FC3F7;
            border: none;
            font-size: 14px;
        }
        QPushButton:hover {
            color: #81D4FA;
            text-decoration: underline;
        }
        """)
        self.to_signup.clicked.connect(self.go_signup)
        self.ui.label_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ui.label_3.mousePressEvent = self.handle_forgot_password

    def go_signup(self):
        self.signup = SignUpWindow()
        self.signup.show()
        self.close()

    def handle_login(self):
        username = self.ui.lineEdit_2.text().strip()
        password = self.ui.lineEdit.text().strip()

        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Nhập đầy đủ thông tin")
            return

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        try:
            auth.sign_in_with_email_and_password(username, password)
            QtWidgets.QApplication.restoreOverrideCursor()

            QtWidgets.QMessageBox.information(self, "Success", "Đăng nhập thành công!")
            self.student = StudentWindow()
            self.student.show()
            self.close()
            return
        except:
            print("Firebase fail → thử PTIT")
        from login_ptit import LoginRequest
        info = LoginRequest(username, password).attempt()
        QtWidgets.QApplication.restoreOverrideCursor()
        if info:
            QtWidgets.QMessageBox.information(self, "Thành công", f"Xin chào {info.name}")
            self.student = StudentWindow()
            self.student.setWindowTitle(f"{info.name} - {info.student_id}")
            self.student.show()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Sai tài khoản Firebase hoặc Code PTIT!")
            
    def handle_forgot_password(self, event):
        email, ok = QtWidgets.QInputDialog.getText(self, "Quên mật khẩu", "Nhập email:")
        if not ok or not email:
            return
        try:
            auth.send_password_reset_email(email)
            QtWidgets.QMessageBox.information(
                self,
                "Thành công",
                "Đã gửi email reset mật khẩu!\nVui lòng kiểm tra Gmail."
            )
        except:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Email không tồn tại!")


class SignUpWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = SignUpUI()
        self.ui.setupUi(self)
        self.ui.signup_button.clicked.connect(self.handle_signup)
        self.to_login = QtWidgets.QPushButton(self.ui.centralwidget)
        self.to_login.setText("Already have an account? Login")
        self.to_login.setGeometry(110, 550, 250, 60)
        self.to_login.setStyleSheet("""
            QPushButton{
                background-color: transparent;
                color: #4FC3F7;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover{
                color: #81D4FA;
                text-decoration: underline;
            }
        """)
        self.to_login.clicked.connect(self.go_login)

    def go_login(self):
        self.login = LoginWindow()
        self.login.show()
        self.close()

    def handle_signup(self):
        email = self.ui.email_input.text().strip()
        password = self.ui.pass_input.text().strip()
        confirm = self.ui.confirm_input.text().strip()
        if not email or not password or not confirm:
            QtWidgets.QMessageBox.warning(self, "Error", "Nhập đầy đủ thông tin")
            return
        if password != confirm:
            QtWidgets.QMessageBox.warning(self, "Error", "Mật khẩu không khớp")
            return
        if len(password) < 6:
            QtWidgets.QMessageBox.warning(self, "Error", "Mật khẩu phải ≥ 6 ký tự")
            return
        try:
            auth.create_user_with_email_and_password(email, password)
            QtWidgets.QMessageBox.information(self, "Success", "Đăng ký thành công!")
            self.go_login()
        except:
            QtWidgets.QMessageBox.warning(self, "Error", "Email đã tồn tại hoặc không hợp lệ")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
