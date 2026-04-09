import sys
import re
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QPointF
from PyQt5.QtGui import QColor, QFont, QPalette, QIcon, QPixmap, QPainter, QPolygonF, QLinearGradient, QPen
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QScrollArea, QMessageBox, QDialog,
    QFormLayout, QComboBox, QSizePolicy, QStackedWidget, QGridLayout,
    QAbstractItemView, QSplitter, QGraphicsDropShadowEffect
)

import firebase_admin
from firebase_admin import credentials, firestore

# ==========================================
# WIDGET MÔ PHỎNG BIỂU ĐỒ (Dùng QPainter)
# ==========================================
class MockAreaChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(250)
        self.setStyleSheet("background-color: white; border-radius: 10px;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        width = rect.width()
        height = rect.height()

        # Dữ liệu mô phỏng
        points = [
            QPointF(0, height * 0.6),
            QPointF(width * 0.2, height * 0.5),
            QPointF(width * 0.4, height * 0.45),
            QPointF(width * 0.6, height * 0.35),
            QPointF(width * 0.8, height * 0.4),
            QPointF(width, height * 0.3)
        ]

        # Vẽ đường biểu đồ
        pen = QPen(QColor("#d32f2f"), 2)
        painter.setPen(pen)
        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i+1])

        # Vẽ vùng Gradient
        polygon = QPolygonF(points)
        polygon.append(QPointF(width, height))
        polygon.append(QPointF(0, height))

        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0.0, QColor(211, 47, 47, 100)) # Đỏ nhạt có alpha
        gradient.setColorAt(1.0, QColor(255, 255, 255, 0))   # Trong suốt

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(polygon)

# ==========================================
# GIAO DIỆN CHÍNH
# ==========================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("S-Link Dashboard (PyQt5)")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #f4f6f9; font-family: Arial;")

        # Container chính
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setup_sidebar()
        self.setup_main_content()

    def add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 30))
        widget.setGraphicsEffect(shadow)

    # --- SIDEBAR ---
    def setup_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("background-color: #ffffff; border-right: 1px solid #e0e0e0;")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)

        # Logo
        logo_layout = QHBoxLayout()
        logo_lbl = QLabel("PTIT")
        logo_lbl.setStyleSheet("color: #d32f2f; font-weight: bold; font-size: 16px; border: 1px solid #d32f2f; border-radius: 15px; padding: 5px;")
        logo_lbl.setFixedSize(40, 40)
        logo_lbl.setAlignment(Qt.AlignCenter)
        
        title_lbl = QLabel("S-Link")
        title_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; border: none;")
        
        logo_layout.addWidget(logo_lbl)
        logo_layout.addWidget(title_lbl)
        logo_layout.addStretch()
        sidebar_layout.addLayout(logo_layout)
        sidebar_layout.addSpacing(20)

        # Menu Items
        menu_items = [
            ("Trang chủ", True), ("Thông tin cá nhân", False), 
            ("Danh sách sinh viên", False), ("Lớp tín chỉ", False), 
            ("Lớp hành chính", False), ("Cài đặt", False)
        ]

        for text, is_active in menu_items:
            btn = QPushButton(text)
            if is_active:
                btn.setStyleSheet("""
                    QPushButton {
                        text-align: left; padding: 10px 15px; background-color: #ffffff; 
                        color: #d32f2f; font-weight: bold; border: none; font-size: 14px;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        text-align: left; padding: 10px 15px; background-color: #ffffff; 
                        color: #555555; border: none; font-size: 14px;
                    }
                    QPushButton:hover { background-color: #f0f0f0; border-radius: 5px; }
                """)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Nút Đăng xuất
        logout_btn = QPushButton("Đăng xuất")
        logout_btn.setStyleSheet("text-align: left; padding: 10px 15px; color: #555; border: none; border-top: 1px solid #eee;")
        sidebar_layout.addWidget(logout_btn)

        self.main_layout.addWidget(self.sidebar)

    # --- KHU VỰC CHÍNH BÊN PHẢI ---
    def setup_main_content(self):
        self.right_container = QWidget()
        right_layout = QVBoxLayout(self.right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Header
        self.setup_header(right_layout)

        # Scroll Area cho nội dung (để tránh vỡ layout khi màn hình nhỏ)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 20, 30, 20)
        content_layout.setSpacing(20)

        # Thêm các thành phần vào content_layout
        self.setup_kpi_cards(content_layout)
        self.setup_charts_and_activity(content_layout)
        
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        
        right_layout.addWidget(scroll_area)
        self.main_layout.addWidget(self.right_container)

    # --- HEADER ---
    def setup_header(self, parent_layout):
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("background-color: #ffffff; border-bottom: 1px solid #e0e0e0;")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(30, 0, 30, 0)

        # Tiêu đề
        title = QLabel("Trang chu")
        title.setStyleSheet("font-size: 22px; font-weight: bold; border: none;")
        h_layout.addWidget(title)

        h_layout.addStretch()

        # Thanh tìm kiếm
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Tìm kiếm...")
        search_bar.setFixedWidth(300)
        search_bar.setStyleSheet("""
            QLineEdit {
                padding: 8px 15px; border: 1px solid #ddd; border-radius: 18px; 
                background-color: #f9f9f9; font-size: 13px;
            }
        """)
        h_layout.addWidget(search_bar)
        
        h_layout.addSpacing(20)

        # User Info
        user_info = QLabel("<b>Nguyen Dinh Nghia</b><br><span style='color: #777; font-size: 11px;'>nghia@ptit.edu.vn</span>")
        user_info.setStyleSheet("border: none; font-size: 13px;")
        
        avatar = QLabel("ND")
        avatar.setFixedSize(36, 36)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold; border-radius: 18px; border: none;")

        h_layout.addWidget(avatar)
        h_layout.addWidget(user_info)

        parent_layout.addWidget(header)

    # --- 4 THẺ KPI CHÍNH ---
    def setup_kpi_cards(self, parent_layout):
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        cards_data = [
            ("Tổng sinh viên", "2,847", "+12.5%", "so với tháng trước", "#4caf50"),
            ("Khóa học", "45", "+3", "khóa học đang hoạt động", "#4caf50"),
            ("Lớp học", "128", "+8", "lớp học trong kỳ này", "#4caf50"),
            ("Tỷ lệ đậu", "94.2%", "+2.1%", "tăng so với kỳ trước", "#4caf50")
        ]

        for title, value, delta, desc, color in cards_data:
            card = QFrame()
            card.setStyleSheet("background-color: white; border-radius: 15px;")
            self.add_shadow(card)
            
            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(20, 20, 20, 20)
            
            lbl_title = QLabel(title)
            lbl_title.setStyleSheet("color: #666; font-size: 14px;")
            
            lbl_value = QLabel(value)
            lbl_value.setStyleSheet("font-size: 28px; font-weight: bold; color: #111; margin-top: 5px;")
            
            lbl_desc = QLabel(f"<span style='color: {color}; font-weight: bold;'>{delta}</span> <span style='color: #888;'>{desc}</span>")
            lbl_desc.setStyleSheet("font-size: 12px; margin-top: 10px;")
            
            c_layout.addWidget(lbl_title)
            c_layout.addWidget(lbl_value)
            c_layout.addWidget(lbl_desc)
            
            cards_layout.addWidget(card)

        parent_layout.addLayout(cards_layout)

    # --- BIỂU ĐỒ & HOẠT ĐỘNG ---
    def setup_charts_and_activity(self, parent_layout):
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        # Cột Trái: Biểu đồ
        chart_frame = QFrame()
        chart_frame.setStyleSheet("background-color: white; border-radius: 15px;")
        self.add_shadow(chart_frame)
        chart_layout = QVBoxLayout(chart_frame)
        chart_layout.setContentsMargins(20, 20, 20, 20)
        
        chart_title = QLabel("Biến động sinh viên")
        chart_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        mock_chart = MockAreaChart() # Widget tự vẽ
        
        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(mock_chart)
        chart_layout.addStretch()

        # Cột Phải: Hoạt động gần đây
        activity_frame = QFrame()
        activity_frame.setFixedWidth(350)
        activity_frame.setStyleSheet("background-color: white; border-radius: 15px;")
        self.add_shadow(activity_frame)
        act_layout = QVBoxLayout(activity_frame)
        act_layout.setContentsMargins(20, 20, 20, 20)
        
        act_title = QLabel("Hoạt động gần đây")
        act_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        act_layout.addWidget(act_title)

        activities = [
            ("Sinh viên mới đăng ký", "Nguyễn Minh Tuấn", "5 phút trước", "#ffebee", "#d32f2f"),
            ("Hoàn thành khóa học", "Trần Thị Mai - Lập trình Web", "15 phút trước", "#e8f5e9", "#2e7d32"),
            ("Sinh viên tốt nghiệp", "Lê Văn Hùng", "1 giờ trước", "#e3f2fd", "#1565c0"),
            ("Đạt học bổng xuất sắc", "Phạm Thị Hương", "2 giờ trước", "#fff8e1", "#f57f17")
        ]

        for act, name, time, bg_col, text_col in activities:
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(0, 10, 0, 10)
            
            icon = QLabel("●")
            icon.setFixedSize(40, 40)
            icon.setAlignment(Qt.AlignCenter)
            icon.setStyleSheet(f"background-color: {bg_col}; color: {text_col}; font-size: 18px; border-radius: 20px;")
            
            text_layout = QVBoxLayout()
            lbl_act = QLabel(f"<b>{act}</b>")
            lbl_act.setStyleSheet("font-size: 13px; color: #222;")
            lbl_name = QLabel(name)
            lbl_name.setStyleSheet("font-size: 12px; color: #666;")
            
            text_layout.addWidget(lbl_act)
            text_layout.addWidget(lbl_name)
            
            lbl_time = QLabel(time)
            lbl_time.setStyleSheet("font-size: 11px; color: #999;")
            lbl_time.setAlignment(Qt.AlignRight | Qt.AlignTop)
            
            item_layout.addWidget(icon)
            item_layout.addLayout(text_layout)
            item_layout.addWidget(lbl_time)
            
            act_layout.addWidget(item_widget)
            
            # Đường kẻ ngang
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setStyleSheet("background-color: #f0f0f0;")
            act_layout.addWidget(line)

        act_layout.addStretch()

        bottom_layout.addWidget(chart_frame, stretch=2)
        bottom_layout.addWidget(activity_frame, stretch=1)

        parent_layout.addLayout(bottom_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Thiết lập font mặc định
    font = QFont("Arial", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())