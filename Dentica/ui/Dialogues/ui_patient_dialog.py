from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt

class Add_Patient(QtWidgets.QDialog):
    def __init__(self, parent=None, patient_data=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        self.setWindowTitle("Add Patient" if not patient_data else "Edit Patient")
        self.setFixedSize(550, 500)

        self.setStyleSheet("""
            QDialog {
                background-color: #B2CDE9;
                border: 1px solid #fff;
                border-radius: 5px;
            }
        """)
        self.oldPos = None
        self.patient_data = patient_data

        label_style = "color: #37547A; font-family: Inter; font-size: 14px;"
        x_label = 20
        x_input = 150
        row_height = 40
        row_start = 60

        self.PatientForm = QtWidgets.QLabel("Patient Form", self)
        self.PatientForm.setGeometry(20, 20, 200, 25)
        self.PatientForm.setStyleSheet("color: #fff; font-family: Katarine; font-size: 20px; font-weight: bold;")
        
        #Pic selector frame
        self.picture_label = QtWidgets.QLabel(self)
        self.picture_label.setGeometry(350, 100, 150, 150)
        self.picture_label.setStyleSheet("background-color: #fff; border: 1px solid #37547A;")
        self.picture_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        #add pic button
        self.picture_button = QtWidgets.QPushButton("Add Picture", self)
        self.picture_button.setGeometry(380, 260, 80, 30)
        self.picture_button.setStyleSheet("background-color: #37547A; color: #fff;")
        self.picture_button.clicked.connect(self.select_picture)
        

        self.picture_path = None

        def add_row(row, text, widget):
            y = row_start + row * row_height
            label = QtWidgets.QLabel(text, self)
            label.setGeometry(x_label, y, 120, 20)
            label.setStyleSheet(label_style)
            widget.setGeometry(x_input, y, 160, 22)

        self.patient_input = QtWidgets.QLineEdit(self)
        add_row(0, "Patient ID:", self.patient_input)
        self.patient_input.setReadOnly(True)

        self.first_input = QtWidgets.QLineEdit(self)
        add_row(1, "First Name:", self.first_input)

        self.middle_input = QtWidgets.QLineEdit(self)
        add_row(2, "Middle Name:", self.middle_input)

        self.last_input = QtWidgets.QLineEdit(self)
        add_row(3, "Last Name:", self.last_input)

        self.address_input = QtWidgets.QLineEdit(self)
        add_row(4, "Address:", self.address_input)

        self.gender_combo = QtWidgets.QComboBox(self)
        self.gender_combo.addItem("Select Gender")
        self.gender_combo.addItems(["Male", "Female", "Other"])
        self.gender_combo.setCurrentIndex(0)
        add_row(5, "Gender:", self.gender_combo)

        self.contact_input = QtWidgets.QLineEdit(self)
        add_row(6, "Contact Number:", self.contact_input)

        self.email_input = QtWidgets.QLineEdit(self)
        add_row(7, "Email:", self.email_input)

        self.birth_input = QtWidgets.QDateEdit(self)
        self.birth_input.setCalendarPopup(True)
        self.birth_input.setDate(QtCore.QDate.currentDate())
        add_row(8, "Birth Date:", self.birth_input)
        
        self.add_patient = QtWidgets.QPushButton("Add", self)
        self.add_patient.setGeometry(170, 440, 80, 30)
        self.add_patient.setStyleSheet("background-color: #37547A; color: #fff;")

        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(260, 440, 80, 30)
        self.cancel_btn.setStyleSheet("""
            QPushButton {background-color: #37547A; color: #fff;}
            QPushButton:hover {background-color: #fff; color: #000;}
        """)
        self.cancel_btn.clicked.connect(self.reject)
        
        if patient_data:
            self.populate_fields(patient_data)
    
    def populate_fields(self, patient_data):
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
        elif hasattr(birth_date, 'year'):  
            birth_date = QtCore.QDate(birth_date.year, birth_date.month, birth_date.day)
            
        self.birth_input.setDate(birth_date)
        self.birth_input.setDate(birth_date)

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