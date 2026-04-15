import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class C:
    BG          = "#F5F5F7"
    CARD        = "#FFFFFF"
    BORDER      = "#E4E4E7"
    TXT         = "#18181B"
    TXT2        = "#71717A"
    TXT3        = "#A1A1AA"
    RED         = "#EF4444"
    RED_BG      = "#FEE2E2"
    GREEN       = "#22C55E"
    GREEN_BG    = "#DCFCE7"
    GREEN_BADGE = "#16A34A"
    BLUE        = "#3B82F6"
    BLUE_BG     = "#DBEAFE"
    GRAY_BADGE  = "#F4F4F5"
    GRAY_TXT    = "#52525B"
    ROW_ALT     = "#FAFAFA"
    HDR_BG      = "#F4F4F5"
    CODE        = "#EF4444"

def add_shadow(w, blur=18, y=3, color="#00000012"):
    sh = QtWidgets.QGraphicsDropShadowEffect()
    sh.setBlurRadius(blur)
    sh.setOffset(0, y)
    sh.setColor(QtGui.QColor(color))
    w.setGraphicsEffect(sh)

class Avatar(QtWidgets.QWidget):
    def __init__(self, initials="ND", size=36, parent=None):
        super().__init__(parent)
        self.initials = initials
        self.setFixedSize(size, size)

    def paintEvent(self, _):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.setBrush(QtGui.QBrush(QtGui.QColor(C.RED)))
        p.setPen(QtCore.Qt.NoPen)
        p.drawEllipse(0, 0, self.width(), self.height())
        p.setPen(QtGui.QPen(QtGui.QColor("white")))
        f = QtGui.QFont("Segoe UI", int(self.width() * 0.28), QtGui.QFont.Bold)
        p.setFont(f)
        p.drawText(self.rect(), QtCore.Qt.AlignCenter, self.initials)

class IconSquare(QtWidgets.QWidget):
    def __init__(self, icon, bg, fg, size=48, r=12, parent=None):
        super().__init__(parent)
        self.icon, self.bg, self.fg, self.r = icon, QtGui.QColor(bg), QtGui.QColor(fg), r
        self.setFixedSize(size, size)

    def paintEvent(self, _):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        path = QtGui.QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.r, self.r)
        p.fillPath(path, QtGui.QBrush(self.bg))
        p.setPen(QtGui.QPen(self.fg))
        f = QtGui.QFont("Segoe UI Emoji", int(self.width() * 0.40))
        p.setFont(f)
        p.drawText(self.rect(), QtCore.Qt.AlignCenter, self.icon)

class StatCard(QtWidgets.QFrame):
    def __init__(self, title, value, icon, icon_bg, icon_fg, parent=None):
        super().__init__(parent)
        self.setObjectName("StatCard")
        self.setStyleSheet(f"""
            QFrame#StatCard {{
                background: {C.CARD};
                border-radius: 14px;
                border: 1px solid {C.BORDER};
            }}
        """)
        self.setFixedHeight(110)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Fixed)
        add_shadow(self)

        lay = QtWidgets.QHBoxLayout(self)
        lay.setContentsMargins(20, 18, 20, 18)
        lay.setSpacing(16)

        lay.addWidget(IconSquare(icon, icon_bg, icon_fg))

        vl = QtWidgets.QVBoxLayout()
        vl.setSpacing(3)

        t = QtWidgets.QLabel(title)
        t.setFont(QtGui.QFont("Segoe UI", 10))
        t.setStyleSheet(f"color:{C.TXT2};")

        v = QtWidgets.QLabel(value)
        v.setFont(QtGui.QFont("Segoe UI", 28, QtGui.QFont.Bold))
        v.setStyleSheet(f"color:{C.TXT};")

        vl.addWidget(t)
        vl.addWidget(v)
        lay.addLayout(vl)
        lay.addStretch()

class Badge(QtWidgets.QLabel):
    _MAP = {
        "Đang học":    (C.GREEN_BG, C.GREEN_BADGE),
        "Đã kết thúc": (C.GRAY_BADGE,  C.GRAY_TXT),
    }

    def __init__(self, status, parent=None):
        super().__init__(status, parent)
        bg, fg = self._MAP.get(status, (C.GRAY_BADGE, C.GRAY_TXT))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFont(QtGui.QFont("Segoe UI", 9, QtGui.QFont.Bold))
        self.setFixedHeight(24)
        self.setStyleSheet(f"""
            QLabel {{
                background:{bg}; color:{fg};
                border-radius:10px; padding:2px 10px;
            }}
        """)

class CourseTable(QtWidgets.QFrame):
    COLS = ["Mã HP", "Tên học phần", "Tín chỉ",
            "Lớp HP", "Giảng viên", "Lịch học",
            "Phòng", "Sĩ số", "Trạng thái"]

    DATA = [
        ("INT1234", "Lap trinh huong doi tuong", "3",
         "INT1234.1", "TS. Nguyen Van A",
         "Thu 2 (Tiet 1-3)", "A1-201", "45/50", "Đang học"),
        ("INT2345", "Co so du lieu", "3",
         "INT2345.2", "PGS.TS. Tran Thi B",
         "Thu 3 (Tiet 4-6)", "A2-305", "48/50", "Đang học"),
        ("INT3456", "Mang may tinh", "3",
         "INT3456.1", "TS. Le Van C",
         "Thu 4 (Tiet 7-9)", "B1-102", "42/50", "Đang học"),
        ("INT4567", "Phat trien ung dung web", "3",
         "INT4567.3", "ThS. Pham Thi D",
         "Thu 5 (Tiet 1-3)", "C2-401", "50/50", "Đang học"),
        ("INT5678", "Tri tue nhan tao", "3",
         "INT5678.1", "PGS.TS. Hoang Van E",
         "Thu 6 (Tiet 4-6)", "A3-201", "40/50", "Đang học"),
        ("INT6789", "Ky thuat phan mem", "3",
         "INT6789.2", "TS. Vu Thi F",
         "Thu 7 (Tiet 1-3)", "B2-303", "38/50", "Đã kết thúc"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CT")
        self.setStyleSheet(f"""
            QFrame#CT {{
                background:{C.CARD};
                border-radius:14px;
                border:1px solid {C.BORDER};
            }}
        """)
        add_shadow(self, blur=22, y=5)

        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(24, 20, 24, 20)
        outer.setSpacing(14)

        hdr = QtWidgets.QHBoxLayout()
        hdr.setSpacing(10)

        title = QtWidgets.QLabel("Danh sach lop tin chi")
        title.setFont(QtGui.QFont("Segoe UI", 13, QtGui.QFont.Bold))
        title.setStyleSheet(f"color:{C.TXT};")
        hdr.addWidget(title)
        hdr.addStretch()

        srch = QtWidgets.QLineEdit()
        srch.setPlaceholderText("🔍  Tim kiem lop...")
        srch.setFixedSize(210, 34)
        srch.setFont(QtGui.QFont("Segoe UI", 10))
        srch.setStyleSheet(f"""
            QLineEdit {{
                background:{C.BG};
                border:1px solid {C.BORDER};
                border-radius:8px;
                padding:3px 12px;
                color:{C.TXT};
            }}
            QLineEdit:focus {{
                border:1.5px solid {C.BLUE};
                background:white;
            }}
        """)
        srch.textChanged.connect(self._filter)
        hdr.addWidget(srch)

        outer.addLayout(hdr)

        self.tbl = QtWidgets.QTableWidget()
        self.tbl.setColumnCount(len(self.COLS))
        self.tbl.setHorizontalHeaderLabels(self.COLS)
        self.tbl.verticalHeader().setVisible(False)
        self.tbl.setShowGrid(False)
        self.tbl.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbl.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbl.setAlternatingRowColors(False)
        self.tbl.setFocusPolicy(QtCore.Qt.NoFocus)

        hh = self.tbl.horizontalHeader()
        hh.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        hh.setStretchLastSection(True)

        col_w = [90, 210, 62, 105, 175, 165, 90, 70, 115]
        for i, w in enumerate(col_w):
            self.tbl.setColumnWidth(i, w)

        self.tbl.setStyleSheet(f"""
            QTableWidget {{
                background:{C.CARD};
                border:none;
                outline:none;
                font-family:'Segoe UI';
                font-size:13px;
                color:{C.TXT};
            }}
            QTableWidget::item {{
                padding:0 8px;
                border-bottom:1px solid {C.BORDER};
            }}
            QTableWidget::item:selected {{
                background:#EFF6FF;
                color:{C.TXT};
            }}
            QTableWidget::item:hover {{
                background:#F9FAFB;
            }}
            QHeaderView::section {{
                background:{C.HDR_BG};
                color:{C.TXT2};
                font-weight:bold;
                font-size:12px;
                font-family:'Segoe UI';
                padding:9px 8px;
                border:none;
                border-bottom:2px solid {C.BORDER};
            }}
            QScrollBar:horizontal {{
                height:6px; background:{C.BG}; border-radius:3px;
            }}
            QScrollBar::handle:horizontal {{
                background:{C.TXT3}; border-radius:3px;
            }}
            QScrollBar:vertical {{
                width:6px; background:{C.BG}; border-radius:3px;
            }}
            QScrollBar::handle:vertical {{
                background:{C.TXT3}; border-radius:3px;
            }}
        """)

        self._all = list(self.DATA)
        self._fill(self.DATA)
        outer.addWidget(self.tbl)

    def _make_item(self, text, bold=False, color=None, align=None):
        it = QtWidgets.QTableWidgetItem(text)
        f = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold if bold else QtGui.QFont.Normal)
        it.setFont(f)
        if color:
            it.setForeground(QtGui.QColor(color))
        if align:
            it.setTextAlignment(align)
        return it

    def _fill(self, rows):
        self.tbl.setRowCount(len(rows))
        for r, row in enumerate(rows):
            self.tbl.setRowHeight(r, 50)
            self.tbl.setItem(r, 0, self._make_item(row[0], bold=True, color=C.CODE))
            self.tbl.setItem(r, 1, self._make_item(row[1]))
            self.tbl.setItem(r, 2, self._make_item(row[2], align=QtCore.Qt.AlignCenter))
            self.tbl.setItem(r, 3, self._make_item(row[3], color=C.TXT2))
            self.tbl.setItem(r, 4, self._make_item("👤 " + row[4]))
            self.tbl.setItem(r, 5, self._make_item("🕐 " + row[5]))
            self.tbl.setItem(r, 6, self._make_item("📍 " + row[6]))
            self.tbl.setItem(r, 7, self._make_item(row[7], align=QtCore.Qt.AlignCenter))
            badge = Badge(row[8])
            cell = QtWidgets.QWidget()
            cl = QtWidgets.QHBoxLayout(cell)
            cl.setContentsMargins(6, 0, 6, 0)
            cl.addWidget(badge)
            cl.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            self.tbl.setCellWidget(r, 9 - 1, None)
            self.tbl.setCellWidget(r, 8, cell)

    def _filter(self, text):
        lo = text.lower()
        if not lo:
            self._fill(self._all)
            return
        self._fill([row for row in self._all
                    if any(lo in col.lower() for col in row)])


class NavBar(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Nav")
        self.setFixedHeight(64)
        self.setStyleSheet(f"""
            QFrame#Nav {{
                background:{C.CARD};
                border-bottom:1px solid {C.BORDER};
            }}
        """)

        lay = QtWidgets.QHBoxLayout(self)
        lay.setContentsMargins(28, 0, 28, 0)
        lay.setSpacing(12)

        lbl = QtWidgets.QLabel("Lop tin chi")
        lbl.setFont(QtGui.QFont("Segoe UI", 17, QtGui.QFont.Bold))
        lbl.setStyleSheet(f"color:{C.TXT};")
        lay.addWidget(lbl)

        lay.addStretch()

        av = Avatar("ND", size=36)
        lay.addWidget(av)

        vl = QtWidgets.QVBoxLayout()
        vl.setSpacing(1)

        nm = QtWidgets.QLabel("Nguyen Dinh Nghia")
        nm.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Bold))
        nm.setStyleSheet(f"color:{C.TXT};")

        em = QtWidgets.QLabel("nghia@ptit.edu.vn")
        em.setFont(QtGui.QFont("Segoe UI", 9))
        em.setStyleSheet(f"color:{C.TXT2};")

        vl.addWidget(nm)
        vl.addWidget(em)
        lay.addLayout(vl)

# ĐỔI THÀNH QWidget ĐỂ NHÚNG VÀO QStackedWidget
class CreditClassWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CreditClassPage")
        self.setStyleSheet(f"background:{C.BG};")

        root_lay = QtWidgets.QVBoxLayout(self)
        root_lay.setContentsMargins(0, 0, 0, 0)
        root_lay.setSpacing(0)

        # Nav bar
        root_lay.addWidget(NavBar())

        # Scroll area
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setStyleSheet(f"""
            QScrollArea {{ background:{C.BG}; border:none; }}
            QScrollBar:vertical {{ width:6px; background:{C.BG}; border-radius:3px; }}
            QScrollBar::handle:vertical {{ background:#C4C4C4; border-radius:3px; }}
        """)

        body = QtWidgets.QWidget()
        body.setStyleSheet(f"background:{C.BG};")
        body_lay = QtWidgets.QVBoxLayout(body)
        body_lay.setContentsMargins(28, 22, 28, 28)
        body_lay.setSpacing(18)

        stats_row = QtWidgets.QHBoxLayout()
        stats_row.setSpacing(14)
        cards = [
            ("Tong so lop",  "6",  "📚", C.RED_BG,   C.RED),
            ("Dang hoc",     "5",  "🕐", C.GREEN_BG,  C.GREEN),
            ("Tong tin chi", "18", "📖", C.BLUE_BG,   C.BLUE),
        ]
        for t, v, ic, bg, fg in cards:
            stats_row.addWidget(StatCard(t, v, ic, bg, fg))
        body_lay.addLayout(stats_row)

        body_lay.addWidget(CourseTable())
        body_lay.addStretch()

        scroll.setWidget(body)
        root_lay.addWidget(scroll)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = CreditClassWidget()
    w.resize(1130, 780)
    w.show()
    sys.exit(app.exec_())