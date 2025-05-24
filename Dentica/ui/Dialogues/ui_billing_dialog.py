from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt

class Add_Payment(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        self.setWindowTitle("Add Payment")
        self.setFixedSize(400, 450)

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

        self.Payform = QtWidgets.QLabel("Payment Form", self)
        self.Payform.setGeometry(20, 20, 200, 25)
        self.Payform.setStyleSheet("color: #fff; font-family: Katarine; font-size: 20px; font-weight: bold;")
        

        def add_row(row, text, widget):
            y = row_start + row * row_height
            label = QtWidgets.QLabel(text, self)
            label.setGeometry(x_label, y, 120, 20)
            label.setStyleSheet(label_style)
            widget.setGeometry(x_input, y, 160, 22)

        self.payment_input = QtWidgets.QLineEdit(self)
        add_row(0, "Payment ID:", self.payment_input)

        self.patient_input = QtWidgets.QLineEdit(self)
        add_row(1, "Patient Name:", self.patient_input)

        self.appointment_input = QtWidgets.QLineEdit(self)
        add_row(2, "Appointment ID:", self.appointment_input)

        self.total_input = QtWidgets.QLineEdit(self)
        add_row(3, "Amount:", self.total_input)

        self.method_input = QtWidgets.QLineEdit(self)
        add_row(4, "Payment Method:", self.method_input)
        
        self.status_input = QtWidgets.QComboBox(self)
        self.status_input.addItems(["Select Status", "Paid", "Unpaid"])
        
        add_row(5, "Payment Status:", self.status_input)

        self.date_input = QtWidgets.QDateEdit(self)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QtCore.QDate.currentDate())
        add_row(6, "Payment Date:", self.date_input)
        
        self.add_patient = QtWidgets.QPushButton("Add", self)
        self.add_patient.setGeometry(120, 380, 80, 30)
        self.add_patient.setStyleSheet("background-color: #37547A; color: #fff;")

        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(210, 380, 80, 30)
        self.cancel_btn.setStyleSheet("""
            QPushButton {background-color: #37547A; color: #fff;}
            QPushButton:hover {background-color: #fff; color: #000;}
        """)
        self.cancel_btn.clicked.connect(self.reject)