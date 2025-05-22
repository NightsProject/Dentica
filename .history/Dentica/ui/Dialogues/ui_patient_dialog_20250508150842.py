from PyQt6 import QtWidgets


class Add_Patient(QtWidgets.QDialog):
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