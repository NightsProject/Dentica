from PyQt6 import QtWidgets

class User_Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setFixedSize(300, 400)
        self.setStyleSheet("background-color: #1e293b; color: white;")

        self.user_label = QtWidgets.QLabel("Username:", self)
        self.user_label.setGeometry(20, 40, 80, 20)

        self.user_input = QtWidgets.QLineEdit(self)
        self.user_input.setGeometry(110, 40, 160, 22)

        self.pass_label = QtWidgets.QLabel("Password:", self)
        self.pass_label.setGeometry(20, 80, 80, 20)

        self.pass_input = QtWidgets.QLineEdit(self)
        self.pass_input.setGeometry(110, 80, 160, 22)
        self.pass_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        
        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(160, 240, 80, 30)
        self.cancel_btn.clicked.connect(self.reject)
        
        self.log_btn = QtWidgets.QPushButton("Login", self)
        self.log_btn.setGeometry(80, 240, 80, 30)