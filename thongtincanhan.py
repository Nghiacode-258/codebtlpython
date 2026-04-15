import sys
from PyQt5 import QtCore, QtGui, QtWidgets

STYLE_SHEET = """
    QWidget {
        background-color: white;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    QLabel#pageTitle {
        font-size: 16px;
        font-weight: bold;
        color: #111827;
        padding: 16px 24px 16px 24px;
        background-color: white;
    }
    QFrame#alertBanner {
        background-color: #EBF5FF;
        border: 1px solid #93C5FD;
        border-radius: 4px;
    }
    QLabel#alertText {
        color: #1E3A8A;
        font-size: 13px;
    }
    
    QPushButton#btnCapNhat {
        background-color: #DC2626; 
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: 500;
    }
    QPushButton#btnCapNhat:hover { background-color: #B91C1C; }

    QPushButton.outlineBtn {
        background-color: white;
        color: #374151;
        border: 1px solid #D1D5DB;
        border-radius: 4px;
        padding: 8px 16px;
        font-size: 13px;
    }
    QPushButton.outlineBtn:hover { background-color: #F3F4F6; }

    QLabel#cardMainTitle {
        font-size: 20px;
        color: #374151;
        margin-bottom: 24px;
    }

    QLabel.infoLabel {
        font-size: 13px;
        color: #111827;
    }
    
    QLabel.badgeBlue {
        background-color: #EBF5FF;
        color: #2563EB;
        border: 1px solid #93C5FD;
        border-radius: 4px;
        font-size: 11px;
        padding: 2px 6px;
        font-weight: 500;
    }
"""

class PersonalInfoWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLE_SHEET)
        self.setup_ui()

    def setup_ui(self):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Trích header
        header = QtWidgets.QLabel("Thông tin cá nhân")
        header.setObjectName("pageTitle")
        root.addWidget(header)

        # Line separator after title
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setStyleSheet("background-color: #E5E7EB; max-height: 1px; border: none;")
        root.addWidget(line)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setStyleSheet("background: white;")

        content = QtWidgets.QWidget()
        content.setStyleSheet("background: white;")
        cl = QtWidgets.QVBoxLayout(content)
        cl.setContentsMargins(32, 24, 32, 32)
        cl.setSpacing(16)
        
        # Banner
        banner = QtWidgets.QFrame()
        banner.setObjectName("alertBanner")
        banner_layout = QtWidgets.QHBoxLayout(banner)
        banner_layout.setContentsMargins(20, 14, 20, 14)
        alert_text = QtWidgets.QLabel('Đợt cập nhật hồ sơ <b>"Đợt cập nhật hồ sơ"</b> từ ngày <b>01/11/2024</b> đến ngày <b>31/03/2028</b>')
        alert_text.setObjectName("alertText")
        banner_layout.addWidget(alert_text)
        cl.addWidget(banner)

        # Action Buttons
        action_bar = QtWidgets.QHBoxLayout()
        action_bar.setSpacing(12)
        
        btn1 = QtWidgets.QPushButton("✎ Cập nhật hồ sơ")
        btn1.setObjectName("btnCapNhat")
        btn1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        action_bar.addWidget(btn1)
        
        btn2 = QtWidgets.QPushButton("☰ Học bạ số")
        btn2.setProperty("class", "outlineBtn")
        btn2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        action_bar.addWidget(btn2)
        
        btn3 = QtWidgets.QPushButton("⟲ Cập nhật ảnh nhận diện")
        btn3.setProperty("class", "outlineBtn")
        btn3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        action_bar.addWidget(btn3)
        
        action_bar.addStretch()
        cl.addLayout(action_bar)
        
        # Thêm padding trước SƠ YẾU LÝ LỊCH
        cl.addSpacing(32)

        title = QtWidgets.QLabel("SƠ YẾU LÝ LỊCH")
        title.setObjectName("cardMainTitle")
        title.setAlignment(QtCore.Qt.AlignCenter)
        cl.addWidget(title)
        
        # Body (Avatar + Info)
        body = QtWidgets.QHBoxLayout()
        body.setSpacing(48)
        body.setAlignment(QtCore.Qt.AlignTop)
        
        # Avatar Col
        avatar_lbl = QtWidgets.QLabel()
        # Create a dark rectangle to mimic the placeholder in the image dimensions
        avatar_lbl.setFixedSize(150, 190)
        avatar_lbl.setStyleSheet("background-color: #2D3748; border: 1px solid #E5E7EB; border-radius: 4px;")
        
        avatar_wrapper = QtWidgets.QVBoxLayout()
        avatar_wrapper.addWidget(avatar_lbl)
        avatar_wrapper.addStretch()
        
        body.addLayout(avatar_wrapper)
        
        # Grid Info Col
        info_col = self._build_info_grid()
        body.addLayout(info_col, 1)

        cl.addLayout(body)
        cl.addStretch()

        scroll.setWidget(content)
        root.addWidget(scroll, 1)
        
    def _lbl(self, html):
        lbl = QtWidgets.QLabel(html)
        lbl.setProperty("class", "infoLabel")
        lbl.setWordWrap(True)
        lbl.setTextFormat(QtCore.Qt.RichText)
        return lbl
        
    def _badge(self, text):
        lbl = QtWidgets.QLabel(text)
        lbl.setProperty("class", "badgeBlue")
        return lbl

    def _build_info_grid(self):
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(18)
        grid.setVerticalSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)
        
        # Để các cột chia đều hoặc auto-fit
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(2, 2)
        
        # Helper to align properly
        
        # Row 0
        grid.addWidget(self._lbl("<b>1. Mã sinh viên:</b> B24DCVN074"), 0, 0)
        grid.addWidget(self._lbl("<b>2. Họ và tên:</b> Nguyễn Đình Nghĩa"), 0, 1, 1, 2)
        
        # Row 1
        grid.addWidget(self._lbl("<b>3. Giới tính:</b> Nam"), 1, 0)
        grid.addWidget(self._lbl("<b>4. Ngày sinh:</b> 25/08/2006"), 1, 1)
        
        trang_thai_layout = QtWidgets.QHBoxLayout()
        trang_thai_layout.addWidget(self._lbl("<b>5. Trạng thái học:</b>"))
        trang_thai_layout.addWidget(self._badge("Đang học"))
        trang_thai_layout.addStretch()
        w = QtWidgets.QWidget()
        w.setLayout(trang_thai_layout)
        trang_thai_layout.setContentsMargins(0,0,0,0)
        grid.addWidget(w, 1, 2)
        
        # Row 2
        grid.addWidget(self._lbl("<b>6. CCCD/CMND:</b> 038206016228, Ngày cấp: 19/04/2024, Nơi cấp: Thanh Hóa"), 2, 0, 1, 3)
        
        # Row 3
        grid.addWidget(self._lbl("<b>7. Số điện thoại:</b> 0375 853 601"), 3, 0)
        grid.addWidget(self._lbl("<b>8. Email:</b> nghiand.b24vn074@stu.ptit.edu.vn"), 3, 1, 1, 2)
        
        # Row 4
        khoa_layout = QtWidgets.QHBoxLayout()
        khoa_layout.addWidget(self._lbl("<b>9. Khóa ngành đào tạo:</b> D24CQ - Công nghệ thông tin Việt - Nhật"))
        khoa_layout.addWidget(self._badge("Đang học"))
        khoa_layout.addWidget(self._lbl("(Chuyên ngành: <i>Chưa cập nhật</i>)"))
        khoa_layout.addStretch()
        w_khoa = QtWidgets.QWidget()
        w_khoa.setLayout(khoa_layout)
        khoa_layout.setContentsMargins(0,0,0,0)
        grid.addWidget(w_khoa, 4, 0, 1, 3)
        
        # Row 5
        grid.addWidget(self._lbl("<b>10. Quốc tịch:</b> Việt Nam"), 5, 0)
        grid.addWidget(self._lbl("<b>11. Dân tộc:</b> Kinh"), 5, 1)
        grid.addWidget(self._lbl("<b>12. Tôn giáo:</b> Không"), 5, 2)
        
        # Row 6
        grid.addWidget(self._lbl("<b>13. Địa chỉ thường trú:</b>"), 6, 0, 1, 3)
        
        # Row 7
        grid.addWidget(self._lbl("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tỉnh/Thành phố: Tỉnh Thanh Hóa"), 7, 0)
        grid.addWidget(self._lbl("Xã/Phường/Đặc khu: Xã Trường Trung"), 7, 1)
        grid.addWidget(self._lbl("Địa chỉ: Thôn Phượng Đoài"), 7, 2)
        
        # Row 8
        grid.addWidget(self._lbl("<b>14. Đảng:</b>"), 8, 0, 1, 3)
        
        # Row 9
        grid.addWidget(self._lbl("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ngày vào Đảng dự bị: 27/08/2024"), 9, 0)
        grid.addWidget(self._lbl("Ngày vào Đảng chính thức: 27/08/2024"), 9, 2)
        
        # Row 10
        grid.addWidget(self._lbl("<b>15. Số bảo hiểm sinh viên:</b> HS4383822953565"), 10, 0)
        grid.addWidget(self._lbl("<b>16. Mã bệnh viện khám chữa bệnh:</b>"), 10, 1, 1, 2)
        
        # Row 11
        grid.addWidget(self._lbl("<b>17. Tài khoản ngân hàng:</b>"), 11, 0, 1, 3)
        
        # Row 12
        grid.addWidget(self._lbl("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tên ngân hàng: MB BANK"), 12, 0)
        grid.addWidget(self._lbl("Số tài khoản: 25080625082006"), 12, 2)
        
        return grid

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QtGui.QFont("Segoe UI", 10))

    window = PersonalInfoWidget()
    window.setWindowTitle("Thông tin cá nhân")
    window.resize(1200, 700)
    window.show()
    sys.exit(app.exec_())