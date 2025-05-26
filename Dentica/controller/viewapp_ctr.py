from PyQt6.QtCore import pyqtSignal
from ui.Dialogues.ui_viewapp_dialog import View_Appointment
from backend.appointments_comp import get_appointment_data
from PyQt6 import QtWidgets

class View_Appointent_Ctr(View_Appointment):
    
    view_app_reload = pyqtSignal()
    
    def __init__(self, appointment_id):
        super().__init__()
        
        self.load_appointment_data(appointment_id)
        
    def load_appointment_data(self, appointment_id):
        data = get_appointment_data(appointment_id)
        if not data:
            QtWidgets.QMessageBox.warning(self, "Error", "Appointment not found.")
            return

        # Fill basic fields
        self.appointment_input.setText(str(data['Appointment_ID']))
        self.patient_input.setText(data['Patient_Name'])
        self.schedule_input.setText(data['Schedule'])
        self.status_input.setText(data['Status'])
        
        # Set payment info
        payment = data.get("Payment", {})
        self.payment_id.setText(payment.get("Payment_ID", "N/A"))
        self.payment_stat.setText(payment.get("Payment_Status", "N/A"))

        total_amount = payment.get("Total_Amount")
        self.Cost_line.setText(f"${total_amount:,.2f}" if total_amount is not None else "N/A")

        
        # Fill treatment table
        treatments = data.get('Treatments', [])
        self.Treat_table.setRowCount(len(treatments))
        for row, treatment in enumerate(treatments):
            self.Treat_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(treatment['Treatment_ID'])))
            self.Treat_table.setItem(row, 1, QtWidgets.QTableWidgetItem(treatment['Diagnosis']))
            self.Treat_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(treatment['Treatment_Date_Time'])))
            self.Treat_table.setItem(row, 3, QtWidgets.QTableWidgetItem(treatment['Treatment_Procedure']))
            self.Treat_table.setItem(row, 4, QtWidgets.QTableWidgetItem(treatment['Treatment_Status']))
            self.Treat_table.setItem(row, 5, QtWidgets.QTableWidgetItem(f"P{treatment['Cost']}"))

            


            