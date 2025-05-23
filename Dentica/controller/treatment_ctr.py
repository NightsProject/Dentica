from PyQt6.QtCore import pyqtSignal, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6 import QtWidgets
from ui.Dialogues.ui_treatment_dialog import Add_Treatment
from PyQt6.QtWidgets import QMessageBox

class Treatment_Dialog_Ctr(Add_Treatment):
    treatment_added = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.cost_input.setText("0.00")

        # Validators
        cost_regex = QRegularExpression(r"^(0|[1-9]\d{0,6})(\.\d{1,2})?$")
        self.cost_input.setValidator(QRegularExpressionValidator(cost_regex))

        # Connect real-time validation
        self.treat_id_input.textChanged.connect(lambda: self.validate_required(self.treat_id_input))
        self.diagnosis_input.textChanged.connect(lambda: self.validate_required(self.diagnosis_input))
        self.procedure_input.textChanged.connect(lambda: self.validate_required(self.procedure_input))
        self.cost_input.textChanged.connect(self.validate_cost)

        self.add_btn.clicked.connect(self.on_add_treatment_clicked)
        self.cancel_btn.clicked.connect(self.reject)

    def validate_required(self, field):
        if not field.text().strip():
            field.setStyleSheet("border: 2px solid red;")
        else:
            field.setStyleSheet("")

    def validate_cost(self):
        text = self.cost_input.text().strip()
        if not text or not self.cost_input.hasAcceptableInput():
            self.cost_input.setStyleSheet("border: 2px solid red;")
        else:
            self.cost_input.setStyleSheet("")

    def on_add_treatment_clicked(self):
        # Validate all fields
        self.validate_required(self.treat_id_input)
        self.validate_required(self.diagnosis_input)
        self.validate_required(self.procedure_input)
        self.validate_cost()

        # Check if any field is invalid
        if (
            not self.treat_id_input.text().strip()
            or not self.diagnosis_input.text().strip()
            or not self.procedure_input.text().strip()
            or not self.cost_input.hasAcceptableInput()
        ):
            QMessageBox.warning(self, "Validation Error", "Please fill all required fields correctly.")
            return

        # All inputs are valid — collect data
        treatment_data = {
            "Treatment_ID": self.treat_id_input.text(),
            "Diagnosis": self.diagnosis_input.text(),
            "Cost": float(self.cost_input.text()),
            "Treatment_Procedure": self.procedure_input.text(),
            "Treatment_Date_Time": self.sched_input.dateTime().toPyDateTime(),
            "Treatment_Status": self.treat_status.currentText()
        }

        self.treatment_added.emit(treatment_data)
        QMessageBox.information(self, "Success", "Treatment added successfully!")
        self.close()
