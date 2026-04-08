from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(480, 700)
        MainWindow.setStyleSheet("""QMainWindow {background-color: #121212;}""")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("""
        QWidget#centralwidget {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 25px;
        }

        QLabel {
            color: white;
            font-weight: bold;
        }

        QLineEdit {
            border: none;
            border-radius: 20px;
            padding: 12px;
            background-color: #2a2a2a;
            color: white;
            font-size: 14px;
        }

        QLineEdit:focus {
            border: 2px solid #00ffff;
        }

        QPushButton {
            background-color: #00c8ff;
            color: black;
            border-radius: 25px;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #00a6d6;
        }

        QCheckBox {
            color: white;
            font-size: 10pt;
        }
        """)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 100, 300, 80)) 
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        font = QtGui.QFont()
        font.setFamily("Segoe UI") 
        font.setPointSize(28)
        font.setBold(True)

        self.label.setFont(font)
        self.label.setStyleSheet("color: white;")
        self.label.setText("Login")
        self.label.setStyleSheet("""
        color: white;
        letter-spacing: 2px;
        """)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 250, 340, 45))
        self.lineEdit_2.setPlaceholderText("@gmail.com")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(70, 320, 340, 45))
        self.lineEdit.setPlaceholderText("Password")
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(70, 390, 150, 30))
        self.checkBox.setText("Remember me")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(280, 390, 170, 30))
        self.label_3.setText("Forgot password?")
        self.label_3.setStyleSheet("color: #00c8ff;") 

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(70, 460, 340, 50))
        self.pushButton.setText("Login")

        self.ptit_btn = QtWidgets.QPushButton("Login with Code PTIT")
        self.ptit_btn.setGeometry(110, 500, 250, 40)
        self.ptit_btn.setStyleSheet("""
        QPushButton {
            background-color: #FF9800;
            color: white;
            border-radius: 6px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #FB8C00;
        }
        """)

        MainWindow.setCentralWidget(self.centralwidget)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())