from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt

class Add_Patient(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Add Patient")
        self.setFixedSize(350, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #B2CDE9;
                border: 1px solid #fff;
                border-radius: 5px;
            }
        """)
        self.oldPos = None

        label_style = "color: #37547A; font-family: Inter; font-size: 14px;"
        x_label = 20
        x_input = 150
        row_height = 40
        row_start = 60

        self.PatientForm = QtWidgets.QLabel("Patient Form", self)
        self.PatientForm.setGeometry(20, 20, 200, 25)
        self.PatientForm.setStyleSheet("color: #fff; font-family: Katarine; font-size: 20px; font-weight: bold;")

        def add_row(row, text, widget):
            y = row_start + row * row_height
            label = QtWidgets.QLabel(text, self)
            label.setGeometry(x_label, y, 120, 20)
            label.setStyleSheet(label_style)
            widget.setGeometry(x_input, y, 160, 22)

        self.patient_input = QtWidgets.QLineEdit(self)
        add_row(0, "Patient ID:", self.patient_input)

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
        self.add_patient.setGeometry(80, 440, 80, 30)
        self.add_patient.setStyleSheet("background-color: #37547A; color: #fff;")

        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(170, 440, 80, 30)
        self.cancel_btn.setStyleSheet("""
            QPushButton {background-color: #37547A; color: #fff;}
            QPushButton:hover {background-color: #fff; color: #000;}
        """)
        self.cancel_btn.clicked.connect(self.reject)

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
