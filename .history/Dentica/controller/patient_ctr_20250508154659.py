from PyQt6.QtCore import pyqtSignal
from ui.Dialogues.ui_patient_dialog import Add_Patient

class Patient_Dialog_Ctr(Add_Patient):
    
    patientCredentials = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.add_patient.clicked.connect(self.on_add_pressed)
        
    def on_add_pressed(self):
        print("Patient Added")