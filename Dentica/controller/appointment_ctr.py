from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from ui.Dialogues.ui_appointment_dialog import Add_Appointment
from backend.appointments_comp import generate_new_appointment_id, save_appointment_to_db, get_patients_name,update_appointment_in_db
from controller.treatment_ctr import Treatment_Dialog_Ctr
from PyQt6.QtCore import Qt

class Appointment_Dialog_Ctr(Add_Appointment):
    
    appointment_added = pyqtSignal()

    def __init__(self, parent=None, appointment_data=None):
        super().__init__(parent, appointment_data)
        self.appointment_data = appointment_data
        
       # Setup treatments and counter based on appointment data
        self.treatments = appointment_data.get('Treatments', []) if appointment_data else []
        self.treatment_counter = len(self.treatments) + 1

        # Setup patient input
        self.patient_input.setEditable(True)
        self.patient_input.setMaxVisibleItems(10)
        self.patient_input.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)

        self.patient_input_line_edit = self.patient_input.lineEdit()
        if self.patient_input_line_edit is not None:
            self.patient_input_line_edit.setPlaceholderText("Search by name...")
            self.patient_input_line_edit.setMaxLength(50)
            self.patient_input_line_edit.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.patient_input_line_edit.setFocus()
            self.patient_input_line_edit.textChanged.connect(self.update_patient_search)
        else:
            print("Warning: Could not get line edit from patient input combo box")

        # Load all patients once
        self.all_patients = get_patients_name()

        # If editing an existing appointment
        if appointment_data:
            self.appointment_id = appointment_data.get('Appointment_ID')  # Needed for updates
            self.add_btn.setText("Update")
            try:
                self.add_btn.clicked.disconnect()
            except TypeError:
                pass
            self.add_btn.clicked.connect(self.on_update_pressed)

            self.update_patient_search(appointment_data.get('Patient_Name', ''))
        else:
            # Creating a new appointment
            self.new_appointment_id = generate_new_appointment_id()
            self.appointment_input.setText(self.new_appointment_id)
            self.add_btn.setText("Add")
            try:
                self.add_btn.clicked.disconnect()
            except TypeError:
                pass
            self.add_btn.clicked.connect(self.on_add_pressed)

        # Connect treatment addition and status validation
        self.AddTreat_btn.clicked.connect(self.on_add_treatment_clicked)
        self.status_input.currentIndexChanged.connect(self.validate_status)


    def update_patient_search(self, text):
        if not hasattr(self, 'patient_input_line_edit') or self.patient_input_line_edit is None:
            self.patient_input_line_edit = self.patient_input.lineEdit()
            if self.patient_input_line_edit is None:
                return
        
        # Ensure we have patients data
        if not hasattr(self, 'all_patients'):
            self.all_patients = get_patients_name()
        
        combo = self.patient_input
        edit = self.patient_input_line_edit
        
        # Block signals to prevent recursion
        combo.blockSignals(True)
        edit.blockSignals(True)

        # Clear current items
        combo.clear()

        # If empty text, show nothing
        if not text.strip():
            combo.blockSignals(False)
            edit.blockSignals(False)
            return

        # Filter patients based on search text
        filtered = [
            p for p in self.all_patients
            if text.lower() in p["Full_Name"].lower()
        ]

        if filtered:
            for p in filtered:
                combo.addItem(p["Full_Name"], p["Patient_ID"])
        else:
            combo.addItem("No matches found", None)

        # Restore the text that was being typed
        edit.setText(text)

        # Re-enable signals
        combo.blockSignals(False)
        edit.blockSignals(False)

    def get_selected_patient_id(self):
        return self.patient_input.currentData()

    def get_new_treatment_id(self):
        return self.treatment_counter

    def on_add_treatment_clicked(self):
        form = Treatment_Dialog_Ctr()
        form.treat_id_input.setText(str(self.get_new_treatment_id()))
        form.treatment_added.connect(self.handle_treatment_added)
        form.exec()

    def handle_treatment_added(self, data):
        data["Appointment_ID"] = self.new_appointment_id
        self.treatment_counter += 1
        self.treatments.append(data)
        self.update_treatment_table_ui(data)
    
    def update_treatment_table_ui(self, treatment):
        row = self.Treat_table.rowCount()
        self.Treat_table.insertRow(row)
        
        # Create action buttons
        action_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        delete_btn = QtWidgets.QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                padding: 2px 5px;
                border-radius: 3px;
            }
        """)
        delete_btn.clicked.connect(lambda: self.remove_treatment(row))
        layout.addWidget(delete_btn)
        action_widget.setLayout(layout)
        
        # Add items to table
        self.Treat_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(treatment["Treatment_ID"])))
        self.Treat_table.setItem(row, 1, QtWidgets.QTableWidgetItem(treatment["Treatment_Procedure"]))
        self.Treat_table.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{treatment['Cost']:.2f}"))
        self.Treat_table.setCellWidget(row, 3, action_widget)
    
    def setup_patient_input(self):
        """Initialize patient input components and connections"""
        if not hasattr(self, 'patient_input_line_edit') or self.patient_input_line_edit is None:
            self.patient_input_line_edit = self.patient_input.lineEdit()
        
        if self.patient_input_line_edit is not None:
            self.patient_input_line_edit.setPlaceholderText("Search by name...")
            self.patient_input_line_edit.setMaxLength(50)
            self.patient_input_line_edit.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.patient_input_line_edit.setFocus()
            self.patient_input_line_edit.textChanged.connect(self.update_patient_search)
        else:
            print("Warning: Could not get line edit from patient input combo box")
        
        # Load all patients initially
        self.all_patients = get_patients_name()
        self.patient_input.setMaxVisibleItems(10)
        self.patient_input.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        self.patient_input.setEditable(True)
    # Validation

    def validate_required(self, field):
        if not field.text().strip():
            field.setStyleSheet("border: 2px solid red;")
            return False
        field.setStyleSheet("")
        return True

    def validate_status(self):
        if self.status_input.currentIndex() == 0:
            self.status_input.setStyleSheet("border: 2px solid red;")
            return False
        self.status_input.setStyleSheet("")
        return True

    def on_add_pressed(self):
        if not self.treatments:
            QMessageBox.warning(self, "No Treatments",
                                "You must add at least one treatment before saving the appointment.")
            return

        # validate patient selection and status
        valid_patient = bool(self.get_selected_patient_id())
        valid_status = self.validate_status()
        if not (valid_patient and valid_status):
            QMessageBox.warning(self, "Validation Error",
                                "Please select a valid patient and status.")
            return

        app_id = self.appointment_input.text()
        pat_id = self.get_selected_patient_id()
        if not pat_id:
            QMessageBox.warning(self, "Invalid Patient",
                                "Please select a valid patient from the list.")
            return

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

    def on_update_pressed(self):
        # Validate required fields
        valid_patient = bool(self.get_selected_patient_id())
        valid_status = self.validate_status()
        
        if not (valid_patient and valid_status):
            QMessageBox.warning(self, "Validation Error",
                            "Please select a valid patient and status.")
            return
        
        # Only require treatments if status is not Cancelled
        if self.status_input.currentText() != "Cancelled" and not self.treatments:
            QMessageBox.warning(self, "No Treatments",
                            "You must add at least one treatment for non-cancelled appointments.")
            return
        
        # Prepare appointment data
        app_id = self.appointment_id
        pat_id = self.get_selected_patient_id()
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

        # Update in database
        success = update_appointment_in_db(appointment_data)
        if success:
            QMessageBox.information(self, "Success", "Appointment updated successfully.")
            self.appointment_added.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "Database Error", 
                            "Failed to update the appointment. Please try again.")