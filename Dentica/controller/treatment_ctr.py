from PyQt6.QtCore import pyqtSignal, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6 import QtWidgets
from ui.Dialogues.ui_treatment_dialog import Add_Treatment
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDateTime
from datetime import datetime, date

class Treatment_Dialog_Ctr(Add_Treatment):
    treatment_added = pyqtSignal(dict)
    treatment_edited = pyqtSignal(dict)  


    def __init__(self, appointment_sched: datetime):
        super().__init__()
        self.cost_input.setText("0.00")

         # datetime or date input)
        if isinstance(appointment_sched, datetime):
            self.original_date = appointment_sched.date()
            self.sched_input.setDateTime(appointment_sched)
        elif isinstance(appointment_sched, date):
            self.original_date = appointment_sched
            now = datetime.now()
            # Use appointment date with current time
            combined = datetime.combine(appointment_sched, now.time())
            self.sched_input.setDateTime(combined)
        else:
            raise TypeError("Expected datetime or date for appointment_sched")

        # Connect validator
        cost_regex = QRegularExpression(r"^(0|[1-9]\d{0,6})(\.\d{1,2})?$")
        self.cost_input.setValidator(QRegularExpressionValidator(cost_regex))

        # Lock the date portion
        self.sched_input.dateTimeChanged.connect(self._enforce_appointment_date)

        # Field validation
        self.treat_id_input.textChanged.connect(lambda: self.validate_required(self.treat_id_input))
        self.diagnosis_input.textChanged.connect(lambda: self.validate_required(self.diagnosis_input))
        self.procedure_input.textChanged.connect(lambda: self.validate_required(self.procedure_input))
        self.cost_input.textChanged.connect(self.validate_cost)

        self.add_btn.clicked.connect(self.on_save_clicked)
        self.cancel_btn.clicked.connect(self.reject)

    # This method is called when the user changes the date/time in the QDateTimeEdit
    # It prevents the user from changing the date part of the datetime
    # while allowing them to change the time part
    def _enforce_appointment_date(self, dt: QDateTime):
        """Prevent user from changing the date part."""
        # Extract only the time from user selection
        time = dt.time()
        # Reset to original date + new time
        new_dt = QDateTime(self.original_date, time)
        self.sched_input.blockSignals(True)
        self.sched_input.setDateTime(new_dt)
        self.sched_input.blockSignals(False)

    def validate_required(self, field):
        if not field.text().strip():
            field.setStyleSheet("border: 2px solid red;")
        else:
            field.setStyleSheet("")

    def validate_cost(self):
        text = self.cost_input.text().strip()

        # Try converting to float to check > 0
        try:
            cost_value = float(text)
        except ValueError:
            cost_value = -1  # invalid value, force fail

        if not text or not self.cost_input.hasAcceptableInput() or cost_value <= 0:
            self.cost_input.setStyleSheet("border: 2px solid red;")
            QMessageBox.warning(
                self,
                "Invalid Cost",
                "Please enter a valid cost greater than 0."
            )
            return False
        else:
            self.cost_input.setStyleSheet("")
            return True


    def on_save_clicked(self):
        # Validate all fields
        self.validate_required(self.treat_id_input)
        self.validate_required(self.diagnosis_input)
        self.validate_required(self.procedure_input)
        cost = self.validate_cost()
        if not cost:
            return

        if (
            not self.treat_id_input.text().strip()
            or not self.diagnosis_input.text().strip()
            or not self.procedure_input.text().strip()
            or not self.cost_input.hasAcceptableInput()
        ):
            QMessageBox.warning(self, "Validation Error", "Please fill all required fields correctly.")
            return

        # Collect data
        treatment_data = {
            "Treatment_ID": self.treat_id_input.text(),
            "Diagnosis": self.diagnosis_input.text(),
            "Cost": float(self.cost_input.text()),
            "Treatment_Procedure": self.procedure_input.text(),
            "Treatment_Date_Time": self.sched_input.dateTime().toPyDateTime(),
            "Treatment_Status": self.treat_status.currentText()
        }

        # Emit both signals (controller listens to the one it cares about)
        self.treatment_added.emit(treatment_data)
        self.treatment_edited.emit(treatment_data)

        QMessageBox.information(self, "Success", "Treatment saved successfully!")
        self.accept()