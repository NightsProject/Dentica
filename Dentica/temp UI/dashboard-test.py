import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTableWidget, QTableWidgetItem, QLabel, QPushButton,
                             QLineEdit, QGroupBox, QListWidget, QSpacerItem,
                             QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor  # Import QColor for background colors


class DentalCareDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("DentalCare")
        self.setGeometry(100, 100, 1200, 800)

        # Main Layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        sidebar = QVBoxLayout()
        sidebar.setSpacing(20)

        sidebar.addWidget(QLabel("Dashboard"))
        sidebar.addWidget(QLabel("Patients"))
        sidebar.addWidget(QLabel("Appointments"))
        sidebar.addWidget(QLabel("Billing"))
        sidebar.addWidget(QLabel("Treatment History"))
        sidebar.addWidget(QLabel("Reports"))
        sidebar.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        main_layout.addLayout(sidebar)

        # Main Content
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Search Bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search patients...")
        content_layout.addWidget(search_bar)

        # Statistics
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        stats_layout.addWidget(self.createStatBox("Total Patients", "156"))
        stats_layout.addWidget(self.createStatBox("Today's Appointments", "8"))
        stats_layout.addWidget(self.createStatBox("Pending Payments", "12"))
        stats_layout.addWidget(self.createStatBox("Completed Treatments", "45"))

        content_layout.addLayout(stats_layout)

        # Upcoming Appointments
        appointments_group = QGroupBox("Upcoming Appointments")
        appointments_layout = QVBoxLayout()

        sample_data = [
            ["Sarah John\n(34)", "2024-02-15 10:00", "Root Canal", "Scheduled", "View Details"],
            ["Michael Chen\n(28)", "2024-02-16 14:30", "Regular Checkup", "Confirmed", "View Details"],
            ["Emma Davis\n(25)", "2024-02-17 11:15", "Crown Fitting", "Waiting", "View Details"]
        ]

        self.appointments_table = QTableWidget(len(sample_data), 5)  # Dynamically set rows
        self.appointments_table.setHorizontalHeaderLabels(["Patient", "Time", "Treatment", "Status", "Action"])

        for i, data in enumerate(sample_data):
            for j, item in enumerate(data):
                table_item = QTableWidgetItem(item)
                if j == 3:  # Status column
                    if "Scheduled" in item:
                        table_item.setBackground(QColor("green"))
                    elif "Confirmed" in item:
                        table_item.setBackground(QColor("yellow"))
                    elif "Waiting" in item:
                        table_item.setBackground(QColor("red"))
                self.appointments_table.setItem(i, j, table_item)

        appointments_layout.addWidget(self.appointments_table)

        add_patient_button = QPushButton("Add Patient")
        add_patient_button.setToolTip("Click to add a new patient")  # Add tooltip
        appointments_layout.addWidget(add_patient_button)
        appointments_group.setLayout(appointments_layout)
        content_layout.addWidget(appointments_group)

        # Recent Notifications
        notifications_group = QGroupBox("Recent Notifications")
        notifications_layout = QVBoxLayout()

        notifications_list = QListWidget()
        notifications = [
            "New appointment request from John Doe",
            "Payment received for Invoice #1234",
            "Reminder: Staff meeting at 3 PM"
        ]
        notifications_list.addItems(notifications)

        notifications_layout.addWidget(notifications_list)
        notifications_group.setLayout(notifications_layout)
        content_layout.addWidget(notifications_group)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        # Apply QSS Stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                font-family: 'Arial';
                color: #333;
            }
            QLabel {
                font-size: 16px;
                margin: 5px;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QGroupBox {
                font-size: 18px;
                margin-top: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
            }
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)

    def createStatBox(self, title, value):
        """Helper function to create a statistics box."""
        stat_box_layout = QVBoxLayout()
        stat_box_layout.addWidget(QLabel(title))
        stat_box_layout.addWidget(QLabel(value))

        # Wrap the layout in a QWidget
        stat_box_widget = QWidget()
        stat_box_widget.setLayout(stat_box_layout)
        return stat_box_widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = DentalCareDashboard()
    dashboard.show()
    sys.exit(app.exec())