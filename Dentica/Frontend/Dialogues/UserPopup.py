from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import pyqtSignal

class LoginPopup(QtWidgets.QDialog):
    
    credentialsSubmitted = pyqtSignal(str, str, str, str)

    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setFixedSize(300, 400)
        self.setStyleSheet("background-color: #1e293b; color: white;")

        self.username_label = QtWidgets.QLabel("User:", self)
        self.username_label.setGeometry(20, 40, 80, 20)

        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setGeometry(110, 40, 160, 22)

        self.password_label = QtWidgets.QLabel("Password:", self)
        self.password_label.setGeometry(20, 80, 80, 20)

        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setGeometry(110, 80, 160, 22)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.host_label = QtWidgets.QLabel("Host:", self)
        self.host_label.setGeometry(20, 120, 80, 20)

        self.host_input = QtWidgets.QLineEdit(self)
        self.host_input.setGeometry(110, 120, 160, 22)

        self.dbname_label = QtWidgets.QLabel("Database Name:", self)
        self.dbname_label.setGeometry(20, 160, 90, 20)

        self.dbname_input = QtWidgets.QLineEdit(self)
        self.dbname_input.setGeometry(110, 160, 160, 22)
        
        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(160, 210, 80, 30)
        self.cancel_btn.clicked.connect(self.reject)
        
        self.login_btn = QtWidgets.QPushButton("Login", self)
        self.login_btn.setGeometry(110, 210, 80, 30)
        self.login_btn.clicked.connect(self.on_login_pressed)
        
        
        
    def on_login_pressed(self):
        host = self.host_input.text()
        user = self.username_input.text()
        password = self.password_input.text()
        databaseName = self.dbname_input.text()
        
        # Emit the signal with the entered credentials
        self.credentialsSubmitted.emit(host, user, password, databaseName)
        
        #ToDO
        #notify in the login panel for succesful or failed connection
        #database created succesfully if not exists
        
        self.accept()
            


