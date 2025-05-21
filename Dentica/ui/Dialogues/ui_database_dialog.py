from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt

class Database_Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Login")
        self.setFixedSize(300, 350)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e293b;
                color: white;
                border: 1px solid #fff;
                border-radius: 5px;
            }
        """)
        self.oldPos = None

        label_style = "color: white; font-family: Inter; font-size: 14px;"
        x_label = 15
        x_input = 130
        row_height = 40
        row_start = 40

        def add_row(row, text, widget):
            y = row_start + row * row_height
            label = QtWidgets.QLabel(text, self)
            label.setGeometry(x_label, y, 110, 20)
            label.setStyleSheet(label_style)
            widget.setGeometry(x_input, y, 160, 22)

        self.username_input = QtWidgets.QLineEdit(self)
        add_row(0, "User:", self.username_input)

        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        add_row(1, "Password:", self.password_input)

        self.host_input = QtWidgets.QLineEdit(self)
        add_row(2, "Host:", self.host_input)
       
        self.dbname_input = QtWidgets.QLineEdit(self)
        add_row(4, "Database Name:", self.dbname_input)

        self.login_btn = QtWidgets.QPushButton("Login", self)
        self.login_btn.setGeometry(60, 260, 80, 30)
        self.login_btn.setStyleSheet("background-color: #37547A; color: #fff;")

        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(150, 260, 80, 30)
        self.cancel_btn.setStyleSheet("""
            QPushButton {background-color: #37547A; color: #fff;}
            QPushButton:hover {background-color: #fff; color: #000;}
        """)
        self.cancel_btn.clicked.connect(self.reject)
        
        
        
        

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

