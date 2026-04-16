import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"D:\VS code\codewep\btlpython\key.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

class C:
    BG = "#F8F9FA"
    CARD = "#FFFFFF"
    BORDER = "#E5E7EB"

    TXT = "#111827"
    TXT2 = "#374151"
    TXT3 = "#6B7280"

    RED = "#C81E1E"
    RED_HOVER = "#B91C1C"
    RED_BG = "#FEE2E2"

    GREEN = "#22C55E"
    GREEN_BG = "#DCFCE7"
    GREEN_BADGE = "#16A34A"

    BLUE = "#3B82F6"
    BLUE_BG = "#DBEAFE"

    GRAY_BADGE = "#F3F4F6"
    GRAY_TXT = "#4B5563"

    HEADER_BG = "#FFFFFF"
    TAB_BG = "#FFFFFF"
    TABLE_HEADER = "#F9FAFB"
    CODE = "#EF4444"


def add_shadow(widget, blur=16, y=2, color="#00000010"):
    shadow = QtWidgets.QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setOffset(0, y)
    shadow.setColor(QtGui.QColor(color))
    widget.setGraphicsEffect(shadow)


# =========================
# SMALL ICON
# =========================
class IconSquare(QtWidgets.QWidget):
    def __init__(self, icon, bg, fg, size=48, radius=12, parent=None):
        super().__init__(parent)
        self.icon = icon
        self.bg = QtGui.QColor(bg)
        self.fg = QtGui.QColor(fg)
        self.radius = radius
        self.setFixedSize(size, size)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        path = QtGui.QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)
        painter.fillPath(path, QtGui.QBrush(self.bg))

        painter.setPen(QtGui.QPen(self.fg))
        font = QtGui.QFont("Segoe UI Emoji", int(self.width() * 0.40))
        painter.setFont(font)
        painter.drawText(self.rect(), QtCore.Qt.AlignCenter, self.icon)


# =========================
# STAT CARD
# =========================
class StatCard(QtWidgets.QFrame):
    def __init__(self, title, value, icon, icon_bg, icon_fg, parent=None):
        super().__init__(parent)

        self.setObjectName("StatCard")
        self.setStyleSheet(f"""
            QFrame#StatCard {{
                background: {C.CARD};
                border: 1px solid {C.BORDER};
                border-radius: 14px;
            }}
        """)

        self.setMinimumHeight(110)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        add_shadow(self)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        layout.addWidget(IconSquare(icon, icon_bg, icon_fg))

        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setSpacing(4)

        self.title_label = QtWidgets.QLabel(title)
        self.title_label.setFont(QtGui.QFont("Segoe UI", 10))
        self.title_label.setStyleSheet(f"color: {C.TXT3}; background: transparent;")

        self.value_label = QtWidgets.QLabel(str(value))
        self.value_label.setFont(QtGui.QFont("Segoe UI", 21, QtGui.QFont.Bold))
        self.value_label.setStyleSheet(f"color: {C.TXT}; background: transparent;")

        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.value_label)

        layout.addLayout(text_layout)
        layout.addStretch()

    def set_value(self, value):
        self.value_label.setText(str(value))


# =========================
# STATUS BADGE
# =========================
class Badge(QtWidgets.QLabel):
    MAP = {
        "Đang học": (C.GREEN_BG, C.GREEN_BADGE),
        "Đã kết thúc": (C.GRAY_BADGE, C.GRAY_TXT),
    }

    def __init__(self, status, parent=None):
        super().__init__(status, parent)
        bg, fg = self.MAP.get(status, (C.GRAY_BADGE, C.GRAY_TXT))

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFont(QtGui.QFont("Segoe UI", 9, QtGui.QFont.Bold))
        self.setFixedHeight(26)
        self.setStyleSheet(f"""
            QLabel {{
                background: {bg};
                color: {fg};
                border-radius: 12px;
                padding: 2px 12px;
            }}
        """)


# =========================
# DIALOG
# =========================
class CreditDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data = data or {}

        self.setWindowTitle("Thêm lớp tín chỉ" if not data else "Sửa lớp tín chỉ")
        self.setModal(True)
        self.resize(520, 520)

        self.setStyleSheet(f"""
            QDialog {{
                background-color: #F8F9FA;
            }}
            QLabel {{
                font-family: 'Segoe UI';
                font-size: 13px;
                color: #374151;
            }}
            QLineEdit, QComboBox {{
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: white;
                font-size: 13px;
                color: #111827;
            }}
            QLineEdit:focus, QComboBox:focus {{
                border: 1px solid {C.RED};
            }}
            QPushButton#saveBtn {{
                background-color: {C.RED};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton#saveBtn:hover {{
                background-color: {C.RED_HOVER};
            }}
        """)

        self.build_ui()
        self.fill_data()

    def build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(16)
        form_layout.setLabelAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.inp_course_code = QtWidgets.QLineEdit()
        self.inp_course_name = QtWidgets.QLineEdit()
        self.inp_credits = QtWidgets.QLineEdit()
        self.inp_class_code = QtWidgets.QLineEdit()
        self.inp_teacher = QtWidgets.QLineEdit()
        self.inp_schedule = QtWidgets.QLineEdit()
        self.inp_room = QtWidgets.QLineEdit()
        self.inp_size = QtWidgets.QLineEdit()
        self.inp_semester = QtWidgets.QLineEdit()

        self.cmb_status = QtWidgets.QComboBox()
        self.cmb_status.addItems(["Đang học", "Đã kết thúc"])

        form_layout.addRow("Mã HP", self.inp_course_code)
        form_layout.addRow("Tên học phần", self.inp_course_name)
        form_layout.addRow("Tín chỉ", self.inp_credits)
        form_layout.addRow("Lớp HP", self.inp_class_code)
        form_layout.addRow("Giảng viên", self.inp_teacher)
        form_layout.addRow("Lịch học", self.inp_schedule)
        form_layout.addRow("Phòng", self.inp_room)
        form_layout.addRow("Sĩ số", self.inp_size)
        form_layout.addRow("Trạng thái", self.cmb_status)
        form_layout.addRow("Học kỳ", self.inp_semester)

        layout.addLayout(form_layout)
        layout.addStretch()

        save_btn = QtWidgets.QPushButton("Lưu")
        save_btn.setObjectName("saveBtn")
        save_btn.clicked.connect(self.validate_and_accept)
        layout.addWidget(save_btn)

    def fill_data(self):
        if not self.data:
            return

        self.inp_course_code.setText(self.data.get("course_code", ""))
        self.inp_course_name.setText(self.data.get("course_name", ""))
        self.inp_credits.setText(str(self.data.get("credits", "")))
        self.inp_class_code.setText(self.data.get("class_code", ""))
        self.inp_teacher.setText(self.data.get("teacher", ""))
        self.inp_schedule.setText(self.data.get("schedule", ""))
        self.inp_room.setText(self.data.get("room", ""))
        self.inp_size.setText(self.data.get("size", ""))
        self.inp_semester.setText(self.data.get("semester", ""))

        idx = self.cmb_status.findText(self.data.get("status", "Đang học"))
        if idx >= 0:
            self.cmb_status.setCurrentIndex(idx)

    def validate_and_accept(self):
        if not self.inp_course_code.text().strip():
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Mã HP không được để trống.")
            return

        if not self.inp_course_name.text().strip():
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Tên học phần không được để trống.")
            return

        try:
            int(self.inp_credits.text().strip())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Tín chỉ phải là số nguyên.")
            return

        self.accept()

    def get_data(self):
        return {
            "course_code": self.inp_course_code.text().strip(),
            "course_name": self.inp_course_name.text().strip(),
            "credits": int(self.inp_credits.text().strip()),
            "class_code": self.inp_class_code.text().strip(),
            "teacher": self.inp_teacher.text().strip(),
            "schedule": self.inp_schedule.text().strip(),
            "room": self.inp_room.text().strip(),
            "size": self.inp_size.text().strip(),
            "status": self.cmb_status.currentText(),
            "semester": self.inp_semester.text().strip(),
        }


# =========================
# PAGE
# =========================
class CreditClassWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.all_rows = []
        self.filtered_rows = []

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {C.BG};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QLabel#pageTitle {{
                font-size: 22px;
                font-weight: bold;
                color: {C.TXT};
            }}
            QFrame.cardFrame {{
                background-color: {C.CARD};
                border: 1px solid {C.BORDER};
                border-radius: 12px;
            }}
        """)

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.create_header())

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setStyleSheet("background: #F8F9FA; border: none;")

        body = QtWidgets.QWidget()
        body.setStyleSheet("background: #F8F9FA;")

        body_layout = QtWidgets.QVBoxLayout(body)
        body_layout.setContentsMargins(20, 20, 20, 20)
        body_layout.setSpacing(16)
        body_layout.setAlignment(QtCore.Qt.AlignTop)

        body_layout.addLayout(self.create_stats_row())
        body_layout.addWidget(self.create_table_card())

        scroll.setWidget(body)
        main_layout.addWidget(scroll, 1)

    def create_header(self):
        header = QtWidgets.QFrame()
        header.setFixedHeight(56)
        header.setStyleSheet("background-color: white; border-bottom: 1px solid #E5E7EB;")

        layout = QtWidgets.QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)

        title = QtWidgets.QLabel("Lớp tín chỉ")
        title.setObjectName("pageTitle")
        layout.addWidget(title)
        layout.addStretch()

        return header

    def create_stats_row(self):
        stats_layout = QtWidgets.QHBoxLayout()
        stats_layout.setSpacing(16)

        self.card_total = StatCard("Tổng số lớp", "0", "📚", C.RED_BG, C.RED)
        self.card_studying = StatCard("Đang học", "0", "🕐", C.GREEN_BG, C.GREEN)
        self.card_credits = StatCard("Tổng tín chỉ", "0", "📖", C.BLUE_BG, C.BLUE)

        stats_layout.addWidget(self.card_total)
        stats_layout.addWidget(self.card_studying)
        stats_layout.addWidget(self.card_credits)

        return stats_layout

    def create_table_card(self):
        frame = QtWidgets.QFrame()
        frame.setProperty("class", "cardFrame")

        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.setSpacing(10)

        title = QtWidgets.QLabel("Danh sách lớp tín chỉ")
        title.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Bold))
        title.setStyleSheet(f"color: {C.TXT};")
        top_layout.addWidget(title)
        top_layout.addStretch()

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("🔍  Tìm kiếm lớp...")
        self.search_input.setFixedWidth(280)
        self.search_input.setFixedHeight(40)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 0 12px;
                background-color: white;
                font-size: 13px;
                color: {C.TXT};
            }}
            QLineEdit:focus {{
                border: 1px solid {C.BLUE};
            }}
        """)
        self.search_input.textChanged.connect(self.apply_filters)
        top_layout.addWidget(self.search_input)

        self.add_btn = QtWidgets.QPushButton("➕ Thêm lớp tín chỉ")
        self.add_btn.setFixedHeight(40)
        self.add_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {C.RED};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 16px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {C.RED_HOVER};
            }}
        """)
        self.add_btn.clicked.connect(self.add_course)
        top_layout.addWidget(self.add_btn)

        layout.addLayout(top_layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Mã HP",
            "Tên học phần",
            "Tín chỉ",
            "Lớp HP",
            "Giảng viên",
            "Lịch học",
            "Phòng",
            "Sĩ số",
            "Trạng thái",
            "Hành động",
        ])

        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setAlternatingRowColors(False)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setWordWrap(False)
        self.table.setFrameShape(QtWidgets.QFrame.NoFrame)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        header.setStretchLastSection(False)
        header.setDefaultAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.table.setStyleSheet(f"""
            QTableWidget {{
                background: white;
                border: 1px solid {C.BORDER};
                border-radius: 10px;
                font-size: 14px;
                color: {C.TXT};
            }}
            QTableWidget::item {{
                padding: 8px 10px;
                border-bottom: 1px solid {C.BORDER};
                color: {C.TXT};
            }}
            QTableWidget::item:selected {{
                background: #F9FAFB;
                color: {C.TXT};
            }}
            QHeaderView::section {{
                background: {C.TABLE_HEADER};
                color: {C.TXT2};
                font-weight: bold;
                font-size: 13px;
                padding: 12px 10px;
                border: none;
                border-bottom: 1px solid {C.BORDER};
            }}
            QScrollBar:vertical {{
                width: 8px;
                background: transparent;
            }}
            QScrollBar::handle:vertical {{
                background: #D1D5DB;
                border-radius: 4px;
            }}
            QScrollBar:horizontal {{
                height: 0px;
                background: transparent;
                border: none;
            }}
        """)

        layout.addWidget(self.table)
        return frame

    def resizeEvent(self, event):
        super().resizeEvent(event)
        QtCore.QTimer.singleShot(0, self.apply_column_sizes)

    def apply_column_sizes(self):
        width = self.table.viewport().width()
        if width <= 0:
            return

        available = width - 24

        ratios = [8, 20, 6, 9, 16, 16, 8, 7, 11, 9]
        ratio_sum = sum(ratios)

        widths = [int(available * r / ratio_sum) for r in ratios]
        diff = available - sum(widths)
        widths[1] += diff

        min_widths = [70, 170, 55, 75, 130, 130, 70, 60, 100, 90]
        for i, w in enumerate(widths):
            self.table.setColumnWidth(i, max(w, min_widths[i]))

    def make_item(self, text, bold=False, color=None, align=None):
        item = QtWidgets.QTableWidgetItem(str(text))
        font = QtGui.QFont("Segoe UI", 10)
        if bold:
            font.setBold(True)
        item.setFont(font)

        item.setForeground(QtGui.QColor(color if color else C.TXT))
        if align:
            item.setTextAlignment(align)
        return item

    def load_data(self):
        try:
            docs = db.collection("credit").stream()
            rows = []

            for doc in docs:
                data = doc.to_dict()
                rows.append({
                    "id": doc.id,
                    "course_code": data.get("course_code", ""),
                    "course_name": data.get("course_name", ""),
                    "credits": str(data.get("credits", "")),
                    "class_code": data.get("class_code", ""),
                    "teacher": data.get("teacher", ""),
                    "schedule": data.get("schedule", ""),
                    "room": data.get("room", ""),
                    "size": data.get("size", ""),
                    "status": data.get("status", "Đang học"),
                    "semester": data.get("semester", ""),
                })

            self.all_rows = rows
            self.filtered_rows = rows.copy()
            self.display(self.filtered_rows)
            self.update_stats(self.all_rows)

        except Exception as e:
            print(f"Lỗi tải dữ liệu lớp tín chỉ: {e}")

    def display(self, rows):
        self.table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            self.table.setRowHeight(row_index, 52)

            self.table.setItem(row_index, 0, self.make_item(row.get("course_code", ""), bold=True, color=C.CODE))
            self.table.setItem(row_index, 1, self.make_item(row.get("course_name", "")))
            self.table.setItem(row_index, 2, self.make_item(row.get("credits", ""), align=QtCore.Qt.AlignCenter))
            self.table.setItem(row_index, 3, self.make_item(row.get("class_code", ""), color=C.TXT2))
            self.table.setItem(row_index, 4, self.make_item("👤  " + row.get("teacher", "")))
            self.table.setItem(row_index, 5, self.make_item("🕐  " + row.get("schedule", "")))
            self.table.setItem(row_index, 6, self.make_item("📍  " + row.get("room", "")))
            self.table.setItem(row_index, 7, self.make_item(row.get("size", ""), align=QtCore.Qt.AlignCenter))

            badge = Badge(row.get("status", ""))
            badge_widget = QtWidgets.QWidget()
            badge_widget.setStyleSheet("background: transparent;")
            badge_layout = QtWidgets.QHBoxLayout(badge_widget)
            badge_layout.setContentsMargins(4, 0, 4, 0)
            badge_layout.addWidget(badge)
            badge_layout.setAlignment(QtCore.Qt.AlignCenter)
            self.table.setCellWidget(row_index, 8, badge_widget)

            action_widget = QtWidgets.QWidget()
            action_widget.setStyleSheet("background: transparent;")
            action_layout = QtWidgets.QHBoxLayout(action_widget)
            action_layout.setContentsMargins(4, 4, 4, 4)
            action_layout.setSpacing(6)
            action_layout.setAlignment(QtCore.Qt.AlignCenter)

            edit_btn = QtWidgets.QPushButton("✏")
            edit_btn.setFixedSize(30, 28)
            edit_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #F3F4F6;
                    border: 1px solid #E5E7EB;
                    border-radius: 6px;
                    color: #111827;
                }
                QPushButton:hover {
                    background-color: #E5E7EB;
                }
            """)
            edit_btn.clicked.connect(lambda _, r=row: self.edit_course(r))

            delete_btn = QtWidgets.QPushButton("🗑")
            delete_btn.setFixedSize(30, 28)
            delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FEE2E2;
                    color: #DC2626;
                    border: none;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #FECACA;
                }
            """)
            delete_btn.clicked.connect(lambda _, doc_id=row["id"]: self.delete_course(doc_id))

            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            self.table.setCellWidget(row_index, 9, action_widget)

        self.apply_column_sizes()

    def apply_filters(self):
        keyword = self.search_input.text().strip().lower()

        self.filtered_rows = [
            row for row in self.all_rows
            if keyword in " ".join([
                row.get("course_code", ""),
                row.get("course_name", ""),
                row.get("class_code", ""),
                row.get("teacher", ""),
                row.get("schedule", ""),
                row.get("room", ""),
                row.get("size", ""),
                row.get("status", ""),
                row.get("semester", ""),
            ]).lower()
        ]

        self.display(self.filtered_rows)

    def add_course(self):
        dialog = CreditDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            try:
                db.collection("credit").add(dialog.get_data())
                QtWidgets.QMessageBox.information(self, "Thành công", "Đã thêm lớp tín chỉ.")
                self.load_data()
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Lỗi", f"Không thể thêm dữ liệu:\n{e}")

    def edit_course(self, row):
        dialog = CreditDialog(self, data=row)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            try:
                db.collection("credit").document(row["id"]).update(dialog.get_data())
                QtWidgets.QMessageBox.information(self, "Thành công", "Đã cập nhật lớp tín chỉ.")
                self.load_data()
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Lỗi", f"Không thể cập nhật dữ liệu:\n{e}")

    def delete_course(self, doc_id):
        reply = QtWidgets.QMessageBox.question(
            self,
            "Xóa lớp tín chỉ",
            "Bạn có chắc chắn muốn xóa lớp tín chỉ này không?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                db.collection("credit").document(doc_id).delete()
                QtWidgets.QMessageBox.information(self, "Thành công", "Đã xóa lớp tín chỉ.")
                self.load_data()
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Lỗi", f"Không thể xóa dữ liệu:\n{e}")

    def update_stats(self, rows):
        total_classes = len(rows)
        studying_classes = sum(1 for row in rows if row.get("status", "") == "Đang học")

        total_credits = 0
        for row in rows:
            try:
                total_credits += int(row.get("credits", 0))
            except Exception:
                pass

        self.card_total.set_value(total_classes)
        self.card_studying.set_value(studying_classes)
        self.card_credits.set_value(total_credits)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QtGui.QFont("Segoe UI", 10))

    window = CreditClassWidget()
    window.resize(1280, 760)
    window.show()

    sys.exit(app.exec_())