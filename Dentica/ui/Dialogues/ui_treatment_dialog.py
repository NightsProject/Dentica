from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt

class Add_Treatment(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Add Treatment")
        self.setFixedSize(350, 400)
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

        self.header = QtWidgets.QLabel("Treatment Form", self)
        self.header.setGeometry(20, 20, 250, 25)
        self.header.setStyleSheet("color: #fff; font-family: Katarine; font-size: 20px; font-weight: bold;")

        def add_row(row, text, widget):
            y = row_start + row * row_height
            label = QtWidgets.QLabel(text, self)
            label.setGeometry(x_label, y, 120, 20)
            label.setStyleSheet(label_style)
            widget.setGeometry(x_input, y, 160, 22)

        self.treat_id_input = QtWidgets.QLineEdit(self)
        add_row(0, "Treatment ID:", self.treat_id_input)

        self.diagnosis_input = QtWidgets.QLineEdit(self)
        add_row(1, "Diagnosis:", self.diagnosis_input)

        self.procedure_input = QtWidgets.QLineEdit(self)
        add_row(2, "Procedure:", self.procedure_input)

        self.sched_input = QtWidgets.QDateTimeEdit(self)
        self.sched_input.setCalendarPopup(True)
        self.sched_input.setDateTime(QtCore.QDateTime.currentDateTime())
        add_row(3, "Schedule:", self.sched_input)

        self.cost_input = QtWidgets.QLineEdit(self)
        add_row(4, "Cost:", self.cost_input)

        self.treat_status = QtWidgets.QComboBox(self)
        self.treat_status.addItems(["Completed","In-Progress","Waiting","Canceled"])
        add_row(5, "Status:", self.treat_status)
        self.treat_status.setStyleSheet("background-color: #fff; color: #000;")
        self.treat_status.setGeometry(x_input, row_start + 5 * row_height, 160, 22)
        self.treat_status.setCurrentText("Waiting")
        self.treat_status.setStyleSheet("background-color: #fff; color: #000;")
     
        self.add_btn = QtWidgets.QPushButton("Add", self)
        self.add_btn.setGeometry(80, 340, 80, 30)
        self.add_btn.setStyleSheet("background-color: #37547A; color: #fff;")

        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(170, 340, 80, 30)
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
