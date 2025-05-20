from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
class Exit_App(QtWidgets.QDialog):
 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Confirm Exit")
        self.setFixedSize(400, 100)
        self.setStyleSheet("""
            QDialog {
                background-color: #B2CDE9;
                border: 1px solid #fff;
                border-radius: 5px;
            }
        """)

        self.username_label = QtWidgets.QLabel("Are you sure you want to exit the app?", self)
        self.username_label.setStyleSheet("color: #37547A; font-family: Inter; font-size: 18px;")
        self.username_label.setGeometry(40, 20, 350, 20)
        
        self.yes_btn = QtWidgets.QPushButton("Yes", self)
        self.yes_btn.setGeometry(110, 60, 80, 30)
        self.yes_btn.setStyleSheet("""
            QPushButton {background-color: #37547A; color: #fff;}
            QPushButton:hover {background-color: #fff; color: #000;}
        """)
        self.yes_btn.clicked.connect(self.accept)
        
        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(210, 60, 80, 30)
        self.cancel_btn.setStyleSheet("""
            QPushButton {background-color: #37547A; color: #fff;}
            QPushButton:hover {background-color: #fff; color: #000;}
        """)
        self.cancel_btn.clicked.connect(self.reject)
