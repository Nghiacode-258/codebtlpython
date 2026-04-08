from PyQt5 import QtCore, QtGui, QtWidgets 
import sqlite3
import hashlib 

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(480, 700)
        MainWindow.setStyleSheet("QMainWindow {background-color: #121212;}")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.centralwidget.setStyleSheet("""
            QWidget#centralwidget{
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 25px;
            }
            QLabel{
                color: white;
                font-weight: bold;
            }
            QLineEdit{
                border: none;
                border-radius: 20px;
                padding: 12px;
                background-color: #2a2a2a;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus{
                border: 2px solid #00ffff;
            }
            QPushButton{
                background-color: #00c8ff;
                color: black;
                border-radius: 25px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover{
                background-color: #00a6d6;
            }
        """)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 80, 300, 80))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont("Segoe UI", 28, QtGui.QFont.Bold)
        self.label.setFont(font)
        self.label.setText("Sign Up")
        self.label.setStyleSheet("color: white; letter-spacing: 2px;")

        self.email_input = QtWidgets.QLineEdit(self.centralwidget)
        self.email_input.setGeometry(QtCore.QRect(70, 220, 340, 45))
        self.email_input.setPlaceholderText("@gmail.com")

        self.pass_input = QtWidgets.QLineEdit(self.centralwidget)
        self.pass_input.setGeometry(QtCore.QRect(70, 290, 340, 45))
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.confirm_input = QtWidgets.QLineEdit(self.centralwidget)
        self.confirm_input.setGeometry(QtCore.QRect(70, 360, 340, 45))
        self.confirm_input.setPlaceholderText("Confirm Password")
        self.confirm_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.signup_button = QtWidgets.QPushButton(self.centralwidget)
        self.signup_button.setGeometry(QtCore.QRect(70, 450, 340, 50))
        self.signup_button.setText("Create Account")

        MainWindow.setCentralWidget(self.centralwidget)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())