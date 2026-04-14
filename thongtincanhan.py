from PyQt5 import QtCore, QtGui, QtWidgets


class PersonalInfoWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
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
                background-color: #C81E1E;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 18px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton#btnCapNhat:hover { background-color: #A41616; }

            QPushButton.outlineBtn {
                background-color: white;
                color: #374151;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 8px 18px;
                font-size: 13px;
            }
            QPushButton.outlineBtn:hover { background-color: #F3F4F6; }

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

            /* Label tên trường */
            QLabel.fieldLabel {
                font-size: 12px;
                color: #6B7280;
                font-weight: bold;
            }
            /* Ô nhập liệu */
            QLineEdit.fieldInput {
                border: 1px solid #E5E7EB;
                border-radius: 6px;
                padding: 7px 10px;
                font-size: 13px;
                color: #111827;
                background-color: white;
            }
            QLineEdit.fieldInput:focus {
                border: 1.5px solid #C81E1E;
                background-color: #FFFAFA;
            }
            QLineEdit.fieldInput:read-only {
                background-color: #F9FAFB;
                color: #9CA3AF;
            }
            /* Section title (13, Địa chỉ...) */
            QLabel.sectionLabel {
                font-size: 13px;
                font-weight: bold;
                color: #111827;
            }
            QFrame.divider {
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
        """)
        self.setup_ui()

    def setup_ui(self):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_header())
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

    # ── Header ───────────────────────────────────────────────────
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

    # ── Action bar ───────────────────────────────────────────────
    def _build_action_bar(self):
        bar = QtWidgets.QWidget()
        bar.setStyleSheet("background:white; border-bottom:1px solid #E5E7EB;")
        bar.setFixedHeight(52)
        layout = QtWidgets.QHBoxLayout(bar)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(10)

        btn1 = QtWidgets.QPushButton("✏  Cap nhat ho so")
        btn1.setObjectName("btnCapNhat")
        btn1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        layout.addWidget(btn1)

        for label in ["📄  Hoc ba so", "📷  Cap nhat anh"]:
            btn = QtWidgets.QPushButton(label)
            btn.setProperty("class", "outlineBtn")
            btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            layout.addWidget(btn)

        layout.addStretch()
        return bar

    # ── Main card ────────────────────────────────────────────────
    def _build_main_card(self):
        frame = QtWidgets.QFrame()
        frame.setObjectName("mainCard")

        outer = QtWidgets.QVBoxLayout(frame)
        outer.setContentsMargins(32, 28, 32, 32)
        outer.setSpacing(20)

        title = QtWidgets.QLabel("SO YEU LY LICH")
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

    # ── Cột form nhập liệu ───────────────────────────────────────
    def _build_form_col(self):
        col = QtWidgets.QWidget()
        col.setStyleSheet("background:transparent;")
        layout = QtWidgets.QVBoxLayout(col)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        def div():
            sep = QtWidgets.QFrame()
            sep.setFrameShape(QtWidgets.QFrame.HLine)
            sep.setProperty("class", "divider")
            sep.setContentsMargins(0, 4, 0, 4)
            return sep

        # ── Hàng 1: Mã SV | Họ tên | Trạng thái ────────────────
        g1 = QtWidgets.QGridLayout()
        g1.setContentsMargins(0, 8, 0, 8)
        g1.setSpacing(12)
        self.inp_masv      = self._make_input("VD: B24DCVN012", readonly=True)
        self.inp_hoten     = self._make_input("Nguyen Van A")
        self.inp_trangthai = self._make_input("Dang hoc / Bao luu...")
        g1.addWidget(self._lbl("1. Ma sinh vien"),    0, 0)
        g1.addWidget(self.inp_masv,                   1, 0)
        g1.addWidget(self._lbl("2. Ho va ten"),       0, 1)
        g1.addWidget(self.inp_hoten,                  1, 1)
        g1.addWidget(self._lbl("5. Trang thai hoc"),  0, 2)
        g1.addWidget(self.inp_trangthai,              1, 2)
        layout.addLayout(g1)
        layout.addWidget(div())

        # ── Hàng 2: Giới tính | Ngày sinh ───────────────────────
        g2 = QtWidgets.QGridLayout()
        g2.setContentsMargins(0, 8, 0, 8)
        g2.setSpacing(12)
        self.inp_gioitinh  = self._make_input("Nam / Nu")
        self.inp_ngaysinh  = self._make_input("DD/MM/YYYY")
        g2.addWidget(self._lbl("3. Gioi tinh"),  0, 0)
        g2.addWidget(self.inp_gioitinh,          1, 0)
        g2.addWidget(self._lbl("4. Ngay sinh"),  0, 1)
        g2.addWidget(self.inp_ngaysinh,          1, 1)
        g2.setColumnStretch(1, 2)
        layout.addLayout(g2)
        layout.addWidget(div())

        # ── Hàng 3: CCCD / CMND ──────────────────────────────────
        g3 = QtWidgets.QGridLayout()
        g3.setContentsMargins(0, 8, 0, 8)
        g3.setSpacing(12)
        self.inp_cccd      = self._make_input("So CCCD/CMND")
        self.inp_cccd_ngay = self._make_input("Ngay cap (DD/MM/YYYY)")
        self.inp_cccd_noi  = self._make_input("Noi cap")
        g3.addWidget(self._lbl("6. CCCD/CMND"),  0, 0)
        g3.addWidget(self.inp_cccd,              1, 0)
        g3.addWidget(self._lbl("Ngay cap"),      0, 1)
        g3.addWidget(self.inp_cccd_ngay,         1, 1)
        g3.addWidget(self._lbl("Noi cap"),       0, 2)
        g3.addWidget(self.inp_cccd_noi,          1, 2)
        layout.addLayout(g3)
        layout.addWidget(div())

        # ── Hàng 4: SĐT | Email ──────────────────────────────────
        g4 = QtWidgets.QGridLayout()
        g4.setContentsMargins(0, 8, 0, 8)
        g4.setSpacing(12)
        self.inp_sdt   = self._make_input("0xxx xxx xxx")
        self.inp_email = self._make_input("example@ptit.edu.vn")
        g4.addWidget(self._lbl("7. So dien thoai"),  0, 0)
        g4.addWidget(self.inp_sdt,                   1, 0)
        g4.addWidget(self._lbl("8. Email"),           0, 1)
        g4.addWidget(self.inp_email,                  1, 1)
        layout.addLayout(g4)
        layout.addWidget(div())

        # ── Hàng 5: Khoa ngành | Chuyên ngành ───────────────────
        g5 = QtWidgets.QGridLayout()
        g5.setContentsMargins(0, 8, 0, 8)
        g5.setSpacing(12)
        self.inp_khoaNganh    = self._make_input("Ma lop - Ten khoa nganh")
        self.inp_chuyenNganh  = self._make_input("Ten chuyen nganh")
        g5.addWidget(self._lbl("9. Khoa nganh dao tao"),  0, 0)
        g5.addWidget(self.inp_khoaNganh,                  1, 0, 1, 2)
        g5.addWidget(self._lbl("Chuyen nganh"),           0, 2)
        g5.addWidget(self.inp_chuyenNganh,                1, 2)
        layout.addLayout(g5)
        layout.addWidget(div())

        # ── Hàng 6: Quốc tịch | Dân tộc | Tôn giáo ─────────────
        g6 = QtWidgets.QGridLayout()
        g6.setContentsMargins(0, 8, 0, 8)
        g6.setSpacing(12)
        self.inp_quoctich = self._make_input("Viet Nam...")
        self.inp_dantoc   = self._make_input("Kinh...")
        self.inp_tongiao  = self._make_input("Khong / Co")
        g6.addWidget(self._lbl("10. Quoc tich"),  0, 0)
        g6.addWidget(self.inp_quoctich,           1, 0)
        g6.addWidget(self._lbl("11. Dan toc"),    0, 1)
        g6.addWidget(self.inp_dantoc,             1, 1)
        g6.addWidget(self._lbl("12. Ton giao"),   0, 2)
        g6.addWidget(self.inp_tongiao,            1, 2)
        layout.addLayout(g6)
        layout.addWidget(div())

        # ── Địa chỉ thường trú ───────────────────────────────────
        sec13 = QtWidgets.QLabel("13. Dia chi thuong tru:")
        sec13.setProperty("class", "sectionLabel")
        sec13.setContentsMargins(0, 8, 0, 6)
        layout.addWidget(sec13)

        g7 = QtWidgets.QGridLayout()
        g7.setContentsMargins(12, 0, 0, 8)
        g7.setSpacing(12)
        self.inp_tinh   = self._make_input("Tinh / Thanh pho")
        self.inp_xa     = self._make_input("Xa / Phuong / Dac khu")
        self.inp_diachi = self._make_input("So nha, duong, thon...")
        g7.addWidget(self._lbl("Tinh/Thanh pho"),       0, 0)
        g7.addWidget(self.inp_tinh,                     1, 0)
        g7.addWidget(self._lbl("Xa/Phuong/Dac khu"),    0, 1)
        g7.addWidget(self.inp_xa,                       1, 1)
        g7.addWidget(self._lbl("Dia chi cu the"),       0, 2)
        g7.addWidget(self.inp_diachi,                   1, 2)
        layout.addLayout(g7)
        layout.addWidget(div())

        # ── Đảng ─────────────────────────────────────────────────
        sec14 = QtWidgets.QLabel("14. Dang:")
        sec14.setProperty("class", "sectionLabel")
        sec14.setContentsMargins(0, 8, 0, 6)
        layout.addWidget(sec14)

        g8 = QtWidgets.QGridLayout()
        g8.setContentsMargins(12, 0, 0, 8)
        g8.setSpacing(12)
        self.inp_dang_db = self._make_input("DD/MM/YYYY")
        self.inp_dang_ct = self._make_input("DD/MM/YYYY")
        g8.addWidget(self._lbl("Ngay vao Dang du bi"),      0, 0)
        g8.addWidget(self.inp_dang_db,                      1, 0)
        g8.addWidget(self._lbl("Ngay vao Dang chinh thuc"), 0, 1)
        g8.addWidget(self.inp_dang_ct,                      1, 1)
        layout.addLayout(g8)
        layout.addWidget(div())

        # ── Bảo hiểm | Mã bệnh viện ──────────────────────────────
        g9 = QtWidgets.QGridLayout()
        g9.setContentsMargins(0, 8, 0, 8)
        g9.setSpacing(12)
        self.inp_bhsv  = self._make_input("HS...")
        self.inp_mabv  = self._make_input("BV...")
        g9.addWidget(self._lbl("15. So bao hiem sinh vien"),        0, 0)
        g9.addWidget(self.inp_bhsv,                                 1, 0)
        g9.addWidget(self._lbl("16. Ma benh vien kham chua benh"),  0, 1)
        g9.addWidget(self.inp_mabv,                                 1, 1)
        layout.addLayout(g9)
        layout.addWidget(div())

        # ── Tài khoản ngân hàng ───────────────────────────────────
        sec17 = QtWidgets.QLabel("17. Tai khoan ngan hang:")
        sec17.setProperty("class", "sectionLabel")
        sec17.setContentsMargins(0, 8, 0, 6)
        layout.addWidget(sec17)

        g10 = QtWidgets.QGridLayout()
        g10.setContentsMargins(12, 0, 0, 8)
        g10.setSpacing(12)
        self.inp_ngan_hang = self._make_input("MB Bank / Vietcombank...")
        self.inp_so_tk     = self._make_input("So tai khoan")
        g10.addWidget(self._lbl("Ten ngan hang"),  0, 0)
        g10.addWidget(self.inp_ngan_hang,          1, 0)
        g10.addWidget(self._lbl("So tai khoan"),   0, 1)
        g10.addWidget(self.inp_so_tk,              1, 1)
        layout.addLayout(g10)

        # ── Nút lưu ──────────────────────────────────────────────
        layout.addSpacing(16)
        btn_row = QtWidgets.QHBoxLayout()
        self.btn_luu = QtWidgets.QPushButton("💾  Luu thong tin")
        self.btn_luu.setObjectName("btnLuu")
        self.btn_luu.setFixedHeight(38)
        self.btn_luu.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_luu.clicked.connect(self.handle_save)
        btn_row.addWidget(self.btn_luu)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        return col

    # ── Helpers ──────────────────────────────────────────────────
    def _lbl(self, text: str) -> QtWidgets.QLabel:
        lbl = QtWidgets.QLabel(text)
        lbl.setProperty("class", "fieldLabel")
        return lbl

    def _make_input(self, placeholder: str = "", readonly: bool = False) -> QtWidgets.QLineEdit:
        inp = QtWidgets.QLineEdit()
        inp.setProperty("class", "fieldInput")
        inp.setPlaceholderText(placeholder)
        inp.setReadOnly(readonly)
        inp.setFixedHeight(34)
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