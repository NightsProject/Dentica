from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMessageBox
from ui.Dialogues.ui_database_dialog import Database_Login
import sys

class Database_Dialog_Ctr(Database_Login):
    
    credentialsSubmitted = pyqtSignal(str, str, str, str, str, bool)

    def __init__(self, first_login=False):
        super().__init__()
        self.first_login = first_login

        self.login_btn.clicked.connect(self.on_login_pressed)
        self.cancel_btn.clicked.connect(self.on_cancel_pressed)

    def on_login_pressed(self):
        host = self.host_input.text().strip()
        port = self.port_input.text().strip()
        user = self.username_input.text().strip()
        password = self.password_input.text().strip()
        database_name = self.dbname_input.text().strip()

        # Input validation
        if not all([host, port, user, password, database_name]):
            QMessageBox.warning(self, "Missing Fields", "Please fill in all fields.")
            return  # Do NOT close or accept dialog

        if not port.isdigit():
            QMessageBox.warning(self, "Invalid Port", "Port must be numeric.")
            return

        # Inputs valid → emit signal and close dialog
        self.credentialsSubmitted.emit(host, port, user, password, database_name, False)
        self.accept() 

    def on_cancel_pressed(self):
        if self.first_login:
            reply = QMessageBox.question(
                self, "Confirm Exit",
                "Are you sure you want to cancel and exit the application?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                sys.exit(0)
        else:
            self.reject()  # Close the dialog without exiting app
