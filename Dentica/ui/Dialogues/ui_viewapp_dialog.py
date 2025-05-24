from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from controller.patient_ctr import Patient_Dialog_Ctr

class View_Appointment(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Book Appointment")
        self.setFixedSize(670, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #B2CDE9;
                border: 1px solid #fff;
                border-radius: 5px;
            }
        """)
        self.oldPos = None

        label_style = "color: #37547A; font-family: Inter; font-size: 14px;"
        input_x = 150
        label_x = 20
        
        second_col_label_x = 360
        second_col_input_x = 490
        
        row_height = 33
        row_start = 60

        self.header = QtWidgets.QLabel("Appointment Details", self)
        self.header.setGeometry(20, 20, 300, 25)
        self.header.setStyleSheet("color: #fff; font-family: Katarine; font-size: 20px; font-weight: bold;")

        def add_row(row, text, widget,label_x, input_x):
            y = row_start + row * row_height
            label = QtWidgets.QLabel(text, self)
            label.setGeometry(label_x, y, 120, 20)
            label.setStyleSheet(label_style)
            widget.setGeometry(input_x, y, 160, 22)

        self.appointment_input = QtWidgets.QLineEdit(self)
        self.appointment_input.setText("Fetch appointment ID")
        self.appointment_input.setReadOnly(True)
        add_row(0, "Appointment ID:", self.appointment_input,label_x, input_x)

        self.patient_input = QtWidgets.QLineEdit(self)
        self.patient_input.setText("Fetch Patient Name")
        self.patient_input.setReadOnly(True)
        add_row(1, "Patient Name:", self.patient_input, label_x, input_x)

        self.schedule_input = QtWidgets.QLineEdit(self)
        self.schedule_input.setText("Fetch Schedule")
        self.schedule_input.setReadOnly(True)
        add_row(2, "Schedule:", self.schedule_input, label_x, input_x)

        self.status_input = QtWidgets.QLineEdit(self)
        self.status_input.setText("Fetch Status")
        self.status_input.setReadOnly(True)
        add_row(0, "Status:", self.status_input, second_col_label_x, second_col_input_x)

        self.payment_id = QtWidgets.QLineEdit(self)
        self.payment_id.setText("Fetch Payment ID")
        self.payment_id.setReadOnly(True)
        add_row(1, "Payment ID:", self.payment_id, second_col_label_x, second_col_input_x)

        self.payment_stat = QtWidgets.QLineEdit(self)
        self.payment_stat.setText("Fetch Payment Status")
        self.payment_stat.setReadOnly(True)
        add_row(2, "Payment Status:", self.payment_stat, second_col_label_x, second_col_input_x)

        self.Treat_label = QtWidgets.QLabel("Treatment List", self)
        self.Treat_label.setGeometry(20, 165, 120, 20)
        self.Treat_label.setStyleSheet("color: #37547A; font-family: Inter; font-size: 15px;")

        self.Treat_table = QtWidgets.QTableWidget(self)
        self.Treat_table.setGeometry(20, 195, 630, 210)
        self.Treat_table.setColumnCount(6)
        self.Treat_table.setHorizontalHeaderLabels(["TreatmentID","Diagnosis","Date & Time", "Procedure","Status", "Cost"])
        self.Treat_table.setStyleSheet("""
            QTableWidget {
                background-color: #B2CDE9;
                color: #37547A;
                gridline-color: #A0BFD8;
                border: 1px solid #fff;
                font-family: Inter;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #A0BFD8;
                color: #37547A;
                font-weight: bold;
                border: none;
                padding: 4px;
                margin: 0px;
            }
            QTableWidget::item:selected {
                background-color: #88A9C9;
                color: white;
            }
        """)
        self.Treat_table.setRowCount(0)
        self.Treat_table.horizontalHeader().setContentsMargins(0, 0, 0, 0)
        self.Treat_table.horizontalHeader().setStyleSheet("margin: 0px; padding: 0px;")
        
        self.Total_cost = QtWidgets.QLabel("Total Cost:", self)
        self.Total_cost.setGeometry(20, 420, 120, 20)
        self.Total_cost.setStyleSheet("color: #37547A; font-family: Inter; font-size: 15px;")
        
        self.Cost_line = QtWidgets.QLineEdit(self)
        self.Cost_line.setText("Fetch Total Cost")
        self.Cost_line.setReadOnly(True)
        self.Cost_line.setGeometry(150, 420, 160, 22)

        self.exit_btn = QtWidgets.QPushButton("Exit", self)
        self.exit_btn.setGeometry(300, 455, 80, 30)
        self.exit_btn.setStyleSheet("""
            QPushButton {background-color: #37547A; color: #fff;}
            QPushButton:hover {background-color: #fff; color: #000;}
        """)
        self.exit_btn.clicked.connect(self.reject)

    def open_patient(self):
        patient_popup = Patient_Dialog_Ctr()
        patient_popup.exec()

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
