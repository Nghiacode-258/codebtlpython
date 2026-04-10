from PyQt5 import QtCore, QtGui, QtWidgets 
import sqlite3
import hashlib 

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(480, 700)
        MainWindow.setStyleSheet("QMainWindow {background-color: #FAEAEC;}")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.centralwidget.setStyleSheet("""
            QWidget#centralwidget {
                background-color: #FAEAEC;
            }
            QLineEdit {
                border: 1px solid #D0D0D0;
                border-radius: 10px;
                padding: 10px 15px;
                background-color: white;
                color: #333333;
                font-size: 14px;
                min-height: 35px;
            }
            QLineEdit:focus{
                border: 2px solid #D32F2F; 
            }
            QPushButton {
                background-color: #D32F2F;
                color: white;
                border-radius: 25px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #B71C1C;
            }
            """)

        self.main_h_layout = QtWidgets.QHBoxLayout(self.centralwidget)

        self.signup_container = QtWidgets.QWidget()
        self.signup_container.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.signup_container.setMaximumWidth(600)

        self.form_layout = QtWidgets.QVBoxLayout(self.signup_container)
        self.form_layout.setSpacing(15)

        self.form_layout.addStretch(1)

        self.label = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setFamily("Segoe UI") 
        font.setPointSize(32)
        font.setBold(True)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("<html><head/><body><p><span style=\"color:#D32F2F;\">Sign</span><span style=\"color:#2D3748;\"> Up</span></p></body></html>")
        self.label.setContentsMargins(0, 0, 0, 30)

        self.email_input = QtWidgets.QLineEdit()
        self.email_input.setPlaceholderText("@gmail.com")
        self.email_input.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.pass_input = QtWidgets.QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_input.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.confirm_input = QtWidgets.QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm Password")
        self.confirm_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_input.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.signup_button = QtWidgets.QPushButton("Create Account")
        self.signup_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.signup_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.form_layout.addWidget(self.label)
        self.form_layout.addWidget(self.email_input)
        self.form_layout.addWidget(self.pass_input)
        self.form_layout.addWidget(self.confirm_input)
        self.form_layout.addWidget(self.signup_button)

        self.form_layout.addStretch(1)

        self.main_h_layout.addStretch(1)
        self.main_h_layout.addWidget(self.signup_container,4) 
        self.main_h_layout.addStretch(1)
        MainWindow.setCentralWidget(self.centralwidget)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())