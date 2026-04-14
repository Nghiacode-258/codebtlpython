from PyQt5 import QtCore, QtGui, QtWidgets

STYLE_SHEET = """
    QWidget {
        background-color: #F8F9FA;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    QFrame#topHeader {
        background-color: white;
        border-bottom: 1px solid #E5E7EB;
    }
    QLabel#pageTitle {
        font-size: 20px;
        font-weight: bold;
        color: #111827;
    }
    QLineEdit#searchBox {
        border: 1px solid #D1D5DB;
        border-radius: 20px;
        padding: 6px 16px;
        font-size: 13px;
        color: #374151;
        background-color: white;
        min-width: 220px;
    }

    QLineEdit#searchBox:focus { border: 1px solid #C81E1E; }

    QPushButton#btnCapNhat {
        background-color: #C81E1E; /* Sửa thành #EF4444 nếu muốn đỏ nhạt hơn */
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 18px;
        font-size: 13px;
        font-weight: bold;
    }
    QPushButton#btnCapNhat:hover { background-color: #A41616; }

    QPushButton[class="outlineBtn"] {
        background-color: white;
        color: #374151;
        border: 1px solid #D1D5DB;
        border-radius: 6px;
        padding: 8px 18px;
        font-size: 13px;
    }
    QPushButton[class="outlineBtn"]:hover { background-color: #F3F4F6; }

    QFrame#mainCard {
        background-color: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
    }
    QLabel#cardMainTitle {
        font-size: 17px;
        font-weight: bold;
        color: #111827;
        letter-spacing: 2px;
    }

    QLabel[class="fieldLabel"] {
        font-size: 12px;
        color: #6B7280;
        font-weight: bold;
    }
    
    QLineEdit[class="fieldInput"] {
        border: 1px solid #E5E7EB;
        border-radius: 6px;
        padding: 7px 10px;
        font-size: 13px;
        color: #111827;
        background-color: white;
    }

    QLineEdit[class="fieldInput"]:focus {
        border: 1.5px solid #C81E1E;
        background-color: #FFFAFA;
    }
    
    QLineEdit[class="fieldInput"]:read-only {
        background-color: #F9FAFB;
        color: #9CA3AF;
    }
    
    QLabel[class="sectionLabel"] {
        font-size: 13px;
        font-weight: bold;
        color: #111827;
    }
    QFrame[class="divider"] {
        background-color: #F3F4F6;
        border: none;
        max-height: 1px;
    }
    QFrame#avatarFrame {
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        background: #F9FAFB;
    }
    QPushButton#btnDoiAnh {
        background-color: white;
        border: 1px solid #D1D5DB;
        border-radius: 6px;
        padding: 6px 14px;
        font-size: 12px;
        color: #374151;
    }
    QPushButton#btnDoiAnh:hover { background-color: #F3F4F6; }

    QPushButton#btnLuu {
        background-color: #C81E1E;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 9px 24px;
        font-size: 13px;
        font-weight: bold;
    }
    QPushButton#btnLuu:hover { background-color: #A41616; }
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

        # root.addWidget(self._build_header())
        root.addWidget(self._build_action_bar())

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setStyleSheet("background: #F5F5F5; border: none;")

        content = QtWidgets.QWidget()
        content.setStyleSheet("background: #F5F5F5;")
        cl = QtWidgets.QVBoxLayout(content)
        cl.setContentsMargins(24, 20, 24, 24)
        cl.setSpacing(0)
        cl.addWidget(self._build_main_card())
        cl.addStretch()

        scroll.setWidget(content)
        root.addWidget(scroll, 1)

    def _build_header(self):
        frame = QtWidgets.QFrame()
        frame.setObjectName("topHeader")
        frame.setFixedHeight(56)
        layout = QtWidgets.QHBoxLayout(frame)
        layout.setContentsMargins(24, 0, 24, 0)

        title = QtWidgets.QLabel("Thong tin ca nhan")
        title.setObjectName("pageTitle")
        layout.addWidget(title)
        layout.addStretch()

        search = QtWidgets.QLineEdit()
        search.setObjectName("searchBox")
        search.setPlaceholderText("Tim kiem...")
        layout.addWidget(search)
        layout.addSpacing(12)

        bell = QtWidgets.QPushButton("🔔")
        bell.setFixedSize(36, 36)
        bell.setStyleSheet("QPushButton{background:transparent;border:none;font-size:18px;}"
                           "QPushButton:hover{background:#F3F4F6;border-radius:18px;}")
        layout.addWidget(bell)
        return frame

    def _build_action_bar(self):
        bar = QtWidgets.QWidget()
        bar.setStyleSheet("background:white; border-bottom:1px solid #E5E7EB;")
        bar.setFixedHeight(52)
        layout = QtWidgets.QHBoxLayout(bar)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(10)

        btn1 = QtWidgets.QPushButton("✏  Cập nhật hồ sơ")
        btn1.setObjectName("btnCapNhat")
        btn1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        layout.addWidget(btn1)

        for label in ["📄  Học bạ số", "📷  Cập nhật ảnh"]:
            btn = QtWidgets.QPushButton(label)
            btn.setProperty("class", "outlineBtn")
            btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            layout.addWidget(btn)

        layout.addStretch()
        return bar

    def _build_main_card(self):
        frame = QtWidgets.QFrame()
        frame.setObjectName("mainCard")

        outer = QtWidgets.QVBoxLayout(frame)
        outer.setContentsMargins(32, 28, 32, 32)
        outer.setSpacing(20)

        title = QtWidgets.QLabel("SƠ YẾU LÝ LỊCH")
        title.setObjectName("cardMainTitle")
        title.setAlignment(QtCore.Qt.AlignCenter)
        outer.addWidget(title)

        body = QtWidgets.QHBoxLayout()
        body.setSpacing(28)
        body.setAlignment(QtCore.Qt.AlignTop)
        body.addWidget(self._build_avatar_col())
        body.addWidget(self._build_form_col(), 1)
        outer.addLayout(body)

        return frame

    # ── Cột avatar ───────────────────────────────────────────────
    def _build_avatar_col(self):
        col = QtWidgets.QWidget()
        col.setStyleSheet("background:transparent;")
        col.setFixedWidth(160)
        layout = QtWidgets.QVBoxLayout(col)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)

        av_frame = QtWidgets.QFrame()
        av_frame.setObjectName("avatarFrame")
        av_frame.setFixedSize(130, 160)
        av_inner = QtWidgets.QVBoxLayout(av_frame)
        av_inner.setContentsMargins(0, 0, 0, 0)
        av_inner.setAlignment(QtCore.Qt.AlignCenter)

        av_lbl = QtWidgets.QLabel()
        av_lbl.setFixedSize(128, 158)
        av_lbl.setAlignment(QtCore.Qt.AlignCenter)
        av_lbl.setStyleSheet("background:#E5E7EB; border-radius:8px; color:#9CA3AF; font-size:13px;")
        av_lbl.setText("Anh\nthe")
        av_inner.addWidget(av_lbl)
        layout.addWidget(av_frame, alignment=QtCore.Qt.AlignHCenter)

        btn_doi = QtWidgets.QPushButton("📷  Doi anh")
        btn_doi.setObjectName("btnDoiAnh")
        btn_doi.setFixedWidth(120)
        btn_doi.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        layout.addWidget(btn_doi, alignment=QtCore.Qt.AlignHCenter)
        return col

    def _create_grid_row(self, fields_data):
        g = QtWidgets.QGridLayout()
        g.setContentsMargins(0, 8, 0, 8)
        g.setSpacing(12)
        for col_idx, (label_text, input_widget) in enumerate(fields_data):
            g.addWidget(self._lbl(label_text), 0, col_idx)
            g.addWidget(input_widget, 1, col_idx)
        return g
    
    # ── Cột form nhập liệu ───────────────────────────────────────
    def _build_form_col(self):
        col = QtWidgets.QWidget()
        col.setStyleSheet("background:transparent;")
        layout = QtWidgets.QVBoxLayout(col)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        def add_div():
            sep = QtWidgets.QFrame()
            sep.setFrameShape(QtWidgets.QFrame.HLine)
            sep.setProperty("class", "divider")
            sep.setContentsMargins(0, 4, 0, 4)
            layout.addWidget(sep)

        def add_section_title(text):
            lbl = QtWidgets.QLabel(text)
            lbl.setProperty("class", "sectionLabel")
            lbl.setContentsMargins(0, 12, 0, 6)
            layout.addWidget(lbl)

        self.inp_masv = self._make_input("B24DCVN074", readonly=True)
        self.inp_hoten = self._make_input("Nguyễn Đình Nghĩa")
        self.inp_trangthai = self._make_input("Đang học")
        layout.addLayout(self._create_grid_row([
            ("1. Mã sinh viên", self.inp_masv),
            ("2. Họ và tên", self.inp_hoten),
            ("5. Trạng thái học", self.inp_trangthai)
        ]))
        add_div()

        # ── Hàng 2: Giới tính | Ngày sinh 
        self.inp_gioitinh = self._make_input("Nam")
        self.inp_ngaysinh = self._make_input("25/08/2006")
        layout.addLayout(self._create_grid_row([
            ("3. Giới tính", self.inp_gioitinh),
            ("4. Ngày sinh", self.inp_ngaysinh)
        ]))
        add_div()

        # ── Hàng 3: CCCD / CMND 
        self.inp_cccd = self._make_input("038206016228")
        self.inp_cccd_ngay = self._make_input("19/04/2024")
        self.inp_cccd_noi = self._make_input("Thanh Hoá")
        layout.addLayout(self._create_grid_row([
            ("6. CCCD/CMND", self.inp_cccd),
            ("Ngày cấp", self.inp_cccd_ngay),
            ("Nơi cấp", self.inp_cccd_noi)
        ]))
        add_div()

        # ── Hàng 4: SĐT | Email 
        self.inp_sdt = self._make_input("0375 853 601")
        self.inp_email = self._make_input("nghiand.b24vn074@stu.ptit.edu.vn")
        layout.addLayout(self._create_grid_row([
            ("7. Số điện thoại", self.inp_sdt),
            ("8. Email", self.inp_email)
        ]))
        add_div()

        # ── Hàng 5: Khoa ngành | Chuyên ngành 
        self.inp_khoaNganh = self._make_input("D24CQ - Công nghệ thông tin Việt - Nhật")
        self.inp_chuyenNganh = self._make_input("Chưa cập nhật")
        layout.addLayout(self._create_grid_row([
            ("9. Khóa ngành đào tạo", self.inp_khoaNganh),
            ("Chuyên ngành", self.inp_chuyenNganh)
        ]))
        add_div()

        self.inp_quoctich = self._make_input("Việt Nam")
        self.inp_dantoc = self._make_input("Kinh")
        self.inp_tongiao = self._make_input("Không")
        layout.addLayout(self._create_grid_row([
            ("10. Quốc tịch", self.inp_quoctich),
            ("11. Dân tộc", self.inp_dantoc),
            ("12. Tôn giáo", self.inp_tongiao)
        ]))
        add_div()

        # ── 13. Địa chỉ thường trú 
        add_section_title("13. Địa chỉ thường trú:")
        self.inp_tinh = self._make_input("Tỉnh Thanh Hóa")
        self.inp_xa = self._make_input("Xã Trường Trung")
        self.inp_diachi = self._make_input("Thôn Phượng Đoài")
        layout.addLayout(self._create_grid_row([
            ("Tỉnh/Thành phố", self.inp_tinh),
            ("Xã/Phường/Đặc khu", self.inp_xa),
            ("Địa chỉ", self.inp_diachi)
        ]))
        add_div()

        # ── 14. Đảng 
        add_section_title("14. Đảng:")
        self.inp_dang_db = self._make_input("27/08/2024")
        self.inp_dang_ct = self._make_input("27/08/2024")
        layout.addLayout(self._create_grid_row([
            ("Ngày vào Đảng dự bị", self.inp_dang_db),
            ("Ngày vào Đảng chính thức", self.inp_dang_ct)
        ]))
        add_div()

        self.inp_bhsv = self._make_input("HS4383822953565")
        self.inp_mabv = self._make_input("")
        layout.addLayout(self._create_grid_row([
            ("15. Số bảo hiểm sinh viên", self.inp_bhsv),
            ("16. Mã bệnh viện khám chữa bệnh", self.inp_mabv)
        ]))
        add_div()

        # ── 17. Tài khoản ngân hàng 
        add_section_title("17. Tài khoản ngân hàng:")
        self.inp_ngan_hang = self._make_input("MB BANK")
        self.inp_so_tk = self._make_input("25080625082006")
        layout.addLayout(self._create_grid_row([
            ("Tên ngân hàng", self.inp_ngan_hang),
            ("Số tài khoản", self.inp_so_tk)
        ]))

        # ── Nút lưu 
        layout.addSpacing(24)
        btn_row = QtWidgets.QHBoxLayout()
        self.btn_luu = QtWidgets.QPushButton("💾 Lưu thông tin")
        self.btn_luu.setObjectName("btnLuu")
        self.btn_luu.setFixedHeight(38)
        self.btn_luu.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_luu.clicked.connect(self.handle_save)
        
        btn_row.addStretch()
        btn_row.addWidget(self.btn_luu)
        layout.addLayout(btn_row)

        return col

    def _lbl(self, text: str) -> QtWidgets.QLabel:
        lbl = QtWidgets.QLabel(text)
        lbl.setProperty("class", "fieldLabel")
        return lbl

    def _make_input(self, text_value: str = "", readonly: bool = False) -> QtWidgets.QLineEdit:
        inp = QtWidgets.QLineEdit()
        inp.setProperty("class", "fieldInput")
        inp.setText(text_value)
        inp.setReadOnly(readonly)
        inp.setFixedHeight(34)
        inp.setCursorPosition(0) 
        return inp

    def handle_save(self):
        self.btn_luu.setText("✔  Da luu thanh cong!")
        self.btn_luu.setStyleSheet("background-color: #16A34A; color: white; border-radius: 6px; padding: 9px 24px; font-size: 13px; font-weight: bold;")
        QtCore.QTimer.singleShot(2000, self.reset_btn)

    def reset_btn(self):
        self.btn_luu.setText("💾  Luu thong tin")
        self.btn_luu.setStyleSheet("")


# ─── Chạy ứng dụng ──────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QtGui.QFont("Segoe UI", 10))

    window = PersonalInfoWidget()
    window.setWindowTitle("Thong tin ca nhan")
    window.resize(1280, 760)
    window.show()
    sys.exit(app.exec_())