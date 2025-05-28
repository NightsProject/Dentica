from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import QRegularExpression, pyqtSignal, QDateTime
from ui.Dialogues.ui_billing_dialog import Add_Payment
from backend.billing_comp import get_billing_by_payment_id, update_payment_record
from PyQt6.QtWidgets import QMessageBox
class Billing_Dialog_Ctr(Add_Payment):
    payment_added = pyqtSignal()

    def __init__(self, payment_id, parent=None):
        super().__init__(parent)
        self.payment_id = payment_id

        data = get_billing_by_payment_id(payment_id)
        if not data:
            return

        payment_id_val, patient_name, appointment_id, total_amount, method, status, payment_date = data

        self.payment_input.setText(payment_id_val)
        self.patient_input.setText(patient_name)
        self.appointment_input.setText(appointment_id)
        self.total_input.setText(f"{total_amount:.2f}")
        self.method_input.setCurrentText(method)
        self.status_input.setCurrentText("Paid")

        # Set the date input
        if payment_date:
            qdt = QDateTime.fromString(payment_date.strftime("%Y-%m-%d %H:%M:%S"), "yyyy-MM-dd HH:mm:ss")
        else:
            qdt = QDateTime.currentDateTime()
        self.date_input.setDateTime(qdt)

        # Control field editability based on status
        is_paid = (status == "Paid")

        self.payment_input.setReadOnly(True)
        self.patient_input.setReadOnly(True)
        self.appointment_input.setReadOnly(True)
        self.total_input.setReadOnly(True)
        self.date_input.setReadOnly(not is_paid)
        self.status_input.setEnabled(True)
        self.method_input.setEnabled(True)
        
        if status == "Unpaid":
            self.save.clicked.connect(self.pay)
            self.cancel_btn.clicked.connect(self.cancel)
        else:
            self.save.clicked.connect(self.update)
            self.cancel_btn.clicked.connect(self.cancel_update)

    def cancel(self):
        reply = QMessageBox.question(
            self,
            "Confirm Cancel",
            "Are you sure you want to cancel Paying this Billing?\nAll unsaved information will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.reject()
       
    def cancel_update(self):
        reply = QMessageBox.question(
            self,
            "Confirm Cancel",
            "Are you sure you want to cancel updating this Billing?\nAll unsaved information will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.reject()
            
    def pay(self):
        method = self.method_input.currentText()

        if method == "None":
            QtWidgets.QMessageBox.warning(self, "Payment Error", "Please select a valid payment method before proceeding.")
            return

        # Force payment status to 'Paid'
        status = self.status_input.currentText()
        if status == "Unpaid":
            QtWidgets.QMessageBox.warning(self, "Payment Error", "Please select a valid payment status before proceeding.")
            return

        payment_date = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")

        # Update the backend
        success = update_payment_record(
            payment_id=self.payment_id,
            method=method,
            status=status,
            payment_date=payment_date
        )

        if success:
            QtWidgets.QMessageBox.information(self, "Payment Successful", "The billing has been marked as paid.")
            self.payment_added.emit()
            self.close()
        else:
            QtWidgets.QMessageBox.critical(self, "Database Error", "Failed to record the payment.")

    def update(self):
        method = self.method_input.currentText()
        status = self.status_input.currentText()
        payment_date = self.date_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")

        if status == "Unpaid" and method != "None":
            QtWidgets.QMessageBox.warning(self, "Update Error", "Cannot set status to Unpaid with a payment method selected.")
            return
          
        if status == "Paid" and method == "None":
            QtWidgets.QMessageBox.warning(self, "Update Error", "Cannot set status to Paid with a None payment method selected.")
            return
            
        # Update the backend 
        success = update_payment_record(
            payment_id=self.payment_id,
            method=method,
            status=status,
            payment_date=payment_date
        )

        if success:
            QtWidgets.QMessageBox.information(self, "Success", "Billing information updated.")
            self.payment_added.emit()
            self.close()
        else:
            QtWidgets.QMessageBox.critical(self, "Database Error", "Failed to update billing info.")
