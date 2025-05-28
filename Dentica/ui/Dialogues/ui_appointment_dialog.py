from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QAbstractItemView
from PyQt6.QtCore import Qt
from controller.treatment_ctr import Treatment_Dialog_Ctr
from controller.patient_ctr import Patient_Dialog_Ctr

class Add_Appointment(QtWidgets.QDialog):
    def __init__(self, parent=None, appointment_data=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Book Appointment")
        self.setFixedSize(720, 600)
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
        input_x = 150
        label_x = 20
        row_height = 40
        row_start = 60

        self.header = QtWidgets.QLabel("Appointment Form", self)
        self.header.setGeometry(20, 20, 300, 25)
        self.header.setStyleSheet("""color: #fff; font-family: Katarine; font-size: 20px; font-weight: bold;""")

        def add_row(row, text, widget):
            y = row_start + row * row_height
            label = QtWidgets.QLabel(text, self)
            label.setGeometry(label_x, y, 120, 20)
            label.setStyleSheet(label_style)
            widget.setGeometry(input_x, y, 160, 22)

        self.appointment_input = QtWidgets.QLineEdit(self)
        self.appointment_input.setReadOnly(True)
        add_row(0, "Appointment ID:", self.appointment_input)

        self.patient_input = QtWidgets.QComboBox(self)
        self.patient_input.setEditable(True)
        self.patient_input.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        add_row(1, "Patient Name:", self.patient_input)
        self.patient_input.lineEdit().textChanged.connect(self.update_patient_search)


        self.AddPatient_btn = QtWidgets.QPushButton("Add Patient", self)
        self.AddPatient_btn.setGeometry(400, row_start + 1 * row_height, 120, 30)
        self.AddPatient_btn.setStyleSheet("background-color: #37547A; color: #fff;")
        self.AddPatient_btn.clicked.connect(self.open_patient)

        self.schedule_input = QtWidgets.QDateTimeEdit(self)
        self.schedule_input.setCalendarPopup(True)
        self.schedule_input.setDateTime(QtCore.QDateTime.currentDateTime())
        add_row(2, "Schedule:", self.schedule_input)

        self.status_input = QtWidgets.QComboBox(self)
        self.status_input.setGeometry(input_x, row_start + 3 * row_height, 160, 22)
        self.status_input.addItems(["Select Status", "Scheduled", "Completed", "Cancelled"])
        
        label = QtWidgets.QLabel("Status:", self)
        label.setGeometry(label_x, row_start + 3 * row_height, 120, 20)
        label.setStyleSheet(label_style)
        
        self.AddTreat_btn = QtWidgets.QPushButton("Add Treatment", self)
        self.AddTreat_btn.setGeometry(400, row_start + 3 * row_height, 120, 30)
        self.AddTreat_btn.setStyleSheet("background-color: #37547A; color: #fff;")
      
        self.Treat_table = QtWidgets.QTableWidget(self)
        self.Treat_table.setGeometry(20, 220, 680, 280)
        self.Treat_table.setColumnCount(7)
        self.Treat_table.setHorizontalHeaderLabels(["TreatmentID","Diagnosis","Date & Time", "Procedure","Status", "Cost", "Actions"])
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
        header = self.Treat_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents) # TreatmentID
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)          # Diagnosis
        
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents) # Date&Time
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Stretch)          # Procedure
        
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents) # Status
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.ResizeToContents) # Cost
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeMode.Fixed)            # Actions
        
        self.Treat_table.setColumnWidth(6, 100)
        self.Treat_table.verticalHeader().setVisible(False)
        self.Treat_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.Treat_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.Treat_table.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        
        self.total_label = QtWidgets.QLabel("Total Bill:", self)
        self.total_label.setGeometry(20, 510, 120, 20)
        self.total_label.setStyleSheet("color: #37547A; font-family: Inter; font-size: 14px;")

        self.total_input = QtWidgets.QLineEdit(self)
        self.total_input.setGeometry(80, 510, 160, 22)
        self.total_input.setReadOnly(True)
        self.total_input.setStyleSheet("background-color: #fff; color: #37547A;")

        self.add_btn = QtWidgets.QPushButton("Add", self)
        self.add_btn.setGeometry(200, 550, 80, 30)
        self.add_btn.setStyleSheet("background-color: #37547A; color: #fff;")

        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.cancel_btn.setGeometry(310, 550, 80, 30)
        self.cancel_btn.setStyleSheet("""
            QPushButton {background-color: #37547A; color: #fff;}
            QPushButton:hover {background-color: #fff; color: #000;}
        """)
        self.apply_theme()
        if appointment_data:
            self.populate_fields(appointment_data)
            
    def populate_fields(self, appointment_data):
        self.appointment_input.setText(appointment_data['Appointment_ID'])
        self.appointment_input.setReadOnly(True)
        
        # Set patient
        patient_name = appointment_data.get('Patient_Name', '')
        self.patient_input.setCurrentText(patient_name)
        
        # Set schedule
        schedule = QtCore.QDateTime.fromString(appointment_data['Schedule'], QtCore.Qt.DateFormat.ISODate)
        self.schedule_input.setDateTime(schedule)
        
        # Set status
        status_index = self.status_input.findText(appointment_data['Status'])
        if status_index >= 0:
            self.status_input.setCurrentIndex(status_index)
        
        # Clear existing treatments and add new ones
        self.treatments = appointment_data.get('Treatments', [])
        self.Treat_table.setRowCount(0)
        for treatment in self.treatments:
            self.update_treatments_table_ui()

    def open_patient(self):
        patient_popup = Patient_Dialog_Ctr()
        patient_popup.dark_mode = self.dark_mode
        patient_popup.apply_theme()
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

    def apply_theme(self):
        if self.dark_mode:
            # Dark theme colors
            bg_color = "#2D2D2D"
            text_color = "#FFFFFF"
            card_bg = "#3D3D3D"
            card_bd = "gray"
            button_bg = "#37547A"
            header_bg = "#1F1F21"
            select = "light gray"
            header_text = "#FFFFFF"
        else:
            # Light theme colors
            bg_color = "#B2CDE9"
            text_color = "#37547A"
            card_bg = "#C6D7EC"
            card_bd = "#fff"
            button_bg = "#37547A"
            header_bg = "#1F1F21"
            select = "#88A9C9"
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
            QLineEdit, QComboBox, QDateTimeEdit {{
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
        
        
        
        self.Treat_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {bg_color};
                color: {text_color};
                gridline-color: {bg_color};
                border: 1px solid {card_bd};
                font-family: Inter;
                font-size: 13px;
            }}
            QHeaderView::section {{
            background-color: {bg_color};
            color: {text_color};
            font-weight: bold;
            border: none;
            padding: 4px;
            margin: 0px;
            }}
            QTableWidget::item:selected {{
                background-color: {select};
                color: white;
            }}
        """)

        for child in self.findChildren(QtWidgets.QLabel):
            if child != self.header:  # Skip the header we already styled
                child.setStyleSheet(f"""
                    color: {text_color};
                    font-family: Inter;
                    font-size: 14px;
            """)
    