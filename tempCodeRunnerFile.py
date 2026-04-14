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