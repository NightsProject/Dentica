from PyQt6.QtCore import pyqtSignal
from ui.Dialogues.ui_database_dialog import Add_Appointment

class Appointment_Dialog_Ctr(Add_Appointment):
    
    appointment_details = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.login_btn.clicked.connect(self.on_login_pressed)
        
    def on_login_pressed(self):
        app_id = self.appointment_input.text()
        pat_id = self.patient_input.text()
        sched = self.schedule.text()

        
        self.appointment_details.emit(app_id, pat_id, sched)