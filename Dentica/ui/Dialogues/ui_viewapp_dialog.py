from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from controller.treatment_ctr import Treatment_Dialog_Ctr
from controller.patient_ctr import Patient_Dialog_Ctr

class View_Appointment(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Book Appointment")
        self.setFixedSize(350, 600)
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
        row_height = 40
        row_start = 60

        self.header = QtWidgets.QLabel("Appointment Details", self)
        self.header.setGeometry(20, 20, 300, 25)
        self.header.setStyleSheet("""color: #fff; font-family: Katarine; font-size: 20px; font-weight: bold;""")

        def add_row(row, text, widget):
            y = row_start + row * row_height
            label = QtWidgets.QLabel(text, self)
            label.setGeometry(label_x, y, 120, 20)
            label.setStyleSheet(label_style)
            widget.setGeometry(input_x, y, 160, 22)

        self.appointment_input = QtWidgets.QLineEdit(self)
        self.appointment_input.setText("Fetch appointment ID")
        self.appointment_input.setReadOnly(True)
        add_row(0, "Appointment ID:", self.appointment_input)

        self.patient_input = QtWidgets.QLineEdit(self)
        self.patient_input.setText("Fetch Patient Name")
        self.patient_input.setReadOnly(True)
        add_row(1, "Patient Name:", self.patient_input)


        self.schedule_input = QtWidgets.QLineEdit(self)
        self.schedule_input.setText("Fetch Schedule")
        add_row(2, "Schedule:", self.schedule_input)

        self.status_input = QtWidgets.QComboBox(self)
        self.status_input.setGeometry(input_x, row_start + 3 * row_height, 160, 22)
        self.status_input.addItems(["Fetch Status", "Scheduled", "Completed", "Cancelled"])
        
        label = QtWidgets.QLabel("Status:", self)
        label.setGeometry(label_x, row_start + 3 * row_height, 120, 20)
        label.setStyleSheet(label_style)
           
        self.Treat_label = QtWidgets.QLabel("Treatment List", self)
        self.Treat_label.setGeometry(20, 220, 120, 20)
        self.Treat_label.setStyleSheet("color: #37547A; font-family: Inter; font-size: 15px;")
        self.Treat_table = QtWidgets.QTableWidget(self)
        self.Treat_table.setGeometry(20, 250, 300, 280)
        self.Treat_table.setColumnCount(4)
        self.Treat_table.setHorizontalHeaderLabels(["TreatmentID", "Procedure", "Cost", "Actions"])
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

        self.exit_btn = QtWidgets.QPushButton("Exit", self)
        self.exit_btn.setGeometry(250, 550, 80, 30)
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
