from PyQt6.QtCore import pyqtSignal
from ui.Dialogues.ui_patient_dialog import Add_Patient

class Patient_Dialog_Ctr(Add_Patient):
    
    userCredentials = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.log_btn.clicked.connect(self.on_add_pressed)
        
    def on_add_pressed(self):
        user = self.user_input.text()
        password = self.pass_input.text()
        
        self.userCredentials.emit(user, password)