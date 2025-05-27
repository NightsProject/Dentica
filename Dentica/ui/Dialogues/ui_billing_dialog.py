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

        self.dark_mode = False
        
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

        self.method_input = QtWidgets.QComboBox(self)
        self.method_input.addItems(["None", "Cash", "Gcash"])
        add_row(4, "Payment Method:", self.method_input)
        
        self.status_input = QtWidgets.QComboBox(self)
        self.status_input.addItems(["Paid", "Unpaid"])
        
        add_row(5, "Payment Status:", self.status_input)

        self.date_input = QtWidgets.QDateEdit(self)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QtCore.QDate.currentDate())
        add_row(6, "Payment Date:", self.date_input)
        

        self.save = QtWidgets.QPushButton("Save", self)
        self.save.setGeometry(120, 380, 80, 30)
        self.save.setStyleSheet("background-color: #37547A; color: #fff;")


        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(210, 380, 80, 30)
        self.cancel_btn.setStyleSheet("""
            QPushButton {background-color: #37547A; color: #fff;}
            QPushButton:hover {background-color: #fff; color: #000;}
        """)
        self.cancel_btn.clicked.connect(self.reject)
        self.apply_theme()
        
    def apply_theme(self):
        if self.dark_mode:
            # Dark theme colors
            bg_color = "#2D2D2D"
            text_color = "#FFFFFF"
            card_bg = "#3D3D3D"
            button_bg = "#37547A"
            header_bg = "#1F1F21"
            header_text = "#FFFFFF"
        else:
            # Light theme colors
            bg_color = "#B2CDE9"
            text_color = "#37547A"
            card_bg = "#C6D7EC"
            button_bg = "#37547A"
            header_bg = "#1F1F21"
            header_text = "#FFFFFF"

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
                border: 1px solid #fff;
                border-radius: 5px;
            }}
            QLabel {{
                color: {text_color};
                font-family: Inter;
                font-size: 14px;
            }}
            QLineEdit, QComboBox, QDateEdit {{
                background-color: {card_bg};
                color: {text_color};
                border: 1px solid {card_bg};
                border-radius: 3px;
                padding: 2px 5px;
            }}
            QPushButton {{
                background-color: {button_bg};
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px 10px;
            }}
            QPushButton:hover {{
                background-color: #8DB8E0;
            }}
        """)

        for child in self.findChildren(QtWidgets.QLabel):
            child.setStyleSheet(f"""
                    color: {text_color};
                    font-family: Inter;
                    font-size: 14px;
            """)
    