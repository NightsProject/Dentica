from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from ui.Dialogues.ui_appointment_dialog import Add_Appointment
from backend.appointments_comp import generate_new_appointment_id, save_appointment_to_db
from controller.treatment_ctr import Treatment_Dialog_Ctr
from PyQt6.QtCore import QDateTime


class Appointment_Dialog_Ctr(Add_Appointment):
    
    appointment_added = pyqtSignal()

    def __init__(self):
        super().__init__()
       
        self.AddTreat_btn.clicked.connect(self.on_add_treatment_clicked)
        self.new_appointment_id = generate_new_appointment_id()  
        self.appointment_input.setText(self.new_appointment_id)
        self.appointment_input.setReadOnly(True)
        
        self.treatments = []
        self.treatment_counter = 1
        
        self.add_btn.clicked.connect(self.on_add_pressed)

        # Real-time validation connections
        self.patient_input.textChanged.connect(lambda: self.validate_required(self.patient_input))
        self.status_input.currentIndexChanged.connect(self.validate_status)
       
    def get_new_treatment_id(self):
        treatment_id = self.treatment_counter
        return treatment_id

    def on_add_treatment_clicked(self):
        self.treatment_form = Treatment_Dialog_Ctr()
        self.treatment_form.treat_id_input.setText(str(self.get_new_treatment_id()))
        self.treatment_form.treatment_added.connect(self.handle_treatment_added)  
        self.treatment_form.exec()

    def handle_treatment_added(self, data):
        data["Appointment_ID"] = self.new_appointment_id
        self.treatment_counter += 1
        self.treatments.append(data)
        self.update_treatment_table_ui(data)
    
    def update_treatment_table_ui(self, treatment):
        row = self.Treat_table.rowCount()
        self.Treat_table.insertRow(row)
        self.Treat_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(treatment["Treatment_ID"])))
        self.Treat_table.setItem(row, 1, QtWidgets.QTableWidgetItem(treatment["Treatment_Procedure"]))
        self.Treat_table.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{treatment['Cost']:.2f}"))

    # Validation functions

    def validate_required(self, field):
        if not field.text().strip():
            field.setStyleSheet("border: 2px solid red;")
            return False
        else:
            field.setStyleSheet("")
            return True

    def validate_status(self):
        if self.status_input.currentIndex() == 0:  # assuming index 0 is a placeholder like "Select Status"
            self.status_input.setStyleSheet("border: 2px solid red;")
            return False
        else:
            self.status_input.setStyleSheet("")
            return True

    def on_add_pressed(self):
        # Run validations
        valid_patient = self.validate_required(self.patient_input)
        valid_status = self.validate_status()
        
        if not self.treatments:
            QMessageBox.warning(self, "No Treatments", "You must add at least one treatment before saving the appointment.")
            return

        if not (valid_patient and valid_status):
            QMessageBox.warning(self, "Validation Error", "Please fill all required fields correctly.")
            return

        app_id = self.appointment_input.text()
        pat_id = self.patient_input.text()
        sched = self.schedule_input.dateTime().toPyDateTime()
        formatted_sched = sched.strftime('%Y-%m-%d %H:%M:%S')
        status = self.status_input.currentText()

        appointment_data = {
            "Appointment_ID": app_id,
            "Patient_ID": pat_id,
            "Schedule": formatted_sched,
            "Status": status,
            "Treatments": self.treatments
        }

        success = save_appointment_to_db(appointment_data)
        if success:
            QMessageBox.information(self, "Success", "Appointment saved successfully.")
            self.appointment_added.emit()  
            self.accept()  
        else:
            QMessageBox.critical(self, "Database Error", "Failed to save the appointment. Please try again.")
