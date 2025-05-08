from PyQt6 import QtWidgets

class Database_Login(QtWidgets.QDialog):
 
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
        
        self.port_label = QtWidgets.QLabel("Port:", self)
        self.port_label.setGeometry(20, 160, 80, 20)

        self.port_input = QtWidgets.QLineEdit(self)
        self.port_input.setGeometry(110, 160, 160, 22)

        self.dbname_label = QtWidgets.QLabel("Database Name:", self)
        self.dbname_label.setGeometry(20, 200, 90, 20)

        self.dbname_input = QtWidgets.QLineEdit(self)
        self.dbname_input.setGeometry(110, 200, 160, 22)
        
        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(160, 240, 80, 30)
        self.cancel_btn.clicked.connect(self.reject)
        
        self.login_btn = QtWidgets.QPushButton("Login", self)
        self.login_btn.setGeometry(80, 240, 80, 30)
        
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
              
class Add_Appointment(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Appointment")
        self.setFixedSize(300, 400)
        self.setStyleSheet("background-color: #1e293b; color: white;")

        self.appointment_id = QtWidgets.QLabel("Appointment ID:", self)
        self.appointment_id.setGeometry(20, 40, 80, 20)

        self.appointment_input = QtWidgets.QLineEdit(self)
        self.appointment_input.setGeometry(110, 40, 160, 22)

        self.patient_id = QtWidgets.QLabel("Patient ID:", self)
        self.patient_id.setGeometry(20, 80, 80, 20)

        self.patient_input = QtWidgets.QLineEdit(self)
        self.patient_input.setGeometry(110, 80, 160, 22)
        self.patient_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.schedule = QtWidgets.QLabel("Schedule:", self)
        self.schedule.setGeometry(20, 120, 80, 20)

        self.schedule_input = QtWidgets.QLineEdit(self)
        self.schedule_input.setGeometry(110, 120, 160, 22)
        
        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(160, 240, 80, 30)
        self.cancel_btn.clicked.connect(self.reject)
        
        self.login_btn = QtWidgets.QPushButton("Add", self)
        self.login_btn.setGeometry(80, 240, 80, 30)
        


