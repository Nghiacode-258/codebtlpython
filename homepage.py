import sys
from PyQt5 import QtCore, QtGui, QtWidgets

PRIMARY        = "#c8003a"
PRIMARY_DARK   = "#a0002e"
PRIMARY_LIGHT  = "#ff4d7a"
CARD_BG        = "#ffffff"
PAGE_BG        = "#fdf0f3"
TEXT_DARK      = "#1a1a2e"
TEXT_MUTED     = "#9b8fa0"
ACCENT_SOFT    = "#ffe4ec"
BORDER_SOFT    = "#f5d0da"

STAT_DATA = [
    {"title": "Tổng sinh viên", "value": "2,543", "icon": "👥", "sub": "+12 tuần này"},
    {"title": "Lớp học",         "value": "48",    "icon": "🏫", "sub": "4 khoa"},
    {"title": "Điểm trung bình", "value": "7.5",   "icon": "📊", "sub": "Học kỳ này"},
    {"title": "Học kỳ hiện tại", "value": "HK 2",  "icon": "📅", "sub": "2024 – 2025"},
]

COURSE_DATA = [
    {"code": "BAS1269",  "name": "Xác suất thống kê",          "bt": 18, "tuan": 10, "diem": 8.2},
    {"code": "ELE1319",  "name": "Lý thuyết thông tin",        "bt": 22, "tuan": 11, "diem": 7.8},
    {"code": "INT13145", "name": "Kiến trúc máy tính",         "bt": 15, "tuan": 9,  "diem": 9.0},
    {"code": "MAT2040",  "name": "Giải tích 2",                 "bt": 20, "tuan": 12, "diem": 6.5},
    {"code": "PHY1110",  "name": "Vật lý đại cương",           "bt": 12, "tuan": 8,  "diem": 7.2},
    {"code": "CSE2030",  "name": "Lập trình hướng đối tượng",  "bt": 25, "tuan": 13, "diem": 9.5},
]

COURSE_ICONS = ["📐", "📡", "🖥️", "📘", "⚡", "💻"]


class StatCard(QtWidgets.QFrame):
    clicked = QtCore.pyqtSignal(dict)

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data
        self._build()

    def _build(self):
        self.setFixedHeight(110)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setStyleSheet(f"""
            StatCard {{
                background: {CARD_BG};
                border-radius: 16px;
                border: 1.5px solid {BORDER_SOFT};
            }}
            StatCard:hover {{
                border: 1.5px solid {PRIMARY_LIGHT};
                background: #fff9fb;
            }}
        """)

        root = QtWidgets.QHBoxLayout(self)
        root.setContentsMargins(20, 14, 20, 14)
        root.setSpacing(12)

        # ── Left text block ──
        left = QtWidgets.QVBoxLayout()
        left.setSpacing(2)

        lbl_title = QtWidgets.QLabel(self.data["title"])
        lbl_title.setFont(QtGui.QFont("Segoe UI", 10))
        lbl_title.setStyleSheet(f"color: {TEXT_MUTED}; background: transparent;")

        lbl_value = QtWidgets.QLabel(self.data["value"])
        lbl_value.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
        lbl_value.setStyleSheet(f"color: {PRIMARY}; background: transparent;")

        lbl_sub = QtWidgets.QLabel(self.data.get("sub", ""))
        lbl_sub.setFont(QtGui.QFont("Segoe UI", 8))
        lbl_sub.setStyleSheet(f"color: {TEXT_MUTED}; background: transparent;")

        left.addWidget(lbl_title)
        left.addWidget(lbl_value)
        left.addWidget(lbl_sub)
        left.addStretch()

        # ── Right icon bubble ──
        lbl_icon = QtWidgets.QLabel(self.data["icon"])
        lbl_icon.setFont(QtGui.QFont("Segoe UI", 20))
        lbl_icon.setAlignment(QtCore.Qt.AlignCenter)
        lbl_icon.setFixedSize(52, 52)
        lbl_icon.setStyleSheet(f"""
            background: {ACCENT_SOFT};
            border-radius: 14px;
        """)

        root.addLayout(left, 1)
        root.addWidget(lbl_icon, 0, QtCore.Qt.AlignVCenter)

    def mousePressEvent(self, event):
        self.clicked.emit(self.data)
        super().mousePressEvent(event)

class Chip(QtWidgets.QLabel):
    def __init__(self, label: str, value, parent=None):
        super().__init__(f"{label}: {value}", parent)
        self.setFont(QtGui.QFont("Segoe UI", 9))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet(f"""
            background: {ACCENT_SOFT};
            color: {PRIMARY};
            border-radius: 8px;
            padding: 3px 10px;
        """)


class CourseCard(QtWidgets.QFrame):
    clicked = QtCore.pyqtSignal(dict)

    def __init__(self, data: dict, icon: str = "📚", parent=None):
        super().__init__(parent)
        self.data = data
        self.icon = icon
        self._build()

    def _build(self):
        self.setMinimumHeight(155)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setStyleSheet(f"""
            CourseCard {{
                background: {CARD_BG};
                border-radius: 16px;
                border: 1.5px solid {BORDER_SOFT};
            }}
            CourseCard:hover {{
                border: 1.5px solid {PRIMARY_LIGHT};
                background: #fff9fb;
            }}
        """)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(8)

        # ── Header row ──
        header = QtWidgets.QHBoxLayout()
        header.setSpacing(8)

        lbl_code = QtWidgets.QLabel(self.data["code"])
        lbl_code.setFont(QtGui.QFont("Segoe UI", 13, QtGui.QFont.Bold))
        lbl_code.setStyleSheet(f"color: {PRIMARY}; background: transparent;")

        lbl_icon = QtWidgets.QLabel(self.icon)
        lbl_icon.setFont(QtGui.QFont("Segoe UI", 18))
        lbl_icon.setAlignment(QtCore.Qt.AlignCenter)
        lbl_icon.setFixedSize(38, 38)
        lbl_icon.setStyleSheet(f"""
            background: {ACCENT_SOFT};
            border-radius: 10px;
        """)

        header.addWidget(lbl_code)
        header.addStretch()
        header.addWidget(lbl_icon)

        # ── Course name ──
        lbl_name = QtWidgets.QLabel(self.data["name"])
        lbl_name.setFont(QtGui.QFont("Segoe UI", 10))
        lbl_name.setStyleSheet(f"color: {TEXT_DARK}; background: transparent;")
        lbl_name.setWordWrap(True)

        # ── Divider ──
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setFixedHeight(1)
        divider.setStyleSheet(f"background: {BORDER_SOFT}; border: none;")

        # ── Stats chips ──
        stats_row = QtWidgets.QHBoxLayout()
        stats_row.setSpacing(6)
        stats_row.addWidget(Chip("Bài tập", f"{self.data['bt']} / 29"))
        stats_row.addWidget(Chip("Tuần", self.data["tuan"]))
        stats_row.addWidget(Chip("Điểm", self.data["diem"]))
        stats_row.addStretch()

        root.addLayout(header)
        root.addWidget(lbl_name)
        root.addWidget(divider)
        root.addLayout(stats_row)
        root.addStretch()

    def mousePressEvent(self, event):
        self.clicked.emit(self.data)
        super().mousePressEvent(event)


# ─────────────────────────────────────────────
#  HEADER BAR
# ─────────────────────────────────────────────
class HeaderBar(QtWidgets.QWidget):
    logout_clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(64)
        self.setStyleSheet(f"""
            HeaderBar {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {PRIMARY_DARK},
                    stop:1 {PRIMARY_LIGHT}
                );
            }}
        """)
        self._build()

    def _build(self):
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(28, 0, 28, 0)
        layout.setSpacing(0)

        # ── Brand (left) ──
        brand = QtWidgets.QHBoxLayout()
        brand.setSpacing(10)

        lbl_logo = QtWidgets.QLabel("🎓")
        lbl_logo.setFont(QtGui.QFont("Segoe UI", 22))
        lbl_logo.setStyleSheet("background: transparent; color: white;")

        lbl_title = QtWidgets.QLabel("Student Manager")
        lbl_title.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
        lbl_title.setStyleSheet("background: transparent; color: white;")

        brand.addWidget(lbl_logo)
        brand.addWidget(lbl_title)

        # ── Logout button (right) ──
        btn_logout = QtWidgets.QPushButton("⎋  Đăng xuất")
        btn_logout.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
        btn_logout.setFixedSize(130, 36)
        btn_logout.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn_logout.setStyleSheet(f"""
            QPushButton {{
                background: rgba(255,255,255,0.18);
                color: white;
                border: 1.5px solid rgba(255,255,255,0.45);
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background: rgba(255,255,255,0.32);
            }}
            QPushButton:pressed {{
                background: rgba(255,255,255,0.10);
            }}
        """)
        btn_logout.clicked.connect(self.logout_clicked.emit)

        layout.addLayout(brand)
        layout.addStretch()
        layout.addWidget(btn_logout)

class Studenthomepage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Manager")
        self.resize(1200, 720)
        self.setMinimumSize(900, 600)
        self._apply_style()
        self._build()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QMainWindow, QWidget#central {{
                background: {PAGE_BG};
            }}
            QScrollArea {{
                background: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                background: {BORDER_SOFT};
                width: 7px;
                border-radius: 4px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {PRIMARY_LIGHT};
                border-radius: 4px;
                min-height: 30px;
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0;
            }}
        """)

    def _build(self):
        # 1. Thiết lập layout chính cho trang chủ
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 2. Thêm Header (Thanh tiêu đề màu đỏ)
        self.header = HeaderBar()
        self.header.logout_clicked.connect(self._on_logout)
        main_layout.addWidget(self.header)

        # 3. Khu vực cuộn (Scroll Area) cho nội dung bên dưới
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")
        main_layout.addWidget(scroll)

        # 4. Widget chứa nội dung thực tế
        body = QtWidgets.QWidget()
        body.setObjectName("home_body")
        body.setStyleSheet(f"#home_body {{ background: {PAGE_BG}; }}")
        scroll.setWidget(body)

        body_layout = QtWidgets.QVBoxLayout(body)
        body_layout.setContentsMargins(32, 28, 32, 32)
        body_layout.setSpacing(28)
        
        body_layout.addLayout(self._build_welcome())
        body_layout.addLayout(self._build_stats())
        body_layout.addWidget(self._section_label("Lớp tín chỉ  📚"))
        body_layout.addLayout(self._build_courses())
        body_layout.addStretch()

    def _build_welcome(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(4)

        lbl_greeting = QtWidgets.QLabel("Chào mừng trở lại 👋")
        lbl_greeting.setFont(QtGui.QFont("Segoe UI", 26, QtGui.QFont.Bold))
        lbl_greeting.setStyleSheet(f"color: {TEXT_DARK}; background: transparent;")

        lbl_sub = QtWidgets.QLabel("Quản lí thông tin sinh viên một cách hiệu quả")
        lbl_sub.setFont(QtGui.QFont("Segoe UI", 12))
        lbl_sub.setStyleSheet(f"color: {TEXT_MUTED}; background: transparent;")

        layout.addWidget(lbl_greeting)
        layout.addWidget(lbl_sub)
        return layout

    # ── Stat cards ───────────────────────────
    def _build_stats(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(16)
        for d in STAT_DATA:
            card = StatCard(d)
            card.clicked.connect(self._on_stat_click)
            layout.addWidget(card)
        return layout

    # ── Course cards ─────────────────────────
    def _build_courses(self):
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(16)
        for i, course in enumerate(COURSE_DATA):
            card = CourseCard(course, icon=COURSE_ICONS[i % len(COURSE_ICONS)])
            card.clicked.connect(self._on_course_click)
            row, col = divmod(i, 3)
            grid.addWidget(card, row, col)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)
        return grid

    # ── Section label ─────────────────────────
    def _section_label(self, text: str) -> QtWidgets.QLabel:
        lbl = QtWidgets.QLabel(text)
        lbl.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
        lbl.setStyleSheet(f"color: {TEXT_DARK}; background: transparent;")
        return lbl

    # ── Slots ─────────────────────────────────
    def _on_logout(self):
        print("[ACTION] Đăng xuất")

    def _on_stat_click(self, data):
        print(f"[STAT] {data['title']} → {data['value']}")

    def _on_course_click(self, data):
        print(f"[COURSE] {data['code']} – {data['name']}")


# ─────────────────────────────────────────────
#  ENTRY
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QtGui.QFont("Segoe UI", 10))

    window = Studenthomepage()
    window.show()
    sys.exit(app.exec_())