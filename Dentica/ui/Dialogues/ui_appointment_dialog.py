from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDateEdit
from PyQt6.QtCore import QDate
from controller.treatment_ctr import Treatment_Dialog_Ctr
from controller.patient_ctr import Patient_Dialog_Ctr

class Add_Appointment(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Book Appointment")
        self.setFixedSize(600, 600)
        self.setStyleSheet("background-color: #1e293b; color: white;")

        self.appointment_id = QtWidgets.QLabel("Appointment ID:", self)
        self.appointment_id.setGeometry(20, 40, 90, 20)

        self.appointment_input = QtWidgets.QLineEdit(self)
        self.appointment_input.setGeometry(110, 40, 160, 22)

        self.patient_id = QtWidgets.QLabel("Patient ID:", self)
        self.patient_id.setGeometry(20, 80, 80, 20)

        self.patient_input = QtWidgets.QLineEdit(self)
        self.patient_input.setGeometry(110, 80, 160, 22)
        self.patient_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        
        self.AddPatient_btn = QtWidgets.QPushButton("Add Patient", self)
        self.AddPatient_btn.setGeometry(400, 80, 120, 30)
        self.AddPatient_btn.clicked.connect(lambda: open_patient(self))

        def open_patient(self):
            patient_popup = Patient_Dialog_Ctr()
            patient_popup.exec()
        
 
        self.schedule = QtWidgets.QLabel("Schedule:", self)
        self.schedule.setGeometry(20, 120, 80, 20)

        self.schedule_input = QtWidgets.QDateTimeEdit(self)
        self.schedule_input.setCalendarPopup(True)
        self.schedule_input.setDateTime(QtCore.QDateTime.currentDateTime())
        self.schedule_input.setGeometry(110, 120, 160, 22)

        self.AddTreat_btn = QtWidgets.QPushButton("Add Treatment", self)
        self.AddTreat_btn.clicked.connect(lambda: add_treat_form(self))
        self.AddTreat_btn.setGeometry(400, 150, 120, 30)

        def add_treat_form(self):
            treat_popup = Treatment_Dialog_Ctr()
            treat_popup.exec()


        self.Treat_table = QtWidgets.QTableWidget(parent=self)
        self.Treat_table.setGeometry(20, 192, 500, 300)
        self.Treat_table.setObjectName("Treat_table")
        self.Treat_table.setColumnCount(3)
        self.Treat_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Treat_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Treat_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.Treat_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.Treat_table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("TreatmentID"))
        self.Treat_table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Procedure"))
        self.Treat_table.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Cost"))


        self.add_btn = QtWidgets.QPushButton("Add", self)
        self.add_btn.setGeometry(200, 550, 80, 30)
        
        
        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(310, 550, 80, 30)
        self.cancel_btn.clicked.connect(self.reject)
        
      


