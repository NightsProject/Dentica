from PyQt6 import QtWidgets, QtCore

class Add_Treatment(QtWidgets.QDialog):
 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Treatment")
        self.setFixedSize(300, 400)
        self.setStyleSheet("background-color: #1e293b; color: white;")

        self.treat_id = QtWidgets.QLabel("Treatment ID", self)
        self.treat_id.setGeometry(20, 40, 80, 20)

        self.treat_id_input = QtWidgets.QLineEdit(self)
        self.treat_id_input.setGeometry(110, 40, 160, 22)

        self.diagnosis_label = QtWidgets.QLabel("Diagnosis:", self)
        self.diagnosis_label.setGeometry(20, 80, 150, 20)

        self.diagnosis_input = QtWidgets.QLineEdit(self)
        self.diagnosis_input.setGeometry(110, 80, 160, 22)

        self.procedure_label = QtWidgets.QLabel("Treatment Procedure:", self)
        self.procedure_label.setGeometry(20, 120, 80, 20)

        self.procedure_input = QtWidgets.QLineEdit(self)
        self.procedure_input.setGeometry(110, 120, 160, 22)
        
        self.sched_label = QtWidgets.QLabel("Treatment Schedule:", self)
        self.sched_label.setGeometry(20, 160, 80, 20)

        self.sched_input = QtWidgets.QDateTimeEdit(self)
        self.sched_input.setCalendarPopup(True)
        self.sched_input.setDateTime(QtCore.QDateTime.currentDateTime())
        self.sched_input.setGeometry(110, 160, 160, 22)

        self.cost_label = QtWidgets.QLabel("Cost:", self)
        self.cost_label.setGeometry(20, 200, 90, 20)

        self.cost_input = QtWidgets.QLineEdit(self)
        self.cost_input.setGeometry(110, 200, 160, 22)

        self.add_btn = QtWidgets.QPushButton("Add", self)
        self.add_btn.setGeometry(80, 240, 80, 30)
        
        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(160, 240, 80, 30)
        self.cancel_btn.clicked.connect(self.reject)
        
        
        