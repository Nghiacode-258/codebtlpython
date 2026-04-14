import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets

import setting
from lophanhchinh import StudentDashboard
from thongtincanhan import PersonalInfoWidget
from homepage import Studenthomepage

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(r"D:\VS code\codewep\btlpython\key.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

class StudentWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("I love the AI department")
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
        self.sidebar.setFixedWidth(250)
        self.sidebar.setObjectName("sidebar")

        layout = QtWidgets.QVBoxLayout(self.sidebar)
        layout.setContentsMargins(15, 30, 15, 20) 
        layout.setSpacing(2)

        logo = QtWidgets.QLabel("🎓 S-Link")
        logo.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        logo.setObjectName("logo_text")
        layout.addWidget(logo)
        
        layout.addSpacing(20)

        self.menu_buttons = []
        menu_items = [
            {"type": "header", "text": "TỔNG QUAN"},
            {"type": "active_btn", "text": "🎛️  Trang chủ"},
            {"type": "btn", "text": "👤  Thông tin cá nhân"},
            {"type": "space", "height": 15},
            
            {"type": "header", "text": "QUẢN LÝ"},
            {"type": "btn", "text": "👥  Danh sách sinh viên"},
            {"type": "btn", "text": "📖  Lớp tín chỉ"},
            {"type": "btn", "text": "📅  Lớp hành chính"},
            {"type": "space", "height": 15},
            
            {"type": "header", "text": "HỆ THỐNG"},
            {"type": "btn", "text": "⚙️  Cài đặt"},
        ]

        for item in menu_items:
            if item["type"] == "header":
                lbl = QtWidgets.QLabel(item["text"])
                lbl.setObjectName("menu_header")
                layout.addWidget(lbl)
            
            elif item["type"] == "btn" or item["type"] == "active_btn":
                btn = QtWidgets.QPushButton(item["text"])
                btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.menu_buttons.append(btn)
                
                # SẮP XẾP LẠI INDEX CHUẨN XÁC THEO THỨ TỰ TỪ TRÊN XUỐNG
                idx = -1
                text = item["text"]
                if "Trang chủ" in text: 
                    idx = 0
                elif "Thông tin cá nhân" in text: 
                    idx = 1
                elif "Danh sách sinh viên" in text: 
                    idx = 2
                elif "Lớp tín chỉ" in text: 
                    idx = 3
                elif "Lớp hành chính" in text: 
                    idx = 4
                elif "Cài đặt" in text: 
                    idx = 5
                
                if item["type"] == "active_btn":
                    btn.setObjectName("menu_btn_active")
                else:
                    btn.setObjectName("menu_btn")
                    
                btn.clicked.connect(lambda _, b=btn, i=idx: self.handle_menu_click(b, i))
                layout.addWidget(btn)
            
            elif item["type"] == "space":
                layout.addSpacing(item["height"])

        layout.addStretch()
        self.main_layout.addWidget(self.sidebar)

    def handle_menu_click(self, clicked_btn, index):
        for btn in self.menu_buttons:
            btn.setObjectName("menu_btn")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        clicked_btn.setObjectName("menu_btn_active")
        clicked_btn.style().unpolish(clicked_btn)
        clicked_btn.style().polish(clicked_btn)

        if index != -1:
            self.stacked_widget.setCurrentIndex(index)
    def setup_main(self):
        self.stacked_widget = QtWidgets.QStackedWidget()

        # ==========================================
        # 1. KHỞI TẠO TẤT CẢ CÁC TRANG CỦA BẠN
        # ==========================================
        
        # Trang 0: Trang chủ
        self.home_page = Studenthomepage()
        
        # Trang 1: Thông tin cá nhân
        self.personal_info_page = PersonalInfoWidget()

        # Trang 2: Danh sách sinh viên
        self.student_page = QtWidgets.QWidget()
        self.student_page.setObjectName("main_content")
        content_layout = QtWidgets.QVBoxLayout(self.student_page)
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
        self.class_combo.currentTextChanged.connect(self.filter_class)
        
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
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents) 

        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)          
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)          
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)          
        
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setShowGrid(False) 
        self.table.setAlternatingRowColors(True)

        self.table.verticalHeader().setDefaultSectionSize(45)
        self.table.verticalHeader().setVisible(False)

        content_layout.addWidget(self.table)
        self.credit_class_page = QtWidgets.QWidget()
        self.credit_class_page.setObjectName("main_content")
        self.admin_class_page = StudentDashboard()
        self.setting_page = setting.SettingsWidget()

        self.stacked_widget.addWidget(self.home_page)           
        self.stacked_widget.addWidget(self.personal_info_page)   
        self.stacked_widget.addWidget(self.student_page)       
        self.stacked_widget.addWidget(self.credit_class_page)    
        self.stacked_widget.addWidget(self.admin_class_page)  
        self.stacked_widget.addWidget(self.setting_page)

        self.main_layout.addWidget(self.stacked_widget)
    def load_data(self):
        try:
            docs = db.collection("students").stream()
            rows = []
            for doc in docs:
                data = doc.to_dict()
                rows.append([
                    doc.id,
                    data.get("mssv", ""),
                    data.get("name", ""),
                    data.get("class", ""),
                    data.get("major", ""),
                    data.get("birthday", ""),
                    data.get("phone", ""),
                    data.get("address", ""),
                ])
            self.display(rows)
        except Exception as e:
            print(f"Lỗi tải dữ liệu: {e}")

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
            if not fields[0].text() or not fields[1].text():
                QtWidgets.QMessageBox.warning(dialog, "Lỗi", "MSV và Tên không được trống!")
                return

            db.collection("students").add({
                "mssv": fields[0].text(),
                "name": fields[1].text(),
                "class": fields[2].text(),
                "major": fields[3].text(),
                "birthday": fields[4].text(),
                "phone": fields[5].text(),
                "address": fields[6].text(),
            })

            dialog.accept()
            self.load_data()

        btn.clicked.connect(save)
        dialog.exec_()

    def edit_student(self, data):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Sửa sinh viên")
        dialog.resize(400, 300)

        layout = QtWidgets.QFormLayout(dialog)

        fields = [QtWidgets.QLineEdit() for _ in range(7)]
        labels = ["MSV", "Tên", "Lớp", "Ngành", "Ngày sinh", "SĐT", "Địa chỉ"]

        for i, f in enumerate(fields):
            f.setText(str(data[i+1]))
            f.setMinimumHeight(40)
            layout.addRow(labels[i], f)

        btn = QtWidgets.QPushButton("Cập nhật")
        btn.setObjectName("btn_primary")
        layout.addWidget(btn)

        def update_data():
            if not fields[0].text() or not fields[1].text():
                QtWidgets.QMessageBox.warning(dialog, "Lỗi", "MSV và Tên không được trống!")
                return
            db.collection("students").document(data[0]).update({
                "mssv": fields[0].text(),
                "name": fields[1].text(),
                "class": fields[2].text(),
                "major": fields[3].text(),
                "birthday": fields[4].text(),
                "phone": fields[5].text(),
                "address": fields[6].text(),
            })

            dialog.accept()
            self.load_data()

        btn.clicked.connect(update_data)
        dialog.exec_()

    def delete_student(self, id):
        if QtWidgets.QMessageBox.question(self, "Xóa", "Chắc chắn xóa?") == QtWidgets.QMessageBox.Yes:
            db.collection("students").document(id).delete()
            self.load_data()

    def search_student(self):
        keyword = self.search_input.text().lower()
        docs = db.collection("students").stream()
        results = []
        for doc in docs:
            d = doc.to_dict()
            if keyword in d.get("name", "").lower() or keyword in d.get("mssv", "").lower():
                results.append([doc.id, d.get("mssv"), d.get("name"), d.get("class"), 
                                d.get("major"), d.get("birthday"), d.get("phone"), d.get("address")])
        self.display(results)

    def filter_class(self):
        cls = self.class_combo.currentText()
        if cls == "--Chọn--":
            self.load_data()
            return

        docs = db.collection("students").where("class", "==", cls).stream()
        results = []
        for doc in docs:
            d = doc.to_dict()
            results.append([doc.id, d.get("mssv"), d.get("name"), d.get("class"), 
                            d.get("major"), d.get("birthday"), d.get("phone"), d.get("address")])
        self.display(results)

    def export_excel(self):
        docs = db.collection("students").stream()
        data_list = []
        for doc in docs:
            d = doc.to_dict()
            d["id"] = doc.id
            data_list.append(d)
        if not data_list:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Không có dữ liệu để xuất!")
            return
            
        df = pd.DataFrame(data_list)
        df.to_excel("students_cloud.xlsx", index=False)
        QtWidgets.QMessageBox.information(self, "Thành công", "Đã xuất file students_cloud.xlsx")

    def open_setting_window(self):
        self.setting_window = setting.SettingsWidget() 
        self.setting_window.show()

    def apply_stylesheet(self):
        self.setStyleSheet("""
            * {
                font-family: 'Segoe UI', 'Roboto', 'Open Sans', Arial, sans-serif;
                font-size: 14px;
                color: #333333; 
            }
            QMainWindow {
                background-color: #F5F6F8; /* Nền xám nhạt để làm nổi bật các khối trắng */
            }
            #sidebar {
                background-color: #FFFFFF;
                border-right: 1px solid #E0E0E0;
            }
            #logo_text {
                font-size: 22px;
                font-weight: 800;
                color: #D32F2F;
                margin-bottom: 10px;
            }
            
            #menu_header {
                color: #B0B0B0;
                font-size: 12px;
                font-weight: bold;
                padding-left: 10px;
                margin-top: 10px;
                margin-bottom: 5px;
            }
            
            QPushButton#menu_btn {
                text-align: left;
                padding: 10px 15px;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                color: #555555; /* Màu xám đậm */
                background-color: transparent;
                font-weight: 600;
            }
            QPushButton#menu_btn:hover {
                background-color: #FFEBEE; /* Hiện nền xám nhạt khi di chuột vào */
            }

            QPushButton#menu_btn_active {
                text-align: left;
                padding: 10px 15px;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                color: #FFFFFF;
                background-color: #D32F2F; 
                font-weight: 600;
            }

            #main_content {
                background-color: #F5F6F8;
            }
            #page_title {
                font-size: 26px;
                font-weight: bold;
                color: #333333;
            }
            #page_subtitle {
                font-size: 13px;
                color: #888888;
            }

            QPushButton#btn_primary {
                background-color: #D32F2F; 
                color: #FFFFFF; 
                border: none;
                border-radius: 6px;
                padding: 8px 18px;
                font-weight: bold;
            }
            QPushButton#btn_primary:hover {
                background-color: #B71C1C;
            }
            
            QPushButton#btn_secondary {
                background-color: #FFFFFF;
                color: #D32F2F;
                border: 2px solid #D32F2F;
                border-radius: 6px;
                padding: 7px 18px;
                font-weight: bold;
            }
            QPushButton#btn_secondary:hover {
                background-color: #FFEBEE;
            }
            
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #D0D0D0;
                border-radius: 5px;
                background-color: white;
                color: #333333;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #D32F2F;
            }
            
            QTableWidget {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                gridline-color: #F0F0F0;
                outline: 0;
            }
            QHeaderView::section {
                background-color: #FFFFFF;
                padding: 12px 10px;
                border: none;
                border-bottom: 2px solid #D32F2F;
                font-weight: bold;
                font-size: 14px;
                color: #333333;
                min-height: 40px;
                qproperty-alignment: AlignCenter;
            }
            QTableWidget::item {
                padding: 5px 10px;
                border-bottom: 1px solid #F5F5F5;
            }
            
            /* Các nút hành động trong bảng */
            QPushButton#action_btn_edit {
                background-color: #F5F5F5;
                color: #333333;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 6px;
                font-size: 16px;
            }
            QPushButton#action_btn_edit:hover {
                background-color: #E0E0E0;
            }
            QPushButton#action_btn_delete {
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