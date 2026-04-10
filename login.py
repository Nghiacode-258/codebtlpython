from PyQt5 import QtCore, QtGui, QtWidgets

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

        QLineEdit:focus {
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

        QCheckBox {
            color: #4A5568;
            font-size: 11pt;
        }

        QCheckBox::indicator {
            width: 14px;
            height: 14px;
            border: 1px solid #B0B0B0;
            border-radius: 4px;
            background-color: white;
        }
        QCheckBox::indicator:checked {
            background-color: #D32F2F;
            border: 1px solid #D32F2F;
        }
        """)
        self.main_h_layout = QtWidgets.QHBoxLayout(self.centralwidget)

        self.login_container = QtWidgets.QWidget()
        self.login_container.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.login_container.setMaximumWidth(600)

        self.form_layout = QtWidgets.QVBoxLayout(self.login_container)
        self.form_layout.setSpacing(25)

        self.form_layout.addStretch(1)
        self.label = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setFamily("Segoe UI") 
        font.setPointSize(32)
        font.setBold(True)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("<html><head/><body><p><span style=\"color:#D32F2F;\">PTIT</span><span style=\"color:#2D3748;\"> Slink</span></p></body></html>")
        
        self.label.setContentsMargins(0, 0, 0, 30)

        self.lineEdit_2 = QtWidgets.QLineEdit()
        self.lineEdit_2.setPlaceholderText("@gmail.com")

        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setPlaceholderText("Password")
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.remember_forgot_layout = QtWidgets.QHBoxLayout()
        
        self.checkBox = QtWidgets.QCheckBox("Remember me")
        
        self.label_3 = QtWidgets.QLabel("Forgot password?")
        self.label_3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_3.setStyleSheet("color: #D32F2F; font-size: 11pt;") 
        self.label_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        self.remember_forgot_layout.addWidget(self.checkBox)
        self.remember_forgot_layout.addWidget(self.label_3)

        self.pushButton = QtWidgets.QPushButton("Login")
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.form_layout.addWidget(self.label)
        self.form_layout.addWidget(self.lineEdit_2)
        self.form_layout.addWidget(self.lineEdit)
        self.form_layout.addLayout(self.remember_forgot_layout)
        self.form_layout.addWidget(self.pushButton)

        self.form_layout.addStretch(1)

        self.main_h_layout.addStretch(1)
        self.main_h_layout.addWidget(self.login_container, 4) 
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