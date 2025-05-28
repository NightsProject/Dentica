import os
import shutil
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, pyqtSignal
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMessageBox
from ui.Dialogues.ui_patient_dialog import Add_Patient
from backend.patients_comp import generate_new_patient_id, insert_patient, update_patient
from PyQt6.QtWidgets import QToolTip
import re

class Patient_Dialog_Ctr(Add_Patient):
    patient_added = pyqtSignal()
    
    def __init__(self, parent=None, patient_data=None):
        super().__init__(parent, patient_data)
        self.patient_data = patient_data 
        self.picture_path = None  # Store the selected picture path

        self.dark_mode = False
        
        if not patient_data:
            new_id = generate_new_patient_id()
            self.patient_input.setText(new_id)
            self.add_patient.clicked.connect(self.on_add_pressed)
        else:
            self.add_patient.setText("Update")
            self.add_patient.clicked.connect(self.update_patient)
            self.load_patient_data(patient_data)  # Load existing patient data

        email_validator = QRegularExpressionValidator(QRegularExpression(r"^[\w\.-]+@[\w\.-]+\.\w+$"))
        self.email_input.setValidator(email_validator)

        contact_validator = QRegularExpressionValidator(QRegularExpression(r"^(09\d{9}|\+639\d{9})$"))
        self.contact_input.setValidator(contact_validator)
        self.contact_input.setPlaceholderText("09") # Default prefix for mobile numbers

        # Real-time validation connections
        self.first_input.textChanged.connect(lambda: self.validate_alphabets_only(self.first_input))
        self.middle_input.textChanged.connect(lambda: self.validate_alphabets_only(self.middle_input))
        self.last_input.textChanged.connect(lambda: self.validate_alphabets_only(self.last_input))
        self.address_input.textChanged.connect(lambda: self.validate_address(self.address_input))
        self.gender_combo.currentIndexChanged.connect(self.validate_gender)
        self.email_input.textChanged.connect(self.validate_email)
        self.contact_input.textChanged.connect(self.validate_contact)

    def load_patient_data(self, patient_data):
        """Load existing patient data into the form fields."""
        self.patient_input.setText(patient_data['Patient_ID'])
        self.first_input.setText(patient_data['First_Name'])
        self.middle_input.setText(patient_data['Middle_Name'])
        self.last_input.setText(patient_data['Last_Name'])
        self.address_input.setText(patient_data['Address'])
        
        gender_index = self.gender_combo.findText(patient_data['Gender'])
        if gender_index >= 0:
            self.gender_combo.setCurrentIndex(gender_index)
        
        self.contact_input.setText(patient_data['Contact_Number'])
        self.email_input.setText(patient_data['Email'])
        
        birth_date = patient_data['Birth_Date']
        if isinstance(birth_date, str):
            birth_date = QtCore.QDate.fromString(birth_date, QtCore.Qt.DateFormat.ISODate)
        self.birth_input.setDate(birth_date)

        # Load and display the patient's picture if it exists
        self.load_patient_picture(patient_data['Patient_ID'])

    def load_patient_picture(self, patient_id):
        """Load the patient's picture from the directory if it exists."""
        picture_path = os.path.join("Dentica/patient_pic", f"{patient_id}.jpg")
        if os.path.exists(picture_path):
            self.picture_path = picture_path  # Store the path for future use
            pixmap = QtGui.QPixmap(picture_path).scaled(
                150, 150,
                QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation
            )
            mask = QtGui.QBitmap(150, 150)
            mask.fill(QtCore.Qt.GlobalColor.color0)
            painter = QtGui.QPainter(mask)
            painter.setBrush(QtCore.Qt.GlobalColor.color1)
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawEllipse(0, 0, 150, 150)
            painter.end()

            pixmap.setMask(mask)
            self.picture_label.setPixmap(pixmap)
            

    def validate_alphabets_only(self, field):
        text = field.text().strip()
        # Regex: one or more letters or spaces, but not empty
        if not text or not re.fullmatch(r"[A-Za-z ]+", text):
            field.setStyleSheet("border: 2px solid red;")
            QToolTip.showText(field.mapToGlobal(field.rect().bottomLeft()), "Only alphabets and spaces are allowed!", field)
            return False
        else:
            field.setStyleSheet("")
            return True


    def validate_address(self, field):
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

    def select_picture(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if file_dialog.exec():
            file_names = file_dialog.selectedFiles()
            if file_names:
                self.picture_path = file_names[0]
                orig = QtGui.QPixmap(self.picture_path).scaled(
                    150, 150,
                    QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation
                )

                mask = QtGui.QBitmap(150, 150)
                mask.fill(QtCore.Qt.GlobalColor.color0)
                painter = QtGui.QPainter(mask)
                painter.setBrush(QtCore.Qt.GlobalColor.color1)
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(0, 0, 150, 150)
                painter.end()

                orig.setMask(mask)
                self.picture_label.setPixmap(orig)
   
    def on_add_pressed(self):   

        # Collect validation results
        first =  self.validate_alphabets_only(self.first_input)
        middle =  self.validate_alphabets_only(self.middle_input)
        last =   self.validate_alphabets_only(self.last_input)
        address = self.address_input.text().strip()
        gender_selected = self.gender_combo.currentIndex() != 0
        email_valid = self.email_input.hasAcceptableInput()
        contact_valid = self.contact_input.hasAcceptableInput()

        # Check for any invalid field
        if not (first and middle and last and address and gender_selected and email_valid and contact_valid):
            QtWidgets.QMessageBox.warning(
                self,
                "Validation Error",
                "Please fill in all required fields with valid data before submitting."
            )
            return

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

        success = insert_patient(self, patient_id, first_name, middle_name, last_name, gender, birth_date, contact_number, email, address)
        if success:
            self.copy_patient_picture(patient_id)  # Copy the picture after adding the patient
            self.patient_added.emit()
            QMessageBox.information(self, "Success", "Patient added successfully!")
            self.accept()  

    def copy_patient_picture(self, patient_id):
        if self.picture_path:
            destination_dir = "Dentica/patient_pic/"
            destination_path = os.path.join(destination_dir, f"{patient_id}.jpg")  # save as .jpg

            # Ensure the destination directory exists
            os.makedirs(destination_dir, exist_ok=True)

            # Copy and rename the picture
            try:
                shutil.copy(self.picture_path, destination_path)
                print(f"Picture copied to {destination_path}")
            except Exception as e:
                print(f"Error copying picture: {e}")

    def update_patient(self):
        
        # Collect validation results
        first =  self.validate_alphabets_only(self.first_input)
        middle =  self.validate_alphabets_only(self.middle_input)
        last =   self.validate_alphabets_only(self.last_input)
        address = self.address_input.text().strip()
        gender_selected = self.gender_combo.currentIndex() != 0
        email_valid = self.email_input.hasAcceptableInput()
        contact_valid = self.contact_input.hasAcceptableInput()

        # Check for any invalid field
        if not (first and middle and last and address and gender_selected and email_valid and contact_valid):
            QtWidgets.QMessageBox.warning(
                self,
                "Validation Error",
                "Please fill in all required fields with valid data before submitting."
            )
            return
        
        patient_id = self.patient_input.text()
        first_name = self.first_input.text()
        middle_name = self.middle_input.text()
        last_name = self.last_input.text()
        gender = self.gender_combo.currentText() if self.gender_combo.currentIndex() > 0 else ""
        birth_date = self.birth_input.date().toString(QtCore.Qt.DateFormat.ISODate)
        contact_number = self.contact_input.text()
        email = self.email_input.text()
        address = self.address_input.text()



        success = update_patient(self,
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
            if self.picture_path:
                self.copy_patient_picture(patient_id)
            self.patient_added.emit()
            QMessageBox.information(self, "Success", "Patient updated successfully!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to update patient.")
    