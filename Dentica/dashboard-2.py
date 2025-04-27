import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DentalCare Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #f8fafc;")
        self.init_ui()

    def init_ui(self):
        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        # --- Sidebar ---
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("""
            background-color: #fff;
            padding: 24px;
        """)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setSpacing(20)

        logo = QLabel("DentalCare")
        logo.setFont(QFont("Inter", 20, QFont.Weight.DemiBold))
        sb_layout.addWidget(logo)

        for name in ["Dashboard", "Patients", "Appointments", "Billing", "Treatment History", "Reports"]:
            btn = QPushButton(name)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 10px;
                    background: none;
                    border: none;
                    color: #475569;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #f1f5f9;
                    border-radius: 8px;
                }
            """)
            sb_layout.addWidget(btn)

        sb_layout.addStretch()
        root_layout.addWidget(sidebar)

        # --- Main Content ---
        content = QVBoxLayout()
        content.setContentsMargins(24, 24, 24, 24)
        content.setSpacing(20)

        # Search + Notifications bar
        topbar = QHBoxLayout()
        search = QLineEdit()
        search.setPlaceholderText("Search patients…")
        search.setFixedHeight(40)
        search.setStyleSheet("""
            QLineEdit {
                background-color: #fff;
                border-radius: 8px;
                padding: 0 12px;
                font-size: 14px;
            }
        """)
        topbar.addWidget(search, 1)

        notif_btn = QPushButton("🔔 3")
        notif_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        notif_btn.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                font-size: 18px;
            }
        """)
        topbar.addWidget(notif_btn)
        content.addLayout(topbar)

        # Summary cards
        cards = QHBoxLayout()
        cards.setSpacing(20)
        def make_card(title, value):
            f = QFrame()
            f.setStyleSheet("""
                QFrame {
                    background: #fff;
                    border: 1px solid #e5e7eb;
                    border-radius: 12px;
                    padding: 20px;
                }
            """)
            l = QVBoxLayout(f)
            t = QLabel(title)
            t.setFont(QFont("Inter", 10))
            t.setStyleSheet("color: #64748b;")
            v = QLabel(str(value))
            v.setFont(QFont("Inter", 24, QFont.Weight.Bold))
            l.addWidget(t)
            l.addWidget(v)
            return f

        for title, val in [
            ("Total Patients", 156),
            ("Today's Appointments", 8),
            ("Pending Payments", 12),
            ("Completed Treatments", 45),
        ]:
            cards.addWidget(make_card(title, val))

        content.addLayout(cards)

        # Appointments & Notifications panels
        panels = QHBoxLayout()
        panels.setSpacing(20)

        # Upcoming Appointments panel
        appt_frame = QFrame()
        appt_frame.setStyleSheet("""
            QFrame {
                background: #fff;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        appt_layout = QVBoxLayout(appt_frame)
        header = QHBoxLayout()
        header.addWidget(QLabel("Upcoming Appointments"), 1)
        add_btn = QPushButton("Add Patient")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setFixedSize(120, 32)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        header.addWidget(add_btn)
        appt_layout.addLayout(header)

        table = QTableWidget(3, 5)
        table.setHorizontalHeaderLabels(["Patient", "Time", "Treatment", "Status", "Action"])
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setStyleSheet("QTableWidget { background: transparent; }")

        data = [
            ("Sarah Johnson",   "2024-02-15 10:00", "Root Canal",     "Scheduled"),
            ("Michael Chen",    "2024-02-16 14:30", "Regular Checkup","Confirmed"),
            ("Emma Davis",      "2024-02-17 11:15", "Crown Fitting",  "Waiting"),
        ]
        status_colors = {
            "Scheduled": ("#d1fae5", "#166534"),
            "Confirmed": ("#dbeafe", "#1e40af"),
            "Waiting":   ("#fee2e2", "#991b1b"),
        }

        for row, (patient, time, treatment, status) in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(patient))
            table.setItem(row, 1, QTableWidgetItem(time))
            table.setItem(row, 2, QTableWidgetItem(treatment))

            lbl = QLabel(status)
            bg, fg = status_colors[status]
            lbl.setStyleSheet(f"background:{bg}; color:{fg}; padding:4px 8px; border-radius:4px;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setCellWidget(row, 3, lbl)

            btn = QPushButton("View")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("QPushButton { color: #3b82f6; background: none; border: none; }")
            table.setCellWidget(row, 4, btn)

        appt_layout.addWidget(table)
        panels.addWidget(appt_frame, 3)

        # Recent Notifications panel
        notif_frame = QFrame()
        notif_frame.setStyleSheet("""
            QFrame {
                background: #fff;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        nf_layout = QVBoxLayout(notif_frame)
        nf_layout.addWidget(QLabel("Recent Notifications"))

        notes = [
            ("New appointment request from John Doe", "5m ago"),
            ("Payment received for Invoice #1234", "10m ago"),
            ("Reminder: Staff meeting at 3 PM", "1h ago"),
        ]
        for text, when in notes:
            row = QHBoxLayout()
            dot = QLabel()
            dot.setFixedSize(8, 8)
            dot.setStyleSheet("background-color: #3b82f6; border-radius: 4px;")
            row.addWidget(dot)
            v = QVBoxLayout()
            lbl = QLabel(text)
            lbl.setWordWrap(True)
            lbl.setStyleSheet("color:#1e293b;")
            t = QLabel(when)
            t.setStyleSheet("color:#64748b; font-size:12px;")
            v.addWidget(lbl)
            v.addWidget(t)
            row.addLayout(v)
            nf_layout.addLayout(row)

        panels.addWidget(notif_frame, 1)

        content.addLayout(panels)
        root_layout.addLayout(content, 1)

        #test pr
        #test again pr
        #test branch pr
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Dashboard()
    win.show()
    sys.exit(app.exec())
