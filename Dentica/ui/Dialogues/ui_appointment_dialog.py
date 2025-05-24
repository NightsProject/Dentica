from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from controller.treatment_ctr import Treatment_Dialog_Ctr
from controller.patient_ctr import Patient_Dialog_Ctr

class Add_Appointment(QtWidgets.QDialog):
    def __init__(self, parent=None, appointment_data=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Book Appointment")
        self.setFixedSize(600, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #B2CDE9;
                border: 1px solid #fff;
                border-radius: 5px;
            }
        """)
        self.oldPos = None

        label_style = "color: #37547A; font-family: Inter; font-size: 14px;"
        input_x = 150
        label_x = 20
        row_height = 40
        row_start = 60

        self.header = QtWidgets.QLabel("Appointment Form", self)
        self.header.setGeometry(20, 20, 300, 25)
        self.header.setStyleSheet("""color: #fff; font-family: Katarine; font-size: 20px; font-weight: bold;""")

        def add_row(row, text, widget):
            y = row_start + row * row_height
            label = QtWidgets.QLabel(text, self)
            label.setGeometry(label_x, y, 120, 20)
            label.setStyleSheet(label_style)
            widget.setGeometry(input_x, y, 160, 22)

        self.appointment_input = QtWidgets.QLineEdit(self)
        add_row(0, "Appointment ID:", self.appointment_input)

        self.patient_input = QtWidgets.QComboBox(self)
        self.patient_input.setEditable(True)
        self.patient_input.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        add_row(1, "Patient Name:", self.patient_input)
        self.patient_input.lineEdit().textChanged.connect(self.update_patient_search)


        self.AddPatient_btn = QtWidgets.QPushButton("Add Patient", self)
        self.AddPatient_btn.setGeometry(400, row_start + 1 * row_height, 120, 30)
        self.AddPatient_btn.setStyleSheet("background-color: #37547A; color: #fff;")
        self.AddPatient_btn.clicked.connect(self.open_patient)

        self.schedule_input = QtWidgets.QDateTimeEdit(self)
        self.schedule_input.setCalendarPopup(True)
        self.schedule_input.setDateTime(QtCore.QDateTime.currentDateTime())
        add_row(2, "Schedule:", self.schedule_input)

        self.status_input = QtWidgets.QComboBox(self)
        self.status_input.setGeometry(input_x, row_start + 3 * row_height, 160, 22)
        self.status_input.addItems(["Select Status", "Scheduled", "Completed", "Cancelled"])
        
        label = QtWidgets.QLabel("Status:", self)
        label.setGeometry(label_x, row_start + 3 * row_height, 120, 20)
        label.setStyleSheet(label_style)
        
        self.AddTreat_btn = QtWidgets.QPushButton("Add Treatment", self)
        self.AddTreat_btn.setGeometry(400, row_start + 3 * row_height, 120, 30)
        self.AddTreat_btn.setStyleSheet("background-color: #37547A; color: #fff;")
      
        self.Treat_table = QtWidgets.QTableWidget(self)
        self.Treat_table.setGeometry(20, 220, 300, 280)
        self.Treat_table.setColumnCount(4)
        self.Treat_table.setHorizontalHeaderLabels(["TreatmentID", "Procedure", "Cost", "Actions"])
        self.Treat_table.setStyleSheet("""
            QTableWidget {
                background-color: #B2CDE9;
                color: #37547A;
                gridline-color: #A0BFD8;
                border: 1px solid #fff;
                font-family: Inter;
                font-size: 13px;
            }
            QHeaderView::section {
            background-color: #A0BFD8;
            color: #37547A;
            font-weight: bold;
            border: none;
            padding: 4px;
            margin: 0px;
            }
            QTableWidget::item:selected {
                background-color: #88A9C9;
                color: white;
            }
        """)
        self.Treat_table.setRowCount(0)
        self.Treat_table.horizontalHeader().setContentsMargins(0, 0, 0, 0)
        self.Treat_table.horizontalHeader().setStyleSheet("margin: 0px; padding: 0px;")
        
        
        self.total_label = QtWidgets.QLabel("Total Bill:", self)
        self.total_label.setGeometry(340, 470, 100, 22)
        self.total_label.setStyleSheet("color: #37547A; font-family: Inter; font-size: 14px;")

        self.total_input = QtWidgets.QLineEdit(self)
        self.total_input.setGeometry(430, 470, 130, 22)
        self.total_input.setReadOnly(True)
        self.total_input.setText("Fetch Total Cost")
        self.total_input.setStyleSheet("background-color: #fff; color: #37547A;")

        self.add_btn = QtWidgets.QPushButton("Add", self)
        self.add_btn.setGeometry(200, 530, 80, 30)
        self.add_btn.setStyleSheet("background-color: #37547A; color: #fff;")

        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(310, 530, 80, 30)
        self.cancel_btn.setStyleSheet("""
            QPushButton {background-color: #37547A; color: #fff;}
            QPushButton:hover {background-color: #fff; color: #000;}
        """)
        self.cancel_btn.clicked.connect(self.reject)
        
        if appointment_data:
            self.populate_fields(appointment_data)
            
    def populate_fields(self, appointment_data):
        self.appointment_input.setText(appointment_data['Appointment_ID'])
        self.appointment_input.setReadOnly(True)
        
        # Set patient
        patient_name = appointment_data.get('Patient_Name', '')
        self.patient_input.setCurrentText(patient_name)
        
        # Set schedule
        schedule = QtCore.QDateTime.fromString(appointment_data['Schedule'], QtCore.Qt.DateFormat.ISODate)
        self.schedule_input.setDateTime(schedule)
        
        # Set status
        status_index = self.status_input.findText(appointment_data['Status'])
        if status_index >= 0:
            self.status_input.setCurrentIndex(status_index)
        
        # Clear existing treatments and add new ones
        self.treatments = appointment_data.get('Treatments', [])
        self.Treat_table.setRowCount(0)
        for treatment in self.treatments:
            self.update_treatment_table_ui(treatment)
        if self.treatments:
            max_id = max(int(t['Treatment_ID']) for t in self.treatments)
            self.treatment_counter = max_id + 1

    def open_patient(self):
        patient_popup = Patient_Dialog_Ctr()
        patient_popup.exec()

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
