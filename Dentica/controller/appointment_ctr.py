from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox, QInputDialog
from ui.Dialogues.ui_appointment_dialog import Add_Appointment
from backend.appointments_comp import generate_new_appointment_id, save_appointment_to_db, get_patients_name,update_appointment_in_db
from backend.billing_comp import generate_new_payment_id
from backend.booking_comp import generate_new_booking_id
from controller.treatment_ctr import Treatment_Dialog_Ctr
from PyQt6.QtCore import Qt
from datetime import datetime
from backend.treatment_comp import delete_treatment_by_id
from backend.appointments_comp import get_appointment_details


"""
        
    Key Features

    Signal Emission:
        appointment_added: A custom signal that is emitted when an appointment is successfully added or updated. This allows other parts of the application to react to this event.

    Initialization:
        The constructor (__init__) initializes the dialog, sets up the appointment data, and configures the UI components based on whether the dialog is for creating a new appointment or updating an existing one.
        It generates a new appointment ID if creating a new appointment and sets up the patient input field.

    Treatment Management:
        The class maintains a list of treatments associated with the appointment. It allows adding new treatments, updating the treatment list, and deleting treatments.
        The sync_treatment_dates method ensures that when the appointment date is changed, the corresponding treatment dates are updated while preserving the time.

    Patient Search:
        The update_patient_search method filters the list of patients based on the input text, allowing users to search for patients by name. It updates the patient input combo box with matching results.

    Adding Treatments:
        The on_add_treatment_clicked method opens a dialog for adding a new treatment. When a treatment is added, it updates the treatment list and the total billing amount.

    Billing Calculation:
        The update_total_billing method calculates the total cost of all treatments and updates the billing display in the UI.

    UI Updates:
        The update_treatment_table_ui method updates the treatment table in the UI with the newly added treatment, including a delete button for each treatment.
        The remove_treatment method allows users to delete a treatment from the list and the UI, confirming the action with a message box.

    Validation:
        The class includes validation methods (validate_required and validate_status) to ensure that required fields are filled out correctly before saving or updating an appointment.

    Saving and Updating Appointments:
        The on_add_pressed method handles the logic for saving a new appointment, including gathering all necessary data, generating booking and payment details, and saving to the database.
        The on_update_pressed method handles updating an existing appointment, including validating inputs and deleting treatments marked for deletion.
        
"""



class Appointment_Dialog_Ctr(Add_Appointment):
    
    appointment_added = pyqtSignal()

    def __init__(self, parent=None, appointment_data=None):
        super().__init__(parent, appointment_data)
        self.appointment_data = appointment_data
        
       # Setup treatments and counter based on appointment data
        self.treatments = appointment_data.get('Treatments', []) if appointment_data else []
        self.treatment_counter = len(self.treatments) + 1
        self.treatments_to_delete = [] # when updating the appointment

        self.setup_patient_input()  # Initialize patient input components

        # If editing an existing appointment
        if appointment_data:
            self.appointment_id = appointment_data.get('Appointment_ID')  # Needed for updates
            self.add_btn.setText("Update")
            self.setWindowTitle("Update Appointment")
            try:
                self.add_btn.clicked.disconnect()
            except TypeError:
                pass
            self.add_btn.clicked.connect(self.on_update_pressed)

            self.update_patient_search(appointment_data.get('Patient_Name', ''))
            self.update_total_billing()
        else:
            # Creating a new appointment
            self.appointment_id = generate_new_appointment_id()
            self.appointment_input.setText(self.appointment_id)
            self.add_btn.setText("Add")
            try:
                self.add_btn.clicked.disconnect()
            except TypeError:
                pass
            self.add_btn.clicked.connect(self.on_add_pressed)

        # Connect treatment addition and status validation
        self.AddTreat_btn.clicked.connect(self.on_add_treatment_clicked)
        self.status_input.currentIndexChanged.connect(self.validate_status)
        
        self.schedule_input.dateTimeChanged.connect(self.sync_treatment_dates)

    # This method is called when the user changes the date/time in the QDateTimeEdit
    # It prevents the user from changing the date part of the datetime
    # while allowing them to change the time part
    def sync_treatment_dates(self):
        new_date = self.schedule_input.dateTime().toPyDateTime().date()

        for treatment in self.treatments:
            old_datetime = treatment["Treatment_Date_Time"]
            if isinstance(old_datetime, str):
                old_datetime = datetime.strptime(old_datetime, "%Y-%m-%d %H:%M:%S")
            
            # Replace only the date, preserve the time
            updated_datetime = datetime.combine(new_date, old_datetime.time())
            treatment["Treatment_Date_Time"] = updated_datetime

    def update_patient_search(self, text):
        if not hasattr(self, 'patient_input_line_edit') or self.patient_input_line_edit is None:
            self.patient_input_line_edit = self.patient_input.lineEdit()
            if self.patient_input_line_edit is None:
                return
        
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
        appointment_date = self.schedule_input.dateTime().toPyDateTime().date()
        form = Treatment_Dialog_Ctr(appointment_date)
        form.treat_id_input.setText(str(self.get_new_treatment_id()))
        form.treatment_added.connect(self.handle_treatment_added)
        form.exec()

    def handle_treatment_added(self, data):
        data["Appointment_ID"] = self.appointment_id
        self.treatment_counter += 1
        self.status_input.setCurrentText("Scheduled")
        self.treatments.append(data)
        self.update_treatment_table_ui(data)
        self.update_total_billing()  # Update total billing after treatment is added

    def update_total_billing(self):
        total = 0.0
        for treatment in self.treatments:
            try:
                #treatment dict has a 'Cost' field with a string/float
                cost = float(treatment.get("Cost", 0))
                total += cost
            except ValueError:
                print(f"Invalid cost value in treatment: {treatment}")

        #display the total billing
        self.total_input.setText(f"₱{total:,.2f}")
        return total

    def update_treatment_table_ui(self, treatment):
        row = self.Treat_table.rowCount()
        self.Treat_table.insertRow(row)
        
        print(treatment)
        # Create action buttons
        action_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        delete_btn = QtWidgets.QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                min-width: 60px;
            }
            QPushButton:hover {
            background-color: #cc0000;
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
    
    
    def remove_treatment(self, row):
        """
        Remove a treatment both from the internal list and the UI table by the given row index.
        Tracks deletions for DB update if editing an existing appointment.
        """
        if row < 0 or row >= len(self.treatments):
            return  # Invalid row index

        # Confirm deletion with user
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this treatment?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        # Remove treatment from internal list
        removed_treatment = self.treatments.pop(row)

        # Mark for DB deletion if editing existing appointment
        if self.appointment_data and "Treatment_ID" in removed_treatment:
            if not hasattr(self, "treatments_to_delete"):
                self.treatments_to_delete = []
            self.treatments_to_delete.append(removed_treatment["Treatment_ID"])

        # Remove row from the table
        self.Treat_table.removeRow(row)

        # Update treatment IDs and UI rows below the removed row
        for i in range(row, len(self.treatments)):
            treatment = self.treatments[i]
            treatment["Treatment_ID"] = i + 1  # Reassign new sequential ID

            # Update table UI row i (shifted up)
            self.Treat_table.item(i, 0).setText(str(treatment["Treatment_ID"]))

            # Reconnect delete button for new row index
            action_widget = self.Treat_table.cellWidget(i, 3)
            if action_widget:
                btn = action_widget.findChild(QtWidgets.QPushButton)
                if btn:
                    btn.clicked.disconnect()
                    btn.clicked.connect(lambda checked=False, r=i: self.remove_treatment(r))

        # Decrement treatment counter
        self.treatment_counter -= 1

        # Update total billing
        self.update_total_billing()

    
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

        #setup booking and payment details
        booking_id = generate_new_booking_id()
        booking_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        Payment_id = generate_new_payment_id()
        total_amount = self.total_input.text().replace('₱', '').replace(',', '')
        payment_method = "None"
        payment_status = "Unpaid"
       
        
        booking_data = {
            "Booking_ID": booking_id,
            "Patient_ID": pat_id,
            "Appointment_ID": app_id,
            "Booking_Date_Time": booking_date
        }
        
        payment_data = {
            "Payment_ID": Payment_id,
            "Booking_ID": booking_id,
            "Total_Amount": total_amount,
            "Payment_Method": payment_method,
            "Payment_Status": payment_status,
            
        }
        
        appointment_data = {
            "Appointment_ID": app_id,
            "Patient_ID": pat_id,
            "Schedule": formatted_sched,
            "Status": status,
            "Treatments": self.treatments,
            "Booking": booking_data,
            "Payment": payment_data
        }

        success = save_appointment_to_db(appointment_data)
        if success:
            QMessageBox.information(self, "Success", "Appointment saved successfully.")
            self.appointment_added.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "Database Error", "Failed to save the appointment. Please try again.")

    def on_update_pressed(self):
        # 1) Fetch current data from DB before update
        prev = get_appointment_details(self.appointment_id)
        if not prev:
            QMessageBox.critical(self, "Error", "Failed to fetch existing appointment details.")
            return

        previous_status   = prev["Status"]
        previous_schedule = prev["Schedule"]
        new_status        = self.status_input.currentText()
        new_schedule      = self.schedule_input.dateTime().toPyDateTime()

        # 2) Notify for cancel-record deletion if coming back from Cancelled
        if previous_status == "Cancelled" and new_status in ("Scheduled", "Completed"):
            QMessageBox.information(
                self, "Cancellation Record Removed",
                "The appointment was previously cancelled. Cancellation data will now be removed."
            )

        # 3) Notify for schedule change
        prev_str = previous_schedule.strftime('%Y-%m-%d %H:%M')
        new_str  = new_schedule.strftime('%Y-%m-%d %H:%M')
        if previous_schedule != new_schedule:
            QMessageBox.information(
                self, "Appointment Rescheduled",
                f"Appointment moved from {prev_str} to {new_str}."
            )

        # 4) Validation
        if not (self.get_selected_patient_id() and self.validate_status()):
            QMessageBox.warning(self, "Validation Error",
                                "Please select a valid patient and status.")
            return
        if new_status != "Cancelled" and not self.treatments:
            QMessageBox.warning(self, "No Treatments",
                                "You must add at least one treatment for non-cancelled appointments.")
            return

        # 5) Prepare core appointment_data
        app_id = self.appointment_id
        pat_id = self.get_selected_patient_id()
        formatted_sched = new_schedule.strftime('%Y-%m-%d %H:%M:%S')

        appointment_data = {
            "Appointment_ID": app_id,
            "Patient_ID":     pat_id,
            "Schedule":       formatted_sched,
            "Status":         new_status,
            "Treatments":     self.treatments,
        }

        # 6) Cancellation payload
        if new_status == "Cancelled":
            reply = QMessageBox.question(
                self, "Confirm Cancellation",
                "Are you sure you want to cancel this appointment?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

            reason, ok = QInputDialog.getText(
                self, "Cancellation Reason",
                "Please enter the reason for cancellation:"
            )
            if not (ok and reason.strip()):
                QMessageBox.warning(self, "Input Required", "Cancellation reason is required.")
                return

            appointment_data["Cancel"] = {
                "Cancellation_Date_Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "Reason": reason.strip()
            }

        # 7) Re-schedule logic: if coming back from Cancelled → Scheduled, generate new IDs
        if previous_status == "Cancelled" and new_status == "Scheduled":
            booking_id = generate_new_booking_id()
            payment_id = generate_new_payment_id()
            booking_dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            total_amt  = self.update_total_billing()

            appointment_data["Booking"] = {
                "Booking_ID":        booking_id,
                "Patient_ID":        pat_id,
                "Appointment_ID":    app_id,
                "Booking_Date_Time": booking_dt
            }

            appointment_data["Payment"] = {
                "Payment_ID":     payment_id,
                "Patient_ID":     pat_id,
                "Appointment_ID": app_id,
                "Total_Amount":   total_amt,
                "Payment_Method": "None",
                "Payment_Status": "Unpaid",
                "Payment_Date":   None
            }

        # 8) If still Scheduled (but not a re-schedule), carry forward and update payment info
        elif new_status == "Scheduled" and "Booking" not in appointment_data:
            appointment_data["Booking"] = {
                "Booking_ID":        prev["Booking_ID"],
                "Patient_ID":        pat_id,
                "Appointment_ID":    app_id,
                "Booking_Date_Time": prev["Booking_Date_Time"].strftime('%Y-%m-%d %H:%M:%S')
            }
            appointment_data["Payment"] = {
                "Payment_ID":     prev["Payment_ID"],
                "Patient_ID":     pat_id,
                "Appointment_ID": app_id,
                "Total_Amount":   self.update_total_billing(),
                "Payment_Method": prev["Payment_Method"],
                "Payment_Status": prev["Payment_Status"],
                "Payment_Date":   prev["Payment_Date"]
            }

        # 9) Delete treatments marked for deletion
        if hasattr(self, "treatments_to_delete"):
            for tid in self.treatments_to_delete:
                delete_treatment_by_id(app_id, tid)
            self.treatments_to_delete = []

        # 10) Commit to DB
        success = update_appointment_in_db(appointment_data)
        if success:
            QMessageBox.information(self, "Success", "Appointment updated successfully.")
            self.appointment_added.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "Database Error",
                                "Failed to update the appointment. Please try again.")
