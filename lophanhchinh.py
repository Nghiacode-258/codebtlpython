from PyQt5 import QtCore, QtGui, QtWidgets
from firebase_config import db

AVATAR_COLORS = [
    "#FF4D4F","#597EF7","#36CFC9","#73D13D",
    "#FFC53D","#FF7A45","#9254DE","#40A9FF",
]

def get_initials(name: str) -> str:
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[-1][0] + parts[0][0]).upper()
    return parts[0][0].upper()

class AvatarWidget(QtWidgets.QWidget):
    def __init__(self, name, color, size=48, font_size=15, parent=None):
        super().__init__(parent)
        self.initials  = get_initials(name)
        self.color     = QtGui.QColor(color)
        self.font_size = font_size
        self.setFixedSize(size, size)

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        path = QtGui.QPainterPath()
        path.addEllipse(0, 0, self.width(), self.height())
        p.fillPath(path, QtGui.QBrush(self.color))
        p.setPen(QtGui.QColor("white"))
        p.setFont(QtGui.QFont("Segoe UI", self.font_size, QtGui.QFont.Bold))
        p.drawText(self.rect(), QtCore.Qt.AlignCenter, self.initials)

class StudentCard(QtWidgets.QFrame):
    clicked = QtCore.pyqtSignal(dict)

    def __init__(self, student: dict, color: str, parent=None):
        super().__init__(parent)
        self.student = student
        self.setMinimumHeight(148)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self._apply_normal_style()

        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 2)
        shadow.setColor(QtGui.QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 14, 12, 10)
        layout.setSpacing(3)
        layout.setAlignment(QtCore.Qt.AlignHCenter)

        av = AvatarWidget(student["name"], color, size=44, font_size=15)
        layout.addWidget(av, alignment=QtCore.Qt.AlignHCenter)
        layout.addSpacing(4)

        name_lbl = QtWidgets.QLabel(student["name"])
        name_lbl.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
        name_lbl.setStyleSheet("color: #111827; border: none; background: transparent;")
        name_lbl.setAlignment(QtCore.Qt.AlignCenter)
        name_lbl.setWordWrap(True)
        layout.addWidget(name_lbl)

        meta = QtWidgets.QLabel(f"{student['id']} · {student['gender']}")
        meta.setFont(QtGui.QFont("Segoe UI", 9))
        meta.setStyleSheet("color: #9CA3AF; border: none; background: transparent;")
        meta.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(meta)

        role_color = "#C81E1E" if student["role"] == "Lớp trưởng" else (
                     "#597EF7" if student["role"] == "Lớp phó" else "#9CA3AF")
        role_lbl = QtWidgets.QLabel(student["role"])
        role_lbl.setFont(QtGui.QFont("Segoe UI", 9))
        role_lbl.setStyleSheet(f"color: {role_color}; border: none; background: transparent;")
        role_lbl.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(role_lbl)

    def _apply_normal_style(self):
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1.5px solid #E5E7EB;
                border-radius: 10px;
            }
        """)

    def _apply_hover_style(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #FFF0F0;
                border: 1.5px solid #C81E1E;
                border-radius: 10px;
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit(self.student)

    def leaveEvent(self, event):
        self._apply_normal_style()

    def enterEvent(self, event):
        self._apply_hover_style()

        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(120)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(self.pos() - QtCore.QPoint(0, 6))
        self.anim.start()


    def leaveEvent(self, event):
        self._apply_normal_style()

        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(120)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(self.pos() + QtCore.QPoint(0, 6))
        self.anim.start()

class AddStudentDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm sinh viên")
        self.setFixedSize(320, 420)

        layout = QtWidgets.QVBoxLayout(self)

        self.inputs = {}

        fields = [
            ("name", "Họ tên"),
            ("id", "Mã SV"),
            ("email", "Email"),
            ("gender", "Giới tính"),
            ("dob", "Ngày sinh"),
            ("phone", "SĐT"),
            ("role", "Vai trò"),
        ]

        for key, label in fields:
            lbl = QtWidgets.QLabel(label)
            edit = QtWidgets.QLineEdit()
            edit.setPlaceholderText(label)

            layout.addWidget(lbl)
            layout.addWidget(edit)

            self.inputs[key] = edit

        btn = QtWidgets.QPushButton("Thêm sinh viên")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

    def get_data(self):
        return {k: v.text() for k, v in self.inputs.items()}


# ─── Component: Modal chi tiết sinh viên ────────────────────────
class StudentModal(QtWidgets.QDialog):
    def __init__(self, student: dict, color: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thông tin sinh viên")
        self.setFixedSize(580, 320)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        container = QtWidgets.QFrame(self)
        container.setGeometry(0, 0, 580, 320)
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #E5E7EB;
            }
        """)
        shadow = QtWidgets.QGraphicsDropShadowEffect(container)
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 8)
        shadow.setColor(QtGui.QColor(0, 0, 0, 60))
        container.setGraphicsEffect(shadow)

        outer = QtWidgets.QHBoxLayout(container)
        outer.setContentsMargins(28, 28, 28, 28)
        outer.setSpacing(24)

        # Cột trái: avatar
        left_layout = QtWidgets.QVBoxLayout()
        left_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        left_layout.setSpacing(8)

        av = AvatarWidget(student["name"], color, size=88, font_size=30)
        left_layout.addWidget(av, alignment=QtCore.Qt.AlignHCenter)

        nm = QtWidgets.QLabel(student["name"])
        nm.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Bold))
        nm.setStyleSheet("color: #111827;")
        nm.setAlignment(QtCore.Qt.AlignCenter)
        nm.setWordWrap(True)
        nm.setMaximumWidth(120)
        left_layout.addWidget(nm)

        role_color = "#C81E1E" if student["role"] == "Lớp trưởng" else (
                     "#597EF7" if student["role"] == "Lớp phó" else "#6B7280")
        rl = QtWidgets.QLabel(student["role"])
        rl.setFont(QtGui.QFont("Segoe UI", 10))
        rl.setStyleSheet(f"color: {role_color};")
        rl.setAlignment(QtCore.Qt.AlignCenter)
        left_layout.addWidget(rl)

        left_w = QtWidgets.QWidget()
        left_w.setLayout(left_layout)
        left_w.setFixedWidth(130)
        outer.addWidget(left_w)

        # Đường kẻ dọc
        div = QtWidgets.QFrame()
        div.setFrameShape(QtWidgets.QFrame.VLine)
        div.setStyleSheet("background: #E5E7EB; border: none; max-width: 1px;")
        outer.addWidget(div)

        # Cột phải: thông tin
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.setSpacing(0)

        fields = [
            ("Họ tên",            student["name"]),
            ("Mã sinh viên",      student["id"]),
            ("Email",             student["email"]),
            ("Giới tính",         student["gender"]),
            ("Ngày sinh",         student["dob"]),
            ("Số điện thoại",     student["phone"]),
            ("Vai trò trong lớp", student["role"]),
        ]
        for label, value in fields:
            row = QtWidgets.QHBoxLayout()
            row.setContentsMargins(0, 6, 0, 6)
            lbl = QtWidgets.QLabel(label)
            lbl.setFont(QtGui.QFont("Segoe UI", 10))
            lbl.setStyleSheet("color: #6B7280;")
            lbl.setFixedWidth(140)
            val = QtWidgets.QLabel(value)
            val.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold if label == "Họ tên" else QtGui.QFont.Normal))
            val.setStyleSheet("color: #111827;")
            row.addWidget(lbl)
            row.addWidget(val, 1)
            right_layout.addLayout(row)

            sep = QtWidgets.QFrame()
            sep.setFrameShape(QtWidgets.QFrame.HLine)
            sep.setStyleSheet("background: #F3F4F6; border: none; max-height: 1px;")
            right_layout.addWidget(sep)

        right_layout.addStretch()

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch()
        close_btn = QtWidgets.QPushButton("Đóng")
        close_btn.setFixedSize(88, 34)
        close_btn.setFont(QtGui.QFont("Segoe UI", 10))
        close_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        close_btn.setStyleSheet("""
            QPushButton { background-color: #F3F4F6; border: none; border-radius: 8px; color: #4B5563; }
            QPushButton:hover { background-color: #FFF0F0; color: #C81E1E; }
        """)
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        right_layout.addLayout(btn_row)

        right_w = QtWidgets.QWidget()
        right_w.setLayout(right_layout)
        outer.addWidget(right_w, 1)

        # Nút X góc trên phải
        x_btn = QtWidgets.QPushButton("✕", container)
        x_btn.setFixedSize(28, 28)
        x_btn.move(544, 12)
        x_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        x_btn.setStyleSheet("""
            QPushButton { background-color: #F3F4F6; border: none; border-radius: 14px; color: #6B7280; }
            QPushButton:hover { background-color: #FFF0F0; color: #C81E1E; }
        """)
        x_btn.clicked.connect(self.accept)

class StudentDashboard(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel#pageTitle {
                font-size: 22px;
                font-weight: bold;
                color: #111827;
            }
            QWidget#tabContainer {
                background-color: #F3F4F6;
                border-radius: 10px;
            }
            QPushButton.tabButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 13px;
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
                font-size: 14px;
                font-weight: bold;
                color: #111827;
            }
            QLabel.cardSubtitle {
                font-size: 12px;
                color: #6B7280;
            }
            QLabel.inputLabel {
                font-size: 12px;
                color: #9CA3AF;
            }
            QLabel.inputValue {
                font-size: 13px;
                font-weight: bold;
                color: #111827;
            }
            QLineEdit {
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: white;
                font-size: 13px;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #C81E1E;
            }
            QComboBox {
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 6px 12px;
                background-color: white;
                font-size: 12px;
                color: #374151;
                min-width: 140px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #E5E7EB;
                selection-background-color: #FFF0F0;
                selection-color: #C81E1E;
            }
        """)
        self.all_students = self.load_students()
        self.filtered     = list(self.all_students)
        self.setup_ui()
    
    def load_students(self):
        try:
            students_node = db.child("students").get()
            result = []
            
            if students_node.each():
                for student in students_node.each():
                    data = student.val()
                    data['firebase_key'] = student.key() 
                    result.append(data)
            return result
        except Exception as e:
            print("Lỗi khi tải dữ liệu từ Firebase:", e)
            return []

    def add_student(self):
        dlg = AddStudentDialog(self)
        if dlg.exec_():
            data = dlg.get_data()
            if not data["name"] or not data["id"]:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Phải nhập tên và mã sinh viên!")
                return

            try:
                db.child("students").push(data)
                QtWidgets.QMessageBox.information(self, "Thành công", "Đã thêm sinh viên!")
                self.all_students = self.load_students()
                self.filtered = list(self.all_students)
                self.render_student_grid()
                self.count_lbl.setText(f"Danh sách sinh viên ({len(self.filtered)})")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Lỗi Firebase", f"Không thể thêm sinh viên: {str(e)}")

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.create_header())
        main_layout.addWidget(self.create_tab_bar())
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setStyleSheet("background: #F5F5F5; border: none;")

        body_w = QtWidgets.QWidget()
        body_w.setStyleSheet("background: #F5F5F5;")
        body_layout = QtWidgets.QHBoxLayout(body_w)
        body_layout.setContentsMargins(20, 20, 20, 20)
        body_layout.setSpacing(20)
        body_layout.setAlignment(QtCore.Qt.AlignTop)

        body_layout.addWidget(self.create_left_column(), 7)
        body_layout.addWidget(self.create_right_column(), 3)

        scroll.setWidget(body_w)
        main_layout.addWidget(scroll, 1)
    def create_header(self):
        header = QtWidgets.QFrame()
        header.setFixedHeight(56)
        header.setStyleSheet("background-color: white; border-bottom: 1px solid #E5E7EB;")

        layout = QtWidgets.QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)

        title = QtWidgets.QLabel("Lớp hành chính")
        title.setObjectName("pageTitle")
        layout.addWidget(title)
        layout.addStretch()

        for items in [["Học kỳ 1 - 2024","Học kỳ 2 - 2024"], ["CNTT-K65-1","CNTT-K65-2","CNTT-K64-1"]]:
            combo = QtWidgets.QComboBox()
            for item in items:
                combo.addItem(item)
            layout.addWidget(combo)

        return header
    def create_tab_bar(self):
        tab_container = QtWidgets.QWidget()
        tab_container.setObjectName("tabContainer")
        tab_container.setFixedHeight(48)
        tab_container.setStyleSheet("background-color: white; border-bottom: 1px solid #E5E7EB;")

        layout = QtWidgets.QHBoxLayout(tab_container)
        layout.setContentsMargins(24, 0, 0, 0)
        layout.setSpacing(0)

        self.tab_btn_group = QtWidgets.QButtonGroup(self)

        for i, label in enumerate(["Lớp hành chính"]):
            btn = QtWidgets.QPushButton(label)
            btn.setProperty("class", "tabButton")
            btn.setCheckable(True)
            btn.setFixedHeight(48)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            if i == 0:
                btn.setChecked(True)
            self.tab_btn_group.addButton(btn, i)
            layout.addWidget(btn)

        layout.addStretch()
        return tab_container

    def create_left_column(self):
        widget = QtWidgets.QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addWidget(self.create_class_info_card())
        layout.addWidget(self.create_students_card())
        return widget

    def create_class_info_card(self):
        frame = QtWidgets.QFrame()
        frame.setProperty("class", "cardFrame")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        title = QtWidgets.QLabel("Thông tin lớp học")
        title.setProperty("class", "cardTitle")
        layout.addWidget(title)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(16)

        fields = [
            ("Tên lớp",           "CNTT-K65-1",            0, 0),
            ("Khoa sinh viên",    "Công nghệ Thông tin",    0, 1),
            ("Ngành đào tạo",     "Kỹ thuật Phần mềm",     1, 0),
            ("Vai trò trong lớp", "Lớp trưởng",            1, 1),
        ]
        for label, value, row, col in fields:
            box = QtWidgets.QVBoxLayout()
            box.setSpacing(3)
            lbl = QtWidgets.QLabel(label)
            lbl.setProperty("class", "inputLabel")
            val = QtWidgets.QLabel(value)
            val.setProperty("class", "inputValue")
            if label == "Vai trò trong lớp":
                val.setStyleSheet("color: #C81E1E; font-weight: bold;")
            box.addWidget(lbl)
            box.addWidget(val)
            w = QtWidgets.QWidget()
            w.setStyleSheet("background: transparent;")
            w.setLayout(box)
            grid.addWidget(w, row, col)

        layout.addLayout(grid)
        return frame

    def create_students_card(self):
        frame = QtWidgets.QFrame()
        frame.setProperty("class", "cardFrame")

        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Header
        header_row = QtWidgets.QHBoxLayout()
        self.count_lbl = QtWidgets.QLabel(f"Danh sách sinh viên ({len(self.all_students)})")
        self.count_lbl.setProperty("class", "cardTitle")
        header_row.addWidget(self.count_lbl)
        header_row.addStretch()
        add_btn = QtWidgets.QPushButton("+")
        add_btn.setFixedSize(32, 32)
        add_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        add_btn.clicked.connect(self.add_student)

        header_row.addWidget(add_btn)

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("🔍  Tìm sinh viên...")
        self.search_input.setFixedWidth(240)
        self.search_input.textChanged.connect(self.filter_students)
        header_row.addWidget(self.search_input)

        layout.addLayout(header_row)

        # Scroll area
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("""
            QScrollArea { background: transparent; }
            QScrollBar:vertical {
                width: 8px;
                background: transparent;
            }
            QScrollBar::handle:vertical {
                background: #D1D5DB;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9CA3AF;
            }
        """)

        self.grid_container = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(16)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll.setWidget(self.grid_container)
        layout.addWidget(self.scroll)

        self.render_student_grid()
        return frame

    def render_student_grid(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.filtered:
            empty = QtWidgets.QLabel("Không tìm thấy sinh viên nào")
            empty.setStyleSheet("color:#9CA3AF; font-size:14px;")
            empty.setAlignment(QtCore.Qt.AlignCenter)
            self.grid_layout.addWidget(empty, 0, 0)
            return

        container_width = self.scroll.viewport().width()
        card_width = 180
        spacing = 16
        cols = 4

        for i, student in enumerate(self.filtered):
            row = i // cols
            col = i % cols

            idx = self.all_students.index(student) if student in self.all_students else i
            color = AVATAR_COLORS[idx % len(AVATAR_COLORS)]

            card = StudentCard(student, color)
            card.clicked.connect(self.open_student_modal)

            self.grid_layout.addWidget(card, row, col)

        self.grid_layout.setAlignment(QtCore.Qt.AlignTop)

    def filter_students(self, text):
        q = text.strip().lower()
        self.filtered = [s for s in self.all_students
                         if q in s["name"].lower() or q in s["id"]]
        self.count_lbl.setText(f"Danh sách sinh viên ({len(self.filtered)})")
        self.render_student_grid()

    def open_student_modal(self, student):
        idx = self.all_students.index(student) if student in self.all_students else 0
        color = AVATAR_COLORS[idx % len(AVATAR_COLORS)]
        dlg   = StudentModal(student, color, self.window())
        dlg.exec_()

    def create_right_column(self):
        widget = QtWidgets.QWidget()
        widget.setStyleSheet("background: transparent;")
        widget.setFixedWidth(280)
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addWidget(self.create_advisor_card())
        layout.addWidget(self.create_nav_card())
        layout.addWidget(self.create_empty_card())
        return widget

    def create_advisor_card(self):
        frame = QtWidgets.QFrame()
        frame.setProperty("class", "cardFrame")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header đỏ
        hdr = QtWidgets.QFrame()
        hdr.setFixedHeight(48)
        hdr.setStyleSheet("background-color: #C81E1E; border-radius: 12px 12px 0 0;")
        hdr_layout = QtWidgets.QHBoxLayout(hdr)
        hdr_layout.setContentsMargins(16, 0, 16, 0)
        hdr_title = QtWidgets.QLabel("Cố vấn học tập")
        hdr_title.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Bold))
        hdr_title.setStyleSheet("color: white;")
        hdr_layout.addWidget(hdr_title)
        layout.addWidget(hdr)

        # Body
        body = QtWidgets.QWidget()
        body.setStyleSheet("background: transparent;")
        body_layout = QtWidgets.QVBoxLayout(body)
        body_layout.setContentsMargins(16, 10, 16, 10)
        body_layout.setSpacing(0)

        advisors = [
            ("TS. Nguyễn Thị Thu", "Giảng viên chính", "#C81E1E"),
            ("ThS. Lê Minh Khoa",  "Cố vấn phụ",       "#FA8C16"),
        ]
        for name, role, color in advisors:
            row = QtWidgets.QHBoxLayout()
            row.setContentsMargins(0, 8, 0, 8)
            av = AvatarWidget(name, color, size=36, font_size=12)
            row.addWidget(av)
            row.addSpacing(10)
            col = QtWidgets.QVBoxLayout()
            col.setSpacing(2)
            n = QtWidgets.QLabel(name)
            n.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Bold))
            n.setStyleSheet("color: #111827;")
            r = QtWidgets.QLabel(role)
            r.setFont(QtGui.QFont("Segoe UI", 9))
            r.setStyleSheet("color: #9CA3AF;")
            col.addWidget(n)
            col.addWidget(r)
            row.addLayout(col)
            row.addStretch()
            body_layout.addLayout(row)

            sep = QtWidgets.QFrame()
            sep.setFrameShape(QtWidgets.QFrame.HLine)
            sep.setStyleSheet("background: #F3F4F6; border: none; max-height: 1px;")
            body_layout.addWidget(sep)

        layout.addWidget(body)
        return frame

    def create_nav_card(self):
        frame = QtWidgets.QFrame()
        frame.setProperty("class", "cardFrame")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(0)

        title = QtWidgets.QLabel("Điều hướng lớp")
        title.setProperty("class", "cardTitle")
        layout.addWidget(title)
        layout.addSpacing(10)

        for label in ["Xem tất cả lớp", "Lịch sử hoạt động"]:
            row = QtWidgets.QHBoxLayout()
            row.setContentsMargins(0, 8, 0, 8)
            lbl = QtWidgets.QLabel(label)
            lbl.setFont(QtGui.QFont("Segoe UI", 11))
            lbl.setStyleSheet("color: #374151;")
            arrow = QtWidgets.QLabel("›")
            arrow.setFont(QtGui.QFont("Segoe UI", 14))
            arrow.setStyleSheet("color: #D1D5DB;")
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(arrow)
            layout.addLayout(row)
            sep = QtWidgets.QFrame()
            sep.setFrameShape(QtWidgets.QFrame.HLine)
            sep.setStyleSheet("background: #F3F4F6; border: none; max-height: 1px;")
            layout.addWidget(sep)

        return frame

    def create_empty_card(self):
        frame = QtWidgets.QFrame()
        frame.setProperty("class", "cardFrame")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        icon = QtWidgets.QLabel("+")
        icon.setFont(QtGui.QFont("Segoe UI", 22))
        icon.setStyleSheet("""
            color: #D1D5DB;
            background-color: #F3F4F6;
            border-radius: 24px;
            min-width: 48px; max-width: 48px;
            min-height: 48px; max-height: 48px;
        """)
        icon.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(icon, alignment=QtCore.Qt.AlignHCenter)

        lbl = QtWidgets.QLabel("Trống")
        lbl.setFont(QtGui.QFont("Segoe UI", 11))
        lbl.setStyleSheet("color: #D1D5DB;")
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(lbl)
        return frame

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QtGui.QFont("Segoe UI", 10))
    window = StudentDashboard()
    window.setWindowTitle("Quản lý sinh viên")
    window.resize(1280, 760)
    window.show()
    sys.exit(app.exec_())