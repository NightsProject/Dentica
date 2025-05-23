from ui.Dialogues.ui_patient_dialog import Add_Patient
from backend.patients_comp import generate_new_patient_id, insert_patient, get_all_patients,update_patient

from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, pyqtSignal
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox


class Patient_Dialog_Ctr(Add_Patient):
    patient_added = pyqtSignal()
    
    def __init__(self,parent= None, patient_data = None):
        super().__init__(parent, patient_data)
        self.patient_data = patient_data 
    
        if not patient_data:
            new_id = generate_new_patient_id()
            self.patient_input.setText(new_id)
        
        if patient_data:
            self.add_patient.setText("Update")
            self.add_patient.clicked.connect(self.update_patient)
        else:
            self.add_patient.setText("Add")
            self.add_patient.clicked.connect(self.on_add_pressed)
        
        email_validator = QRegularExpressionValidator(QRegularExpression(r"^[\w\.-]+@[\w\.-]+\.\w+$"))
        self.email_input.setValidator(email_validator)

        contact_validator = QRegularExpressionValidator(QRegularExpression(r"^(09\d{9}|\+639\d{9})$"))
        self.contact_input.setValidator(contact_validator)

        # Real-time validation connections
        self.first_input.textChanged.connect(lambda: self.validate_required(self.first_input))
        self.middle_input.textChanged.connect(lambda: self.validate_required(self.middle_input))
        self.last_input.textChanged.connect(lambda: self.validate_required(self.last_input))
        self.address_input.textChanged.connect(lambda: self.validate_required(self.address_input))
        self.gender_combo.currentIndexChanged.connect(self.validate_gender)
        self.email_input.textChanged.connect(self.validate_email)
        self.contact_input.textChanged.connect(self.validate_contact)
    
    def validate_required(self, field):
        if not field.text().strip():
            field.setStyleSheet("border: 2px solid red;")
            
        else:
            field.setStyleSheet("")
            
    def validate_gender(self):
        if self.gender_combo.currentIndex() == 0:
            self.gender_combo.setStyleSheet("border: 2px solid red;")
           
        else:
            self.gender_combo.setStyleSheet("")

    def validate_email(self):
        text = self.email_input.text().strip()
        if not text or not self.email_input.hasAcceptableInput():
            self.email_input.setStyleSheet("border: 2px solid red;")
        else:
            self.email_input.setStyleSheet("")

    def validate_contact(self):
        text = self.contact_input.text()
        if self.contact_input.hasAcceptableInput():
            self.contact_input.setStyleSheet("")
        else:
            self.contact_input.setStyleSheet("border: 2px solid red;")
           

    def on_add_pressed(self):   
        # Validate all fields
        self.validate_required(self.first_input)
        self.validate_required(self.middle_input)
        self.validate_required(self.last_input)
        self.validate_required(self.address_input)
        self.validate_gender()
        self.validate_email()
        self.validate_contact()

        # Check for validation failures
        if (
            not self.first_input.text().strip()
            or not self.middle_input.text().strip()
            or not self.last_input.text().strip()
            or not self.address_input.text().strip()
            or self.gender_combo.currentIndex() == 0
            or not self.email_input.hasAcceptableInput()
            or not self.contact_input.hasAcceptableInput()
           
        ):
            QtWidgets.QMessageBox.warning(self, "Validation Error", "Please fill all required fields correctly.")
            return  # Stop submission

        # All valid, proceed to collect data
        patient_id = self.patient_input.text()
        first_name = self.first_input.text()
        middle_name = self.middle_input.text()
        last_name = self.last_input.text()
        gender = self.gender_combo.currentText()
        address = self.address_input.text()
        contact_number = self.contact_input.text()
        email = self.email_input.text()
        birth_date = self.birth_input.date().toString("yyyy-MM-dd")

        success = insert_patient(patient_id, first_name, middle_name, last_name, gender, birth_date, contact_number, email, address)
        if success:
            self.patient_added.emit()
            QMessageBox.information(self, "Success", "Patient added successfully!")
            self.accept()  

    def update_patient(self):
        patient_id = self.patient_input.text()
        first_name = self.first_input.text()
        middle_name = self.middle_input.text()
        last_name = self.last_input.text()
        gender = self.gender_combo.currentText() if self.gender_combo.currentIndex() > 0 else ""
        birth_date = self.birth_input.date().toString(QtCore.Qt.DateFormat.ISODate)
        contact_number = self.contact_input.text()
        email = self.email_input.text()
        address = self.address_input.text()

        # Validate required fields
        if not all([first_name, last_name, gender, contact_number]):
            QMessageBox.warning(self, "Validation Error", "Please fill in all required fields.")
            return

        success = update_patient(
            patient_id,
            first_name,
            middle_name,
            last_name,
            gender,
            birth_date,
            contact_number,
            email,
            address
        )

        if success:
            self.patient_added.emit()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to update patient.")    
            
      