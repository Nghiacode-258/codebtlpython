import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from database import connect, init_db

class StudentWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        init_db()
        self.setWindowTitle("🎓 Student Management")
        self.resize(1200, 700)
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.setup_sidebar()
        self.setup_main()
        self.apply_stylesheet()
        self.load_data()

    def setup_sidebar(self):
        self.sidebar = QtWidgets.QFrame()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setObjectName("sidebar")

        layout = QtWidgets.QVBoxLayout(self.sidebar)
        layout.setContentsMargins(10, 40, 10, 20) 
        layout.setSpacing(10)

        logo = QtWidgets.QLabel("🎓 STUDENT")
        logo.setAlignment(QtCore.Qt.AlignCenter)
        logo.setObjectName("logo_text")
        layout.addWidget(logo)
        
        layout.addSpacing(20)

        for text in ["🏠 Trang Chủ", "👨‍🎓 Sinh Viên", "📚 Môn Học"]:
            btn = QtWidgets.QPushButton(text)
            btn.setObjectName("menu_btn")
            btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) 
            layout.addWidget(btn)

        layout.addStretch()
        self.main_layout.addWidget(self.sidebar)

    def setup_main(self):
        self.content_widget = QtWidgets.QWidget()
        self.content_widget.setObjectName("main_content")
        content_layout = QtWidgets.QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(30, 20, 30, 20)
        header_layout = QtWidgets.QHBoxLayout()
        title_layout = QtWidgets.QVBoxLayout()
        title_label = QtWidgets.QLabel("Students")
        title_label.setObjectName("page_title")
        subtitle_label = QtWidgets.QLabel("Dashboard / Students")
        subtitle_label.setObjectName("page_subtitle")
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        export_btn = QtWidgets.QPushButton("📥 Xuất Excel")
        export_btn.setObjectName("btn_secondary")
        export_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        export_btn.clicked.connect(self.export_excel)
        
        add_btn = QtWidgets.QPushButton("➕ Thêm mới")
        add_btn.setObjectName("btn_primary")
        add_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        add_btn.clicked.connect(self.add_student)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(export_btn)
        header_layout.addWidget(add_btn)
        
        content_layout.addLayout(header_layout)
        content_layout.addSpacing(20)

        filter_layout = QtWidgets.QHBoxLayout()
        class_label = QtWidgets.QLabel("Chọn lớp:")
        self.class_combo = QtWidgets.QComboBox()
        self.class_combo.addItems(["--Chọn--", "D15CNPM1", "D15CNPM2"])
        
        search_label = QtWidgets.QLabel("Tìm kiếm:")
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên sinh viên...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self.search_student)
        
        filter_layout.addWidget(class_label)
        filter_layout.addWidget(self.class_combo)
        filter_layout.addSpacing(20)
        filter_layout.addWidget(search_label)
        filter_layout.addWidget(self.search_input)
        filter_layout.addStretch()
        
        content_layout.addLayout(filter_layout)
        content_layout.addSpacing(15)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "MSV", "Họ Tên", "Lớp Học", "Chuyên Ngành", 
            "Ngày Sinh", "Số Điện Thoại", "Địa Chỉ", "Hành Động"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents) # MSV
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents) # Lớp Học
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents) # Ngày Sinh
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents) # SĐT
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents) # Hành Động

        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)          # Họ Tên
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)          # Chuyên Ngành
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)          # Địa Chỉ
        
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setShowGrid(False) 
        self.table.setAlternatingRowColors(True)

        self.table.verticalHeader().setDefaultSectionSize(45)
        self.table.verticalHeader().setVisible(False)

        content_layout.addWidget(self.table)
        self.main_layout.addWidget(self.content_widget)

    def load_data(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        conn.close()

        self.display(rows)

    def display(self, rows):
        self.table.setRowCount(0)

        for row_idx, row in enumerate(rows):
            self.table.insertRow(row_idx)

            for col in range(1, len(row)):
                item = QtWidgets.QTableWidgetItem(str(row[col]))
                item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter) 
                self.table.setItem(row_idx, col - 1, item)

            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(widget)

            edit = QtWidgets.QPushButton("✏")
            edit.setObjectName("action_btn_edit")
            edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            
            delete = QtWidgets.QPushButton("🗑")
            delete.setObjectName("action_btn_delete")
            delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

            edit.clicked.connect(lambda _, r=row: self.edit_student(r))
            delete.clicked.connect(lambda _, r=row: self.delete_student(r[0]))

            layout.addWidget(edit)
            layout.addWidget(delete)
            layout.setContentsMargins(5, 5, 5, 5)

            self.table.setCellWidget(row_idx, 7, widget)

    def add_student(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Thêm sinh viên")
        dialog.resize(400, 300)

        layout = QtWidgets.QFormLayout(dialog)

        fields = [QtWidgets.QLineEdit() for _ in range(7)]
        labels = ["MSV", "Tên", "Lớp", "Ngành", "Ngày sinh", "SĐT", "Địa chỉ"]

        for l, f in zip(labels, fields):
            f.setMinimumHeight(40)
            layout.addRow(l, f)

        btn = QtWidgets.QPushButton("Lưu")
        btn.setObjectName("btn_primary")
        btn.setMinimumHeight(35)
        layout.addWidget(btn)

        def save():
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (mssv, name, class, major, birthday, phone, address)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [f.text() for f in fields])
            conn.commit()
            conn.close()
            dialog.accept()
            self.load_data()

        btn.clicked.connect(save)
        dialog.exec_()

    def edit_student(self, data):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Sửa sinh viên")
        dialog.setMinimumWidth(400)
        layout = QtWidgets.QFormLayout(dialog)

        fields = [QtWidgets.QLineEdit(str(data[i])) for i in range(1, 8)]
        labels = ["MSV", "Tên", "Lớp", "Ngành", "Ngày sinh" , "SĐT", "Địa chỉ"]

        for l, f in zip(labels, fields):
            f.setMinimumHeight(40)
            layout.addRow(l, f)

        btn = QtWidgets.QPushButton("Cập nhật")
        btn.setObjectName("btn_primary")
        btn.setMinimumHeight(35)
        layout.addWidget(btn)

        def update():
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE students SET
                    mssv=?, name=?, class=?, major=?, birthday=?, phone=?, address=?
                WHERE id=?
            """, [f.text() for f in fields] + [data[0]])
            conn.commit()
            conn.close()
            dialog.accept()
            self.load_data()

        btn.clicked.connect(update)
        dialog.exec_()

    def delete_student(self, id):
        if QtWidgets.QMessageBox.question(self, "Xóa", "Chắc chắn xóa?") == QtWidgets.QMessageBox.Yes:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id=?", (id,))
            conn.commit()
            conn.close()
            self.load_data()

    def search_student(self):
        keyword = self.search_input.text()

        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + keyword + '%',))
        rows = cursor.fetchall()
        conn.close()

        self.display(rows)

    def filter_class(self):
        cls = self.class_combo.currentText()

        conn = connect()
        cursor = conn.cursor()

        if cls == "--Chọn--":
            cursor.execute("SELECT * FROM students")
        else:
            cursor.execute("SELECT * FROM students WHERE class=?", (cls,))

        rows = cursor.fetchall()
        conn.close()

        self.display(rows)

    def export_excel(self):
        conn = connect()
        df = pd.read_sql_query("SELECT * FROM students", conn)
        conn.close()

        df.to_excel("students.xlsx", index=False)
        QtWidgets.QMessageBox.information(self, "OK", "Xuất Excel thành công!")

    def apply_stylesheet(self):
        self.setStyleSheet("""
            /* SỬA Ở ĐÂY: Áp dụng font chữ toàn cục cho giao diện */
            * {
                font-family: 'Segoe UI', 'Roboto', 'Open Sans', Arial, sans-serif;
                font-size: 14px;
            }
            QMainWindow{
                background-color: #F8F9FD;
            }
            #sidebar{
                background-color: #FFFFFF;
                border-right: 1px solid #E0E0E0;
            }
            #logo_text{
                font-size: 22px;
                font-weight: 800;
                color: #2196F3;
                margin-bottom: 10px;
            }
            QPushButton#menu_btn{
                text-align: left;
                padding: 12px 15px;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                color: #555555;
                font-weight: 600;
            }
            QPushButton#menu_btn:hover{
                background-color: #F0F4FF;
                color: #2196F3;
            }
            #main_content{
                background-color: #F8F9FD;
            }
            #page_title{
                font-size: 26px;
                font-weight: bold;
                color: #333333;
            }
            #page_subtitle{
                font-size: 13px;
                color: #888888;
            }
            QPushButton#btn_primary{
                background-color: #FFC107;
                color: #333333;
                border: none;
                border-radius: 6px;
                padding: 8px 18px;
                font-weight: bold;
            }
            QPushButton#btn_primary:hover{
                background-color: #FFB300;
            }
            QPushButton#btn_secondary{
                background-color: #FFFFFF;
                color: #FFC107;
                border: 2px solid #FFC107;
                border-radius: 6px;
                padding: 7px 18px;
                font-weight: bold;
            }
            QPushButton#btn_secondary:hover{
                background-color: #FFF8E1;
            }
            QLineEdit, QComboBox{
                padding: 8px;
                border: 1px solid #D0D0D0;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus{
                border: 1px solid #2196F3;
            }
            QTableWidget{
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                gridline-color: #F0F0F0;
                outline: 0;
            }
            
            QHeaderView::section{
                background-color: #FFFFFF;
                padding: 12px 10px;
                border: none;
                border-bottom: 2px solid #E0E0E0;
                font-weight: bold;
                font-size: 14px;
                color: #444444;
                min-height: 40px;
                qproperty-alignment: AlignCenter;
            }
            
            QTableWidget::item{
                padding: 5px 10px;
                border-bottom: 1px solid #F5F5F5;
            }
            QPushButton#action_btn_edit{
                background-color: #E3F2FD;
                color: #1976D2;
                border: none;
                border-radius: 4px;
                padding: 6px;
                font-size: 16px;
            }
            QPushButton#action_btn_edit:hover{
                background-color: #BBDEFB;
            }
            QPushButton#action_btn_delete{
                background-color: #FFEBEE;
                color: #D32F2F;
                border: none;
                border-radius: 4px;
                padding: 6px;
                font-size: 16px;
            }
            QPushButton#action_btn_delete:hover {
                background-color: #FFCDD2;
            }
        """)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    font = QtGui.QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = StudentWindow()
    window.show()
    sys.exit(app.exec_())