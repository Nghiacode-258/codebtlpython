import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"D:\VS code\codewep\btlpython\key.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

PRIMARY = "#c8003a"
PRIMARY_DARK = "#8f0029"
PRIMARY_LIGHT = "#ff4d7a"
CARD_BG = "#ffffff"
PAGE_BG = "#fdf0f3"
TEXT_DARK = "#111827"
TEXT_MUTED = "#6b7280"
ACCENT_SOFT = "#ffe4ec"
BORDER_SOFT = "#f5c2cf"

COURSE_ICONS = ["📐", "📡", "🖥️", "📘", "⚡", "💻", "📚", "🧠", "📝"]


class StatCard(QtWidgets.QFrame):
    clicked = QtCore.pyqtSignal(dict)

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data
        self._build()

    def _build(self):
        self.setMinimumHeight(108)
        self.setMaximumHeight(108)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setObjectName("stat_card")
        self.setStyleSheet(f"""
            QFrame#stat_card {{
                background: {CARD_BG};
                border-radius: 16px;
                border: 1.5px solid {BORDER_SOFT};
            }}
            QFrame#stat_card:hover {{
                border: 1.5px solid {PRIMARY_LIGHT};
                background: #fff9fb;
            }}
        """)

        root = QtWidgets.QHBoxLayout(self)
        root.setContentsMargins(20, 14, 20, 14)
        root.setSpacing(12)

        left = QtWidgets.QVBoxLayout()
        left.setSpacing(2)

        self.lbl_title = QtWidgets.QLabel(self.data.get("title", ""))
        self.lbl_title.setStyleSheet(f"color: {TEXT_MUTED}; background: transparent; font-size: 13px; font-weight: 600;")

        val = str(self.data.get("value", ""))
        if len(val) > 15: val = val.replace("Học kỳ", "HK").replace("Năm học", "Năm")
        self.lbl_value = QtWidgets.QLabel(val)
        fs = 17 if len(val) > 10 else 24
        self.lbl_value.setStyleSheet(f"color: {PRIMARY}; background: transparent; font-size: {fs}px; font-weight: bold;")

        self.lbl_sub = QtWidgets.QLabel(self.data.get("sub", ""))
        self.lbl_sub.setStyleSheet(f"color: {TEXT_MUTED}; background: transparent; font-size: 11px;")
        self.lbl_sub.setWordWrap(True)

        left.addWidget(self.lbl_title)
        left.addWidget(self.lbl_value)
        left.addWidget(self.lbl_sub)
        left.addStretch()

        self.lbl_icon = QtWidgets.QLabel(self.data.get("icon", "📊"))
        self.lbl_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_icon.setFixedSize(50, 50)
        self.lbl_icon.setStyleSheet(f"""
            background: {ACCENT_SOFT};
            border-radius: 14px;
            color: {PRIMARY_DARK};
            font-size: 22px;
        """)

        root.addLayout(left, 1)
        root.addWidget(self.lbl_icon, 0, QtCore.Qt.AlignVCenter)

    def update_data(self, data: dict):
        self.data = data
        self.lbl_title.setText(data.get("title", ""))
        val = str(data.get("value", ""))
        if len(val) > 15: val = val.replace("Học kỳ", "HK").replace("Năm học", "Năm")
        self.lbl_value.setText(val)
        fs = 17 if len(val) > 10 else 24
        self.lbl_value.setStyleSheet(f"color: {PRIMARY}; background: transparent; font-size: {fs}px; font-weight: bold;")
        self.lbl_sub.setText(data.get("sub", ""))
        self.lbl_icon.setText(data.get("icon", "📊"))

    def mousePressEvent(self, event):
        self.clicked.emit(self.data)
        super().mousePressEvent(event)


class Chip(QtWidgets.QLabel):
    def __init__(self, label: str, value, parent=None):
        super().__init__(f"{label}: {value}", parent)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet(f"""
            background: {ACCENT_SOFT};
            color: {PRIMARY};
            border-radius: 8px;
            padding: 4px 10px;
            font-weight: bold;
            font-size: 12px;
        """)


class CourseCard(QtWidgets.QFrame):
    clicked = QtCore.pyqtSignal(dict)

    def __init__(self, data: dict, icon: str = "📚", parent=None):
        super().__init__(parent)
        self.data = data
        self.icon = icon
        self._build()

    def _build(self):
        self.setMinimumHeight(150)
        self.setMaximumHeight(160)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setObjectName("course_card")
        self.setStyleSheet(f"""
            QFrame#course_card {{
                background: {CARD_BG};
                border-radius: 16px;
                border: 1.5px solid {BORDER_SOFT};
            }}
            QFrame#course_card:hover {{
                border: 1.5px solid {PRIMARY_LIGHT};
                background: #fff9fb;
            }}
        """)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(8)

        header = QtWidgets.QHBoxLayout()
        header.setSpacing(8)

        self.lbl_code = QtWidgets.QLabel(self.data.get("code", ""))
        self.lbl_code.setStyleSheet(f"color: {PRIMARY}; background: transparent; font-size: 16px; font-weight: bold;")

        self.lbl_icon = QtWidgets.QLabel(self.icon)
        self.lbl_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_icon.setFixedSize(38, 38)
        self.lbl_icon.setStyleSheet(f"""
            background: {ACCENT_SOFT};
            border-radius: 11px;
            color: {PRIMARY_DARK};
            font-size: 20px;
        """)

        header.addWidget(self.lbl_code)
        header.addStretch()
        header.addWidget(self.lbl_icon)

        self.lbl_name = QtWidgets.QLabel(self.data.get("name", ""))
        self.lbl_name.setStyleSheet(f"color: {TEXT_DARK}; background: transparent; font-size: 14px; font-weight: 600;")
        self.lbl_name.setWordWrap(True)

        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setFixedHeight(1)
        divider.setStyleSheet(f"background: {BORDER_SOFT}; border: none;")

        stats_row = QtWidgets.QHBoxLayout()
        stats_row.setSpacing(6)
        stats_row.addWidget(Chip("Tín chỉ", self.data.get("credits", "")))
        stats_row.addWidget(Chip("Lớp HP", self.data.get("class_code", "")))
        stats_row.addWidget(Chip("Phòng", self.data.get("room", "")))
        stats_row.addStretch()

        root.addLayout(header)
        root.addWidget(self.lbl_name)
        root.addWidget(divider)
        root.addLayout(stats_row)
        root.addStretch()

    def mousePressEvent(self, event):
        self.clicked.emit(self.data)
        super().mousePressEvent(event)


class Studenthomepage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.stat_cards = []
        self.course_cards = []
        self.stats_data = []
        self.credit_rows = []
        self._last_stat_cols = -1
        self._last_course_cols = -1

        self._apply_style()
        self._build()
        self.load_dashboard_data()

    def _apply_style(self):
        self.setObjectName("homepage_root")
        self.setStyleSheet(f"""
            QWidget#homepage_root {{
                background: {PAGE_BG};
            }}
        """)

    def _build(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        self.scroll_content = QtWidgets.QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")
        
        layout = QtWidgets.QVBoxLayout(self.scroll_content)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(22)

        layout.addLayout(self._build_welcome())

        self.stats_container = QtWidgets.QWidget()
        self.stats_grid = QtWidgets.QGridLayout(self.stats_container)
        self.stats_grid.setContentsMargins(0, 0, 0, 0)
        self.stats_grid.setSpacing(16)
        layout.addWidget(self.stats_container)

        self.section_title = self._section_label("Lớp tín chỉ  📚")
        layout.addWidget(self.section_title)

        self.courses_container = QtWidgets.QWidget()
        self.courses_grid = QtWidgets.QGridLayout(self.courses_container)
        self.courses_grid.setContentsMargins(0, 0, 0, 0)
        self.courses_grid.setSpacing(18)
        layout.addWidget(self.courses_container)

        layout.addStretch()
        
        footer = QtWidgets.QLabel("🎓 S-Link - Hệ thống quản lý sinh viên")
        footer.setAlignment(QtCore.Qt.AlignCenter)
        footer.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px; margin-top: 20px;")
        layout.addWidget(footer)

        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        initial_stats = [
            {"title": "Tổng sinh viên", "value": "0", "icon": "👥", "sub": "Từ danh sách sinh viên"},
            {"title": "Lớp học", "value": "0", "icon": "🏫", "sub": "Tổng lớp tín chỉ"},
            {"title": "Tổng tín chỉ", "value": "0", "icon": "📊", "sub": "Từ collection credit"},
            {"title": "Học kỳ hiện tại", "value": "--", "icon": "📅", "sub": "Từ dữ liệu credit"},
        ]

        for data in initial_stats:
            card = StatCard(data)
            card.clicked.connect(self._on_stat_click)
            self.stat_cards.append(card)

    def _build_welcome(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(6)

        self.lbl_greeting = QtWidgets.QLabel("Chào mừng trở lại 👋")
        self.lbl_greeting.setStyleSheet(f"""
            color: {TEXT_DARK};
            background: transparent;
            font-weight: 800;
            font-size: 28px;
        """)

        self.lbl_sub = QtWidgets.QLabel("Quản lí sinh viên một cách hiệu quả")
        self.lbl_sub.setStyleSheet(f"""
            color: {TEXT_MUTED};
            background: transparent;
            font-weight: 600;
            font-size: 14px;
        """)

        layout.addWidget(self.lbl_greeting)
        layout.addWidget(self.lbl_sub)
        return layout

    def _section_label(self, text: str):
        label = QtWidgets.QLabel(text)
        label.setStyleSheet(f"""
            color: {TEXT_DARK};
            background: transparent;
            font-weight: 800;
            font-size: 20px;
        """)
        return label

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.setParent(None)
            elif child_layout is not None:
                self._clear_layout(child_layout)

    def _get_stat_columns(self):
        width = max(1, self.width())
        if width >= 1100:
            return 4
        if width >= 760:
            return 2
        return 1

    def _get_course_columns(self):
        width = max(1, self.width())
        if width >= 1200:
            return 3
        if width >= 760:
            return 2
        return 1

    def _rebuild_stats_grid(self):
        cols = self._get_stat_columns()
        if cols == self._last_stat_cols:
            return

        self._last_stat_cols = cols
        self._clear_layout(self.stats_grid)

        for i, card in enumerate(self.stat_cards):
            row = i // cols
            col = i % cols
            self.stats_grid.addWidget(card, row, col)

        for col in range(cols):
            self.stats_grid.setColumnStretch(col, 1)

    def _rebuild_courses_grid(self):
        cols = self._get_course_columns()
        if cols == self._last_course_cols and self.courses_grid.count() > 0:
            return

        self._last_course_cols = cols
        self._clear_layout(self.courses_grid)

        if not self.credit_rows:
            empty = QtWidgets.QLabel("Chưa có dữ liệu lớp tín chỉ")
            empty.setAlignment(QtCore.Qt.AlignCenter)
            empty.setMinimumHeight(120)
            empty.setStyleSheet(f"""
                color: {TEXT_MUTED};
                background: {CARD_BG};
                border: 1.5px solid {BORDER_SOFT};
                border-radius: 16px;
                font-size: 16px;
                font-weight: 600;
            """)
            self.courses_grid.addWidget(empty, 0, 0, 1, cols)
            return

        self.course_cards.clear()
        for i, course in enumerate(self.credit_rows):
            card = CourseCard(course, icon=COURSE_ICONS[i % len(COURSE_ICONS)])
            card.clicked.connect(self._on_course_click)
            self.course_cards.append(card)

            row = i // cols
            col = i % cols
            self.courses_grid.addWidget(card, row, col)

        for col in range(cols):
            self.courses_grid.setColumnStretch(col, 1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._rebuild_stats_grid()
        self._rebuild_courses_grid()

    def load_dashboard_data(self):
        total_students = 0
        credit_rows = []

        try:
            total_students = len(list(db.collection("students").stream()))
        except Exception as e:
            print(f"Lỗi tải tổng sinh viên: {e}")

        try:
            for doc in db.collection("credit").stream():
                data = doc.to_dict()
                credit_rows.append({
                    "id": doc.id,
                    "code": data.get("course_code", ""),
                    "name": data.get("course_name", ""),
                    "credits": data.get("credits", ""),
                    "class_code": data.get("class_code", ""),
                    "teacher": data.get("teacher", ""),
                    "schedule": data.get("schedule", ""),
                    "room": data.get("room", ""),
                    "size": data.get("size", ""),
                    "status": data.get("status", ""),
                    "semester": data.get("semester", ""),
                })
        except Exception as e:
            print(f"Lỗi tải lớp tín chỉ: {e}")

        total_credit_classes = len(credit_rows)

        total_credits = 0
        for row in credit_rows:
            try:
                total_credits += int(row.get("credits", 0))
            except Exception:
                pass

        current_semester = "--"
        if credit_rows:
            semester = str(credit_rows[0].get("semester", "")).strip()
            if semester:
                current_semester = semester

        self.stats_data = [
            {
                "title": "Tổng sinh viên",
                "value": str(total_students),
                "icon": "👥",
                "sub": "Từ danh sách sinh viên",
            },
            {
                "title": "Lớp học",
                "value": str(total_credit_classes),
                "icon": "🏫",
                "sub": "Tổng lớp tín chỉ",
            },
            {
                "title": "Tổng tín chỉ",
                "value": str(total_credits),
                "icon": "📊",
                "sub": "Từ collection credit",
            },
            {
                "title": "Học kỳ hiện tại",
                "value": current_semester,
                "icon": "📅",
                "sub": "Từ dữ liệu credit",
            },
        ]

        self.credit_rows = credit_rows
        self.update_stats(self.stats_data)
        self._rebuild_stats_grid()
        self._rebuild_courses_grid()

    def update_stats(self, stats):
        for i, data in enumerate(stats):
            if i < len(self.stat_cards):
                self.stat_cards[i].update_data(data)

    def refresh_data(self):
        self.load_dashboard_data()

    def _on_stat_click(self, data):
        print(f"[STAT] {data.get('title', '')} → {data.get('value', '')}")

    def _on_course_click(self, data):
        print(f"[COURSE] {data.get('code', '')} – {data.get('name', '')}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QtGui.QFont("Segoe UI", 10))

    window = Studenthomepage()
    window.resize(1200, 720)
    window.show()

    sys.exit(app.exec_())