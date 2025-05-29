from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt
filepath = "Dentica/ui/icons/"

class Database_Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowSystemMenuHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setWindowTitle("Login")
        self.setFixedSize(400, 480)
        self.setStyleSheet("""
            QDialog {
                background-color: transparent;
                border-radius: 15px;
            }
        """)
        self.oldPos = None

        # Container box for modern card style
        self.container = QtWidgets.QWidget(self)
        self.container.setGeometry(20, 20, 360, 440)
        self.container.setStyleSheet("""
            background-color: #B2CDE9;
            border-radius: 15px;
            border: none;
        """)
        # Add drop shadow effect 
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QtGui.QColor(0, 0, 0, 60))
        self.container.setGraphicsEffect(shadow)

        # Dentica Icon
        self.DenticaIcon = QtWidgets.QLabel(parent = self.container)
        self.DenticaIcon.setGeometry(QtCore.QRect(70, 12, 60, 60))
        dent_icon = QtGui.QIcon(f"{filepath}Dentica_blue.svg")
        pixmap = dent_icon.pixmap(60,60)
        self.DenticaIcon.setPixmap(pixmap)
        
        # Title label
        self.title_label = QtWidgets.QLabel("Dentica", self.container)
        self.title_label.setGeometry(130, 20, 150, 40)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Katarine")
        font.setBold(True)
        self.title_label.setStyleSheet("""
            font-family: Katarine;
            font-weight: 700;
            font-size: 40px;
            color: #1e293b;
        """)

        # Subtitle label
        self.subtitle_label = QtWidgets.QLabel("Please login to your database account", self.container)
        self.subtitle_label.setGeometry(20, 85, 320, 20)
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setStyleSheet("""
            font-family: 'Inter', sans-serif;
            font-weight: 400;
            font-size: 14px;
            color: #64748b;
        """)

        label_style = """
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            font-weight: 600;
            color: #475569;
        """
        input_style = """
            QLineEdit {
                border: none;
                border-radius: 10px;
                padding-left: 15px;
                padding-top: 6px;
                padding-bottom: 6px;
                font-family: 'Inter', sans-serif;
                font-size: 14px;
                color: #334155;
                background-color: #f8fafc;
            }
            QLineEdit:focus {
                border: none;
                background-color: #ffffff;
                color: #1e293b;
                /* Using a solid border on focus for clarity */
                border: 2px solid #3b82f6;
            }
        """

        x_label = 22
        x_input = 130
        row_height = 45
        row_start = 115

        def add_row(row, text, widget):
            y = row_start + row * row_height
            label = QtWidgets.QLabel(text, self.container)
            label.setGeometry(x_label, y+7, 105, 20)  # adjusted vertical center with input
            label.setStyleSheet(label_style)
            widget.setParent(self.container)
            widget.setGeometry(x_input, y, 195, 30)
            widget.setStyleSheet(input_style)

        self.username_input = QtWidgets.QLineEdit()
        add_row(0, "User:", self.username_input)

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        add_row(1, "Password:", self.password_input)

        self.host_input = QtWidgets.QLineEdit()
        add_row(2, "Host:", self.host_input)

        self.port_input = QtWidgets.QLineEdit()
        add_row(3, "Port:", self.port_input)

        self.dbname_input = QtWidgets.QLineEdit()
        add_row(4, "Database Name:", self.dbname_input)

        self.login_btn = QtWidgets.QPushButton("Login", self.container)
        self.login_btn.setGeometry(65, 350, 110, 40)
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-weight: 600;
                font-family: 'Inter', sans-serif;
                font-size: 16px;
                border-radius: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1e40af;
            }
            QPushButton:pressed {
                background-color: #1e3a8a;
            }
            """)

        self.cancel_btn = QtWidgets.QPushButton("Cancel", self.container)
        self.cancel_btn.setGeometry(185, 350, 110, 40)
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e2e8f0;
                color: #475569;
                font-weight: 600;
                font-family: 'Inter', sans-serif;
                font-size: 16px;
                border-radius: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #cbd5e1;
                color: #1e293b;
            }
            QPushButton:pressed {
                background-color: #94a3b8;
            }
        """)

        # For demonstration/testing preset values
        self.host_input.setText("localhost")
        self.port_input.setText("3306")
        self.dbname_input.setText("denticadb")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.oldPos:
            delta = event.globalPosition().toPoint() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.oldPos = None

