from PyQt6 import QtWidgets


class Add_Patient(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Patient")
        self.setFixedSize(300, 400)
        self.setStyleSheet("background-color: #1e293b; color: white;")

        self.patient_id = QtWidgets.QLabel("Patient ID:", self)
        self.patient_id.setGeometry(20, 40, 80, 20)

        self.patient_input = QtWidgets.QLineEdit(self)
        self.patient_input.setGeometry(110, 40, 160, 22)

        self.first_name = QtWidgets.QLabel("First Name:", self)
        self.first_name.setGeometry(20, 80, 80, 20)

        self.first_input = QtWidgets.QLineEdit(self)
        self.first_input.setGeometry(110, 80, 160, 22)
        
        self.middle_name = QtWidgets.QLabel("Middle Name:",self)
        self.middle_name.setGeometry(20,120,80,20)

        self.middle_input = QtWidgets.QLineEdit(self)
        self.middle_input.setGeometry(110,120,160,22)

        self.last_name = QtWidgets.QLabel("Last Name:", self)
        self.last_name.setGeometry(20, 160, 80, 20)

        self.last_input = QtWidgets.QLineEdit(self)
        self.last_input.setGeometry(110, 160, 160, 22)
        
        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(160, 240, 80, 30)
        self.cancel_btn.clicked.connect(self.reject)
        
        self.login_btn = QtWidgets.QPushButton("Add", self)
        self.login_btn.setGeometry(80, 240, 80, 30)