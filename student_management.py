"""
PTIT Student Management System
================================
PyQt5 + Firebase Firestore

Cài đặt thư viện:
    pip install PyQt5 firebase-admin pandas pyqtgraph

Cấu trúc Firestore:
    Collection: students
        Document fields:
            - mssv      : str   (mã số sinh viên)
            - ho_ten    : str
            - lop       : str
            - nganh     : str
            - email     : str
            - sdt       : str
            - gpa       : float
            - trang_thai: str   ("Đang học" | "Bảo lưu" | "Tốt nghiệp")
"""

import sys
import re
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QColor, QFont, QPalette, QIcon, QPixmap, QPainter
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QScrollArea, QMessageBox, QDialog,
    QFormLayout, QComboBox, QSizePolicy, QStackedWidget, QGridLayout,
    QAbstractItemView, QSplitter, QGraphicsDropShadowEffect
)

import firebase_admin
from firebase_admin import credentials, firestore

# ─────────────────────────────────────────────────────────────────────────────
#  Firebase init – đổi đường dẫn key.json cho đúng máy bạn
# ─────────────────────────────────────────────────────────────────────────────
KEY_PATH = r"D:\VS code\codewep\btlpython\key.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()
COLLECTION = "students"

# ─────────────────────────────────────────────────────────────────────────────
#  Palette màu PTIT
# ─────────────────────────────────────────────────────────────────────────────
C = {
    "red":          "#D32F2F",
    "red_dark":     "#B71C1C",
    "red_light":    "#FFEBEE",
    "red_mid":      "#EF9A9A",
    "white":        "#FFFFFF",
    "bg":           "#F5F6FA",
    "surface":      "#FFFFFF",
    "border":       "#EFEFEF",
    "text":         "#1A1A2E",
    "text_sec":     "#666666",
    "text_muted":   "#AAAAAA",
    "blue":         "#1976D2",
    "blue_light":   "#E3F2FD",
    "green":        "#388E3C",
    "green_light":  "#E8F5E9",
    "orange":       "#F57C00",
    "orange_light": "#FFF3E0",
    "purple":       "#7B1FA2",
    "purple_light": "#F3E5F5",
    "row_alt":      "#FAFAFA",
    "row_hover":    "#FFF5F5",
    "row_sel":      "#FFEBEE",
}

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {C['bg']};
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    color: {C['text']};
}}

/* ── Sidebar ────────────────────────────────── */
#sidebar {{
    background-color: {C['white']};
    border-right: 1px solid {C['border']};
}}
#logo_frame {{
    border-bottom: 1px solid {C['border']};
    padding: 4px 0;
}}
#logo_box {{
    background-color: {C['red']};
    border-radius: 10px;
    color: white;
    font-weight: bold;
    font-size: 12px;
}}
#logo_title {{
    color: {C['red']};
    font-weight: bold;
    font-size: 13px;
}}
#logo_sub {{
    color: {C['text_muted']};
    font-size: 10px;
}}
#nav_label {{
    color: #CCCCCC;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1px;
    padding: 8px 8px 2px 8px;
    text-transform: uppercase;
}}
QPushButton#nav_btn {{
    background: transparent;
    border: none;
    border-radius: 8px;
    color: {C['text_sec']};
    font-size: 13px;
    padding: 9px 10px;
    text-align: left;
}}
QPushButton#nav_btn:hover {{
    background-color: {C['red_light']};
    color: {C['red']};
}}
QPushButton#nav_btn[active=true] {{
    background-color: {C['red']};
    color: white;
    font-weight: bold;
}}
QPushButton#logout_btn {{
    background: transparent;
    border: none;
    border-radius: 8px;
    color: #E53935;
    font-size: 13px;
    padding: 9px 10px;
    text-align: left;
}}
QPushButton#logout_btn:hover {{
    background-color: {C['red_light']};
}}

/* ── Header ─────────────────────────────────── */
#header {{
    background-color: {C['white']};
    border-bottom: 1px solid {C['border']};
}}
#search_input {{
    border: 1px solid {C['border']};
    border-radius: 10px;
    padding: 7px 12px 7px 34px;
    background: #F9F9F9;
    font-size: 13px;
    color: {C['text']};
}}
#search_input:focus {{
    border-color: {C['red']};
    background: white;
    outline: none;
}}
#notif_btn {{
    background: #F5F5F5;
    border: none;
    border-radius: 10px;
    color: #888;
    font-size: 16px;
    padding: 4px 10px;
}}
#notif_btn:hover {{
    background: {C['red_light']};
    color: {C['red']};
}}
#user_name_lbl {{
    font-weight: bold;
    font-size: 13px;
    color: {C['text']};
}}
#user_email_lbl {{
    font-size: 11px;
    color: {C['text_muted']};
}}
#avatar_lbl {{
    background-color: {C['red']};
    border-radius: 17px;
    color: white;
    font-weight: bold;
    font-size: 12px;
}}

/* ── Stat card ───────────────────────────────── */
#stat_card {{
    background: {C['white']};
    border-radius: 14px;
    border: 1px solid {C['border']};
}}
#stat_label {{
    font-size: 11px;
    color: {C['text_muted']};
    font-weight: bold;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}
#stat_value {{
    font-size: 26px;
    font-weight: bold;
    color: {C['text']};
}}
#stat_change {{
    font-size: 12px;
    font-weight: bold;
    color: {C['green']};
}}

/* ── Section cards ────────────────────────────── */
#card {{
    background: {C['white']};
    border-radius: 14px;
    border: 1px solid {C['border']};
}}
#card_title {{
    font-size: 15px;
    font-weight: bold;
    color: {C['text']};
}}
#card_badge {{
    background: {C['red_light']};
    color: {C['red']};
    border-radius: 10px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: bold;
}}

/* ── Table ────────────────────────────────────── */
QTableWidget {{
    background: {C['white']};
    border: none;
    gridline-color: {C['border']};
    font-size: 13px;
    color: {C['text']};
    selection-background-color: {C['row_sel']};
    selection-color: {C['text']};
    outline: none;
}}
QTableWidget::item {{
    padding: 10px 12px;
    border-bottom: 1px solid {C['border']};
}}
QTableWidget::item:alternate {{
    background-color: {C['row_alt']};
}}
QTableWidget::item:hover {{
    background-color: {C['row_hover']};
}}
QTableWidget::item:selected {{
    background-color: {C['row_sel']};
    color: {C['text']};
}}
QHeaderView::section {{
    background-color: {C['white']};
    color: {C['text_muted']};
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    padding: 10px 12px;
    border: none;
    border-bottom: 2px solid {C['border']};
}}

/* ── Buttons ─────────────────────────────────── */
QPushButton#primary_btn {{
    background-color: {C['red']};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: bold;
}}
QPushButton#primary_btn:hover {{
    background-color: {C['red_dark']};
}}
QPushButton#danger_btn {{
    background-color: white;
    color: #E53935;
    border: 1px solid #E53935;
    border-radius: 8px;
    padding: 7px 16px;
    font-size: 13px;
}}
QPushButton#danger_btn:hover {{
    background-color: {C['red_light']};
}}
QPushButton#icon_btn {{
    background: transparent;
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 13px;
    color: {C['text_sec']};
}}
QPushButton#icon_btn:hover {{
    border-color: {C['red']};
    color: {C['red']};
    background: {C['red_light']};
}}

/* ── Dialog ─────────────────────────────────── */
QDialog {{
    background: {C['white']};
    border-radius: 16px;
}}
QLineEdit, QComboBox {{
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    background: #FAFAFA;
    color: {C['text']};
}}
QLineEdit:focus, QComboBox:focus {{
    border-color: {C['red']};
    background: white;
}}
QComboBox::drop-down {{
    border: none;
    padding-right: 10px;
}}
QLabel#form_label {{
    color: {C['text_sec']};
    font-size: 12px;
    font-weight: bold;
}}

/* ── Scrollbar ───────────────────────────────── */
QScrollBar:vertical {{
    background: transparent;
    width: 6px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: #DDDDDD;
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {C['red_mid']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{ height: 6px; background: transparent; }}
QScrollBar::handle:horizontal {{
    background: #DDDDDD; border-radius: 3px;
}}
"""

# ─────────────────────────────────────────────────────────────────────────────
#  Worker thread – đọc/ghi Firebase mà không block UI
# ─────────────────────────────────────────────────────────────────────────────
class FirebaseWorker(QThread):
    data_loaded   = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    done          = pyqtSignal(str)

    def __init__(self, task, payload=None):
        super().__init__()
        self.task    = task       # "load" | "add" | "update" | "delete"
        self.payload = payload    # dict hoặc str (doc_id)

    def run(self):
        try:
            if self.task == "load":
                docs = db.collection(COLLECTION).stream()
                rows = []
                for d in docs:
                    r = d.to_dict()
                    r["_id"] = d.id
                    rows.append(r)
                self.data_loaded.emit(rows)

            elif self.task == "add":
                db.collection(COLLECTION).add(self.payload)
                self.done.emit("Thêm sinh viên thành công!")

            elif self.task == "update":
                doc_id = self.payload.pop("_id")
                db.collection(COLLECTION).document(doc_id).update(self.payload)
                self.done.emit("Cập nhật thành công!")

            elif self.task == "delete":
                db.collection(COLLECTION).document(self.payload).delete()
                self.done.emit("Đã xóa sinh viên!")

        except Exception as e:
            self.error_occurred.emit(str(e))


# ─────────────────────────────────────────────────────────────────────────────
#  Dialog Thêm / Sửa sinh viên
# ─────────────────────────────────────────────────────────────────────────────
class StudentDialog(QDialog):
    def __init__(self, parent=None, data: dict = None):
        super().__init__(parent)
        self.setWindowTitle("Thêm sinh viên" if data is None else "Chỉnh sửa sinh viên")
        self.setFixedWidth(480)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._data = data or {}
        self._build()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet(f"""
            QFrame#card {{
                background: white;
                border-radius: 16px;
                border: 1px solid {C['border']};
            }}
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 4)
        card.setGraphicsEffect(shadow)
        outer.addWidget(card)

        lay = QVBoxLayout(card)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(16)

        # Title
        title = QLabel("➕  Thêm sinh viên" if not self._data else "✏️  Chỉnh sửa sinh viên")
        title.setStyleSheet(f"font-size:16px; font-weight:bold; color:{C['text']};")
        lay.addWidget(title)

        line = QFrame(); line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color:{C['border']};")
        lay.addWidget(line)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setSpacing(12)

        def lbl(text):
            l = QLabel(text)
            l.setObjectName("form_label")
            return l

        self.f_mssv   = QLineEdit(self._data.get("mssv", ""))
        self.f_ten    = QLineEdit(self._data.get("ho_ten", ""))
        self.f_lop    = QLineEdit(self._data.get("lop", ""))
        self.f_nganh  = QLineEdit(self._data.get("nganh", ""))
        self.f_email  = QLineEdit(self._data.get("email", ""))
        self.f_sdt    = QLineEdit(self._data.get("sdt", ""))
        self.f_gpa    = QLineEdit(str(self._data.get("gpa", "")))

        self.f_status = QComboBox()
        self.f_status.addItems(["Đang học", "Bảo lưu", "Tốt nghiệp"])
        idx = self.f_status.findText(self._data.get("trang_thai", "Đang học"))
        if idx >= 0:
            self.f_status.setCurrentIndex(idx)

        for lbl_text, widget in [
            ("MSSV *",       self.f_mssv),
            ("Họ tên *",     self.f_ten),
            ("Lớp",          self.f_lop),
            ("Ngành",        self.f_nganh),
            ("Email",        self.f_email),
            ("SĐT",          self.f_sdt),
            ("GPA",          self.f_gpa),
            ("Trạng thái",   self.f_status),
        ]:
            form.addRow(lbl(lbl_text), widget)

        lay.addLayout(form)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        cancel = QPushButton("Hủy")
        cancel.setObjectName("icon_btn")
        cancel.clicked.connect(self.reject)

        save = QPushButton("💾  Lưu")
        save.setObjectName("primary_btn")
        save.clicked.connect(self._save)

        btn_row.addStretch()
        btn_row.addWidget(cancel)
        btn_row.addWidget(save)
        lay.addLayout(btn_row)

    def _save(self):
        mssv   = self.f_mssv.text().strip()
        ho_ten = self.f_ten.text().strip()
        if not mssv or not ho_ten:
            QMessageBox.warning(self, "Thiếu thông tin", "MSSV và Họ tên không được để trống.")
            return
        try:
            gpa = float(self.f_gpa.text()) if self.f_gpa.text() else 0.0
            if not (0 <= gpa <= 4):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "GPA không hợp lệ", "GPA phải là số từ 0 đến 4.")
            return

        self.result_data = {
            "mssv":       mssv,
            "ho_ten":     ho_ten,
            "lop":        self.f_lop.text().strip(),
            "nganh":      self.f_nganh.text().strip(),
            "email":      self.f_email.text().strip(),
            "sdt":        self.f_sdt.text().strip(),
            "gpa":        round(gpa, 2),
            "trang_thai": self.f_status.currentText(),
        }
        if "_id" in self._data:
            self.result_data["_id"] = self._data["_id"]
        self.accept()


# ─────────────────────────────────────────────────────────────────────────────
#  Stat Card widget
# ─────────────────────────────────────────────────────────────────────────────
class StatCard(QFrame):
    def __init__(self, title, value, change, icon, accent):
        super().__init__()
        self.setObjectName("stat_card")
        self.setFixedHeight(110)

        # accent bar
        self._accent = accent
        self.setStyleSheet(f"""
            QFrame#stat_card {{
                background: white;
                border-radius: 14px;
                border: 1px solid {C['border']};
                border-left: 4px solid {accent};
            }}
        """)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 14)
        lay.setSpacing(4)

        top = QHBoxLayout()

        left = QVBoxLayout()
        lbl_title = QLabel(title.upper())
        lbl_title.setObjectName("stat_label")
        lbl_val = QLabel(value)
        lbl_val.setObjectName("stat_value")
        self.lbl_val = lbl_val

        left.addWidget(lbl_title)
        left.addWidget(lbl_val)

        icon_lbl = QLabel(icon)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setFixedSize(40, 40)
        icon_lbl.setStyleSheet(f"""
            background: {accent}22;
            border-radius: 10px;
            font-size: 18px;
        """)

        top.addLayout(left)
        top.addStretch()
        top.addWidget(icon_lbl)

        chg = QLabel(f"↑ {change}")
        chg.setObjectName("stat_change")

        lay.addLayout(top)
        lay.addWidget(chg)

    def update_value(self, val):
        self.lbl_val.setText(str(val))


# ─────────────────────────────────────────────────────────────────────────────
#  Toast notification (nhỏ, hiện góc dưới phải)
# ─────────────────────────────────────────────────────────────────────────────
class Toast(QLabel):
    def __init__(self, parent, message, success=True):
        super().__init__(message, parent)
        color = C['green'] if success else C['red']
        self.setStyleSheet(f"""
            background: {color};
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: bold;
        """)
        self.adjustSize()
        pw, ph = parent.width(), parent.height()
        self.move(pw - self.width() - 24, ph - self.height() - 24)
        self.raise_()
        self.show()
        QTimer.singleShot(2800, self.deleteLater)


# ─────────────────────────────────────────────────────────────────────────────
#  Main Window
# ─────────────────────────────────────────────────────────────────────────────
class StudentWindow(QMainWindow):
    COLS = ["MSSV", "Họ tên", "Lớp", "Ngành", "Email", "SĐT", "GPA", "Trạng thái"]
    KEYS = ["mssv", "ho_ten", "lop", "nganh", "email", "sdt", "gpa", "trang_thai"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PTIT – Quản lý Sinh viên")
        self.resize(1280, 740)
        self._all_rows: list = []
        self._workers: list  = []

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._build_sidebar(root)
        self._build_main(root)
        self.setStyleSheet(STYLESHEET)
        self._load_data()

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self, parent_layout):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(230)
        lay = QVBoxLayout(sidebar)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Logo
        logo_frame = QFrame()
        logo_frame.setObjectName("logo_frame")
        logo_frame.setFixedHeight(64)
        lf_lay = QHBoxLayout(logo_frame)
        lf_lay.setContentsMargins(16, 10, 16, 10)
        lf_lay.setSpacing(10)

        box = QLabel("PTIT")
        box.setObjectName("logo_box")
        box.setFixedSize(38, 38)
        box.setAlignment(Qt.AlignCenter)

        txt = QVBoxLayout()
        t1 = QLabel("PTIT Portal"); t1.setObjectName("logo_title")
        t2 = QLabel("Học viện CNBCVT"); t2.setObjectName("logo_sub")
        txt.addWidget(t1); txt.addWidget(t2)

        lf_lay.addWidget(box)
        lf_lay.addLayout(txt)
        lay.addWidget(logo_frame)

        # Nav
        nav_scroll = QScrollArea()
        nav_scroll.setWidgetResizable(True)
        nav_scroll.setFrameShape(QFrame.NoFrame)
        nav_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        nav_w = QWidget()
        nav_lay = QVBoxLayout(nav_w)
        nav_lay.setContentsMargins(12, 10, 12, 10)
        nav_lay.setSpacing(2)

        self._nav_btns = []

        def section(label):
            l = QLabel(label)
            l.setObjectName("nav_label")
            nav_lay.addWidget(l)

        def nav(icon, text, active=False):
            btn = QPushButton(f"  {icon}   {text}")
            btn.setObjectName("nav_btn")
            btn.setProperty("active", active)
            btn.setFixedHeight(38)
            btn.setCursor(Qt.PointingHandCursor)
            self._nav_btns.append(btn)
            nav_lay.addWidget(btn)
            return btn

        section("TỔNG QUAN")
        btn_home = nav("🏠", "Trang chủ", active=True)
        btn_home.clicked.connect(lambda: self._set_page(0, btn_home))

        section("QUẢN LÝ")
        btn_sv   = nav("👥", "Danh sách sinh viên")
        btn_sv.clicked.connect(lambda: self._set_page(1, btn_sv))
        nav("📚", "Lớp tín chỉ")
        nav("📅", "Lớp hành chính")

        section("HỆ THỐNG")
        nav("⚙️", "Cài đặt")

        nav_lay.addStretch()
        nav_scroll.setWidget(nav_w)
        lay.addWidget(nav_scroll)

        # Logout
        bottom = QFrame()
        bottom.setStyleSheet(f"border-top: 1px solid {C['border']};")
        bl = QVBoxLayout(bottom)
        bl.setContentsMargins(12, 8, 12, 12)
        logout = QPushButton("  🚪   Đăng xuất")
        logout.setObjectName("logout_btn")
        logout.setFixedHeight(38)
        logout.setCursor(Qt.PointingHandCursor)
        logout.clicked.connect(lambda: QApplication.quit())
        bl.addWidget(logout)
        lay.addWidget(bottom)

        parent_layout.addWidget(sidebar)

    def _set_page(self, idx, active_btn):
        for b in self._nav_btns:
            b.setProperty("active", False)
            b.setStyle(b.style())
        active_btn.setProperty("active", True)
        active_btn.setStyle(active_btn.style())
        self._stack.setCurrentIndex(idx)

    # ── Main area ─────────────────────────────────────────────────────────────
    def _build_main(self, parent_layout):
        main_w = QWidget()
        main_lay = QVBoxLayout(main_w)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(0)

        self._build_header(main_lay)

        self._stack = QStackedWidget()
        self._stack.addWidget(self._build_dashboard_page())
        self._stack.addWidget(self._build_student_page())
        main_lay.addWidget(self._stack)

        parent_layout.addWidget(main_w)

    # ── Header ────────────────────────────────────────────────────────────────
    def _build_header(self, parent):
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(60)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(24, 0, 24, 0)
        hl.setSpacing(14)

        # Search
        search_wrap = QWidget()
        search_wrap.setFixedWidth(340)
        sw_lay = QHBoxLayout(search_wrap)
        sw_lay.setContentsMargins(0, 0, 0, 0)
        search_lbl = QLabel("🔍")
        search_lbl.setStyleSheet("color: #aaa; font-size: 14px; padding-left: 6px;")
        self._search = QLineEdit()
        self._search.setObjectName("search_input")
        self._search.setPlaceholderText("Tìm kiếm sinh viên...")
        self._search.textChanged.connect(self._filter_table)
        sw_lay.addWidget(search_lbl)
        sw_lay.addWidget(self._search)

        # Notif
        notif = QPushButton("🔔")
        notif.setObjectName("notif_btn")
        notif.setFixedSize(36, 36)
        notif.setCursor(Qt.PointingHandCursor)
        notif.clicked.connect(lambda: Toast(self, "  📬  Không có thông báo mới", True))

        # User
        avatar = QLabel("AD")
        avatar.setObjectName("avatar_lbl")
        avatar.setFixedSize(34, 34)
        avatar.setAlignment(Qt.AlignCenter)

        user_info = QVBoxLayout()
        user_info.setSpacing(0)
        un = QLabel("Admin PTIT"); un.setObjectName("user_name_lbl")
        ue = QLabel("admin@ptit.edu.vn"); ue.setObjectName("user_email_lbl")
        user_info.addWidget(un)
        user_info.addWidget(ue)

        hl.addWidget(search_wrap)
        hl.addStretch()
        hl.addWidget(notif)
        hl.addWidget(avatar)
        hl.addLayout(user_info)

        parent.addWidget(header)

    # ── Dashboard page ────────────────────────────────────────────────────────
    def _build_dashboard_page(self):
        page = QWidget()
        lay  = QVBoxLayout(page)
        lay.setContentsMargins(24, 20, 24, 20)
        lay.setSpacing(16)

        # Page title
        pt = QLabel("Tổng quan hệ thống")
        pt.setStyleSheet(f"font-size:20px; font-weight:bold; color:{C['text']};")
        ps = QLabel("Năm học 2024 – 2025  ·  Học kỳ II")
        ps.setStyleSheet(f"font-size:13px; color:{C['text_muted']};")
        lay.addWidget(pt)
        lay.addWidget(ps)

        # Stat cards
        grid = QGridLayout()
        grid.setSpacing(14)
        self._card_sv     = StatCard("Tổng sinh viên", "—",    "+8.2% so với năm trước", "👥", C['red'])
        self._card_kh     = StatCard("Khóa học",        "348",  "+12.5% học kỳ này",      "📚", C['blue'])
        self._card_lop    = StatCard("Lớp học",          "196",  "+5.1% học kỳ này",       "📅", C['green'])
        self._card_pass   = StatCard("Tỷ lệ GPA ≥ 2",   "—",    "Tính từ dữ liệu thực",   "📈", C['orange'])
        grid.addWidget(self._card_sv,   0, 0)
        grid.addWidget(self._card_kh,   0, 1)
        grid.addWidget(self._card_lop,  0, 2)
        grid.addWidget(self._card_pass, 0, 3)
        lay.addLayout(grid)

        # Bottom: activity + quick table
        bottom = QHBoxLayout()
        bottom.setSpacing(14)

        # Quick table (latest 8 students)
        left_card = QFrame(); left_card.setObjectName("card")
        lc_lay = QVBoxLayout(left_card)
        lc_lay.setContentsMargins(16, 16, 16, 16)
        lc_lay.setSpacing(10)

        ch = QHBoxLayout()
        ct = QLabel("Sinh viên mới nhất"); ct.setObjectName("card_title")
        cb = QLabel("Top 8"); cb.setObjectName("card_badge")
        ch.addWidget(ct); ch.addStretch(); ch.addWidget(cb)
        lc_lay.addLayout(ch)

        self._dash_table = QTableWidget()
        self._dash_table.setColumnCount(4)
        self._dash_table.setHorizontalHeaderLabels(["MSSV", "Họ tên", "Lớp", "GPA"])
        self._dash_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._dash_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._dash_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._dash_table.verticalHeader().setVisible(False)
        self._dash_table.setAlternatingRowColors(True)
        self._dash_table.setShowGrid(False)
        lc_lay.addWidget(self._dash_table)
        bottom.addWidget(left_card, 3)

        # Activity feed
        right_card = QFrame(); right_card.setObjectName("card")
        right_card.setFixedWidth(300)
        rc_lay = QVBoxLayout(right_card)
        rc_lay.setContentsMargins(16, 16, 16, 16)
        rc_lay.setSpacing(0)

        rch = QHBoxLayout()
        rct = QLabel("Hoạt động gần đây"); rct.setObjectName("card_title")
        rch.addWidget(rct)
        rc_lay.addLayout(rch)

        activities = [
            ("🟥", "<b>Nguyễn Văn A</b> đăng ký lớp tín chỉ mới",      "5 phút trước"),
            ("🟦", "Khóa học <b>Lập trình Python</b> vừa được thêm",    "22 phút trước"),
            ("🟩", "Kết quả HK1 lớp <b>D21CQAT01</b> đã cập nhật",     "1 giờ trước"),
            ("🟧", "3 sinh viên nguy cơ <b>rớt môn</b> Giải tích",      "2 giờ trước"),
            ("🟪", "Lịch thi <b>HK2/2025</b> đã được công bố",          "Hôm qua"),
        ]
        for icon, text, time in activities:
            item_w = QWidget()
            il = QHBoxLayout(item_w)
            il.setContentsMargins(0, 10, 0, 10)
            il.setSpacing(10)
            ic = QLabel(icon); ic.setFixedSize(32, 32)
            ic.setAlignment(Qt.AlignCenter)
            body = QVBoxLayout(); body.setSpacing(2)
            tx = QLabel(text); tx.setWordWrap(True)
            tx.setStyleSheet("font-size:12px; color:#333;")
            tm = QLabel(time); tm.setStyleSheet(f"font-size:11px; color:{C['text_muted']};")
            body.addWidget(tx); body.addWidget(tm)
            il.addWidget(ic); il.addLayout(body)
            sep = QFrame(); sep.setFrameShape(QFrame.HLine)
            sep.setStyleSheet(f"color:{C['border']};")
            rc_lay.addWidget(item_w)
            rc_lay.addWidget(sep)

        rc_lay.addStretch()
        bottom.addWidget(right_card, 0)
        lay.addLayout(bottom)

        return page

    # ── Student list page ─────────────────────────────────────────────────────
    def _build_student_page(self):
        page = QWidget()
        lay  = QVBoxLayout(page)
        lay.setContentsMargins(24, 20, 24, 20)
        lay.setSpacing(14)

        # Page title
        pt = QLabel("Danh sách sinh viên")
        pt.setStyleSheet(f"font-size:20px; font-weight:bold; color:{C['text']};")
        lay.addWidget(pt)

        # Toolbar
        tb = QHBoxLayout(); tb.setSpacing(10)

        btn_add = QPushButton("➕  Thêm sinh viên")
        btn_add.setObjectName("primary_btn")
        btn_add.setCursor(Qt.PointingHandCursor)
        btn_add.clicked.connect(self._add_student)

        btn_edit = QPushButton("✏️  Sửa")
        btn_edit.setObjectName("icon_btn")
        btn_edit.setCursor(Qt.PointingHandCursor)
        btn_edit.clicked.connect(self._edit_student)

        btn_del = QPushButton("🗑  Xóa")
        btn_del.setObjectName("danger_btn")
        btn_del.setCursor(Qt.PointingHandCursor)
        btn_del.clicked.connect(self._delete_student)

        btn_refresh = QPushButton("🔄  Làm mới")
        btn_refresh.setObjectName("icon_btn")
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.clicked.connect(self._load_data)

        # Filter combo
        self._filter_status = QComboBox()
        self._filter_status.setFixedWidth(140)
        self._filter_status.addItems(["Tất cả", "Đang học", "Bảo lưu", "Tốt nghiệp"])
        self._filter_status.currentTextChanged.connect(self._filter_table)

        tb.addWidget(btn_add)
        tb.addWidget(btn_edit)
        tb.addWidget(btn_del)
        tb.addWidget(btn_refresh)
        tb.addStretch()
        tb.addWidget(QLabel("Lọc:"))
        tb.addWidget(self._filter_status)
        lay.addLayout(tb)

        # Table
        card = QFrame(); card.setObjectName("card")
        cl = QVBoxLayout(card); cl.setContentsMargins(0, 0, 0, 0)

        self._table = QTableWidget()
        self._table.setColumnCount(len(self.COLS))
        self._table.setHorizontalHeaderLabels(self.COLS)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setSelectionMode(QAbstractItemView.SingleSelection)
        self._table.verticalHeader().setVisible(False)
        self._table.setAlternatingRowColors(True)
        self._table.setShowGrid(False)
        self._table.setSortingEnabled(True)
        self._table.doubleClicked.connect(self._edit_student)

        # Column widths
        widths = [100, 180, 110, 150, 200, 110, 65, 110]
        for i, w in enumerate(widths):
            self._table.setColumnWidth(i, w)

        cl.addWidget(self._table)
        lay.addWidget(card)

        # Status bar
        self._status_lbl = QLabel("Đang tải dữ liệu...")
        self._status_lbl.setStyleSheet(f"color:{C['text_muted']}; font-size:12px;")
        lay.addWidget(self._status_lbl)

        return page

    # ── Data operations ───────────────────────────────────────────────────────
    def _load_data(self):
        self._status_lbl.setText("⏳ Đang tải từ Firebase...")
        w = FirebaseWorker("load")
        w.data_loaded.connect(self._on_data_loaded)
        w.error_occurred.connect(self._on_error)
        self._workers.append(w)
        w.start()

    def _on_data_loaded(self, rows: list):
        self._all_rows = rows
        self._render_table(rows)
        self._update_stats(rows)
        self._update_dash_table(rows)
        self._status_lbl.setText(f"✅  Tổng: {len(rows)} sinh viên")

    def _render_table(self, rows: list):
        self._table.setRowCount(0)
        for r in rows:
            row_idx = self._table.rowCount()
            self._table.insertRow(row_idx)
            for col, key in enumerate(self.KEYS):
                val = str(r.get(key, ""))
                item = QTableWidgetItem(val)
                item.setData(Qt.UserRole, r.get("_id", ""))
                # Color status badge
                if key == "trang_thai":
                    color_map = {
                        "Đang học":   (C['green'],  C['green_light']),
                        "Bảo lưu":    (C['orange'], C['orange_light']),
                        "Tốt nghiệp": (C['blue'],   C['blue_light']),
                    }
                    fg, bg = color_map.get(val, (C['text'], "white"))
                    item.setForeground(QColor(fg))
                    item.setBackground(QColor(bg))
                    item.setFont(QFont("Segoe UI", 11, QFont.Bold))
                elif key == "gpa":
                    try:
                        g = float(val)
                        if g >= 3.2:   item.setForeground(QColor(C['green']))
                        elif g >= 2.0: item.setForeground(QColor(C['blue']))
                        else:          item.setForeground(QColor(C['red']))
                    except: pass
                self._table.setItem(row_idx, col, item)
            self._table.setRowHeight(row_idx, 42)

    def _update_stats(self, rows):
        total = len(rows)
        self._card_sv.update_value(f"{total:,}")
        if total:
            pass_count = sum(1 for r in rows if r.get("gpa", 0) >= 2.0)
            pct = round(pass_count / total * 100, 1)
            self._card_pass.update_value(f"{pct}%")
        else:
            self._card_pass.update_value("—")

    def _update_dash_table(self, rows):
        top8 = rows[:8]
        self._dash_table.setRowCount(0)
        for r in top8:
            ri = self._dash_table.rowCount()
            self._dash_table.insertRow(ri)
            for ci, key in enumerate(["mssv", "ho_ten", "lop", "gpa"]):
                self._dash_table.setItem(ri, ci, QTableWidgetItem(str(r.get(key, ""))))
            self._dash_table.setRowHeight(ri, 38)

    def _filter_table(self):
        q      = self._search.text().lower()
        status = self._filter_status.currentText()
        filtered = []
        for r in self._all_rows:
            if status != "Tất cả" and r.get("trang_thai", "") != status:
                continue
            haystack = " ".join(str(v) for v in r.values()).lower()
            if q in haystack:
                filtered.append(r)
        self._render_table(filtered)
        self._status_lbl.setText(f"🔍  Tìm thấy {len(filtered)}/{len(self._all_rows)} sinh viên")

    def _selected_row_data(self):
        row = self._table.currentRow()
        if row < 0:
            return None
        data = {}
        for col, key in enumerate(self.KEYS):
            item = self._table.item(row, col)
            data[key] = item.text() if item else ""
            if col == 0 and item:
                data["_id"] = item.data(Qt.UserRole)
        try:
            data["gpa"] = float(data.get("gpa", 0))
        except: pass
        return data

    def _add_student(self):
        dlg = StudentDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            w = FirebaseWorker("add", dlg.result_data)
            w.done.connect(lambda msg: (self._load_data(), Toast(self, f"  ✅  {msg}", True)))
            w.error_occurred.connect(self._on_error)
            self._workers.append(w)
            w.start()

    def _edit_student(self):
        data = self._selected_row_data()
        if not data:
            Toast(self, "  ⚠️  Vui lòng chọn một hàng", False)
            return
        dlg = StudentDialog(self, data)
        if dlg.exec_() == QDialog.Accepted:
            w = FirebaseWorker("update", dlg.result_data)
            w.done.connect(lambda msg: (self._load_data(), Toast(self, f"  ✅  {msg}", True)))
            w.error_occurred.connect(self._on_error)
            self._workers.append(w)
            w.start()

    def _delete_student(self):
        data = self._selected_row_data()
        if not data:
            Toast(self, "  ⚠️  Vui lòng chọn một hàng", False)
            return
        name = data.get("ho_ten", "?")
        reply = QMessageBox.question(
            self, "Xác nhận xóa",
            f"Bạn có chắc muốn xóa sinh viên <b>{name}</b>?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            w = FirebaseWorker("delete", data["_id"])
            w.done.connect(lambda msg: (self._load_data(), Toast(self, f"  🗑  {msg}", True)))
            w.error_occurred.connect(self._on_error)
            self._workers.append(w)
            w.start()

    def _on_error(self, msg):
        Toast(self, f"  ❌  Lỗi: {msg}", False)
        self._status_lbl.setText(f"❌ Lỗi: {msg}")


# ─────────────────────────────────────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Font mặc định
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    win = StudentWindow()
    win.show()
    sys.exit(app.exec_())
