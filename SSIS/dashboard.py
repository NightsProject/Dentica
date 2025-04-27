import sys
from PyQt6 import QtCore, QtGui, QtWidgets

class DashboardWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dentica Dashboard")
        self.resize(1200, 800)

        # Central widget and main layout
        centralWidget = QtWidgets.QWidget()
        centralWidget.setObjectName("central")
        self.setCentralWidget(centralWidget)
        mainLayout = QtWidgets.QHBoxLayout(centralWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # Sidebar
        sidebar = QtWidgets.QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(280)
        sidebarLayout = QtWidgets.QVBoxLayout(sidebar)
        sidebarLayout.setContentsMargins(24, 24, 24, 24)
        sidebarLayout.setSpacing(0)

        # Logo and brand name
        logo = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("path/to/logo.png").scaled(40, 40, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setObjectName("logo")
        sidebarLayout.addWidget(logo, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        sidebarLayout.addSpacing(16)

        brand = QtWidgets.QLabel("Dentica")
        brand.setObjectName("brandName")
        brand.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        sidebarLayout.addWidget(brand)
        sidebarLayout.addSpacing(40)

        # Navigation links
        navLinks = QtWidgets.QVBoxLayout()
        navLinks.setSpacing(8)
        for name in ["Dashboard", "Patients", "Appointments", "Billing", "Reports"]:
            btn = QtWidgets.QPushButton(name)
            btn.setObjectName("navItem")
            btn.setFlat(True)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            navLinks.addWidget(btn)
        sidebarLayout.addLayout(navLinks)
        sidebarLayout.addStretch()

        mainLayout.addWidget(sidebar)

        # Main content area
        mainContent = QtWidgets.QFrame()
        mainContent.setObjectName("mainContent")
        contentLayout = QtWidgets.QVBoxLayout(mainContent)
        contentLayout.setContentsMargins(24, 24, 24, 24)
        contentLayout.setSpacing(24)

        # Header
        header = QtWidgets.QFrame()
        header.setObjectName("header")
        headerLayout = QtWidgets.QHBoxLayout(header)
        headerLayout.setContentsMargins(0, 0, 0, 0)
        headerLayout.setSpacing(16)

        searchContainer = QtWidgets.QFrame()
        searchContainer.setObjectName("searchContainer")
        scLayout = QtWidgets.QHBoxLayout(searchContainer)
        scLayout.setContentsMargins(12, 8, 12, 8)
        scLayout.setSpacing(8)
        searchIcon = QtWidgets.QLabel()
        searchIcon.setPixmap(QtGui.QPixmap("path/to/search-icon.png").scaled(20, 20, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        searchIcon.setObjectName("searchIcon")
        scLayout.addWidget(searchIcon)
        searchInput = QtWidgets.QLineEdit()
        searchInput.setPlaceholderText("Search patients...")
        searchInput.setObjectName("searchInput")
        scLayout.addWidget(searchInput)
        headerLayout.addWidget(searchContainer)
        headerLayout.addStretch()

        notifBtn = QtWidgets.QFrame()
        notifBtn.setObjectName("notificationContainer")
        nbLayout = QtWidgets.QHBoxLayout(notifBtn)
        nbLayout.setContentsMargins(0, 0, 0, 0)
        notifIcon = QtWidgets.QLabel()
        notifIcon.setPixmap(QtGui.QPixmap("path/to/bell-icon.png").scaled(24, 24, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        notifIcon.setObjectName("notificationIcon")
        nbLayout.addWidget(notifIcon)
        badge = QtWidgets.QLabel("3")
        badge.setObjectName("notificationBadge")
        nbLayout.addWidget(badge, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        headerLayout.addWidget(notifBtn)

        profilePic = QtWidgets.QLabel()
        pixmap2 = QtGui.QPixmap("path/to/profile.png").scaled(32, 32, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        profilePic.setPixmap(pixmap2)
        profilePic.setObjectName("profilePic")
        headerLayout.addWidget(profilePic)

        contentLayout.addWidget(header)

        # Stats grid
        statsGrid = QtWidgets.QHBoxLayout()
        statsGrid.setSpacing(24)
        stats = [
            ("Total Patients", "156"),
            ("Today's Appointments", "8"),
            ("Pending Payments", "12"),
            ("Completed Treatments", "45")
        ]
        for title, value in stats:
            card = QtWidgets.QFrame()
            card.setObjectName("statCard")
            cardLayout = QtWidgets.QVBoxLayout(card)
            cardLayout.setContentsMargins(16, 16, 16, 16)
            cardLayout.setSpacing(8)
            lblTitle = QtWidgets.QLabel(title)
            lblTitle.setObjectName("statTitle")
            lblValue = QtWidgets.QLabel(value)
            lblValue.setObjectName("statValue")
            cardLayout.addWidget(lblTitle)
            cardLayout.addWidget(lblValue)
            statsGrid.addWidget(card)
        contentLayout.addLayout(statsGrid)

        # Appointments section
        appSection = QtWidgets.QFrame()
        appSection.setObjectName("appointmentsSection")
        appLayout = QtWidgets.QVBoxLayout(appSection)
        appLayout.setContentsMargins(24, 24, 24, 24)
        appLayout.setSpacing(16)

        sectionHeader = QtWidgets.QFrame()
        sectionHeader.setObjectName("sectionHeader")
        shLayout = QtWidgets.QHBoxLayout(sectionHeader)
        shLayout.setContentsMargins(0, 0, 0, 0)
        shLayout.setSpacing(16)
        sectionTitle = QtWidgets.QLabel("Upcoming Appointments")
        sectionTitle.setObjectName("sectionTitle")
        shLayout.addWidget(sectionTitle)
        shLayout.addStretch()
        addBtn = QtWidgets.QPushButton("Add Patient")
        addBtn.setObjectName("addPatientBtn")
        addBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        shLayout.addWidget(addBtn)
        appLayout.addWidget(sectionHeader)

        table = QtWidgets.QTableWidget(3, 5)
        table.setObjectName("appointmentsTable")
        table.setHorizontalHeaderLabels(["Patient", "Time", "Treatment", "Status", "Action"])
        appointments = [
            ("Sarah Johnson\nAge: 34", "2024-02-15 10:00", "Root Canal", "Scheduled", "View Details"),
            ("Michael Chen\nAge: 28", "2024-02-16 14:30", "Regular Checkup", "Confirmed", "View Details"),
            ("Emma Davis\nAge: 45", "2024-02-17 11:15", "Crown Fitting", "Waiting", "View Details")
        ]
        for r, data in enumerate(appointments):
            for c, item in enumerate(data):
                table.setItem(r, c, QtWidgets.QTableWidgetItem(item))
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        appLayout.addWidget(table)
        contentLayout.addWidget(appSection)

        # Notifications panel
        notifPanel = QtWidgets.QFrame()
        notifPanel.setObjectName("notificationsPanel")
        notifLayout = QtWidgets.QVBoxLayout(notifPanel)
        notifLayout.setContentsMargins(24, 24, 24, 24)
        notifLayout.setSpacing(16)
        notifLayout.addWidget(QtWidgets.QLabel("Recent Notifications"))

        items = [
            ("", "New appointment request from John Doe", "5m ago"),
            ("", "Payment received for Invoice #1234", "10m ago"),
            ("", "Reminder: Staff meeting at 3 PM", "1h ago")
        ]
        for _, text, time in items:
            row = QtWidgets.QHBoxLayout()
            dot = QtWidgets.QFrame()
            dot.setObjectName("notificationDot")
            dot.setFixedSize(8, 8)
            row.addWidget(dot)
            row.addWidget(QtWidgets.QLabel(text))
            row.addStretch()
            row.addWidget(QtWidgets.QLabel(time))
            notifLayout.addLayout(row)
        contentLayout.addWidget(notifPanel)
        contentLayout.addStretch()

        mainLayout.addWidget(mainContent)

        # Global stylesheet
        self.setStyleSheet("""
            * { margin:0; padding:0; box-sizing:border-box; }
            QWidget#central { background-color:#f8fafc; font-family: 'Inter'; }
            QFrame#sidebar { background-color:#fff; border-right:1px solid #e5e7eb; }
            QLabel#logo { }
            QLabel#brandName { font-size:20px; font-weight:600; color:#1e293b; margin-bottom:40px; }
            QPushButton#navItem { color:#475569; font-size:16px; text-align:left; padding:12px 0; background:none; border:none; }
            QPushButton#navItem:hover { background-color:#f1f5f9; }
            QFrame#mainContent { background-color:#f8fafc; }
            QFrame#header { background-color:#fff; }
            QFrame#searchContainer { background-color:#f1f5f9; border-radius:8px; }
            QLabel#searchIcon { margin-left:12px; }
            QLineEdit#searchInput { background:none; border:none; outline:none; font-size:14px; color:#1e293b; }
            QFrame#notificationContainer { position:relative; }
            QLabel#notificationIcon { }
            QLabel#notificationBadge { background-color:#ef4444; color:#fff; border-radius:10px; font-size:12px; min-width:20px; min-height:20px; text-align:center; }
            QLabel#profilePic { border-radius:16px; }
            QFrame#statCard { background-color:#fff; border:1px solid #e5e7eb; border-radius:12px; }
            QLabel#statTitle { font-size:14px; color:#64748b; margin-bottom:8px; }
            QLabel#statValue { font-size:24px; font-weight:600; color:#1e293b; }
            QFrame#appointmentsSection { background-color:#fff; border:1px solid #e5e7eb; border-radius:12px; }
            QLabel#sectionTitle { font-size:18px; font-weight:600; color:#1e293b; }
            QPushButton#addPatientBtn { background-color:#3b82f6; color:#fff; padding:8px 16px; border:none; border-radius:8px; }
            QTableWidget#appointmentsTable { background-color:none; }
            QTableWidget::item { font-size:14px; color:#1e293b; }
            QFrame#notificationsPanel { background-color:#fff; border:1px solid #e5e7eb; border-radius:12px; }
            QFrame#notificationDot { background-color:#3b82f6; border-radius:4px; }
            QLabel { font-family:'Inter'; }
        """)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()