from PyQt6.QtCore import pyqtSignal
from ui.Dialogues.ui_patient_dialog import Add_Patient
from backend.patients_comp import generate_new_patient_id
class Patient_Dialog_Ctr(Add_Patient):
    

    def __init__(self):
        super().__init__()
        self.add_patient.clicked.connect(self.on_add_pressed)
        
        new_id = generate_new_patient_id()
        self.patient_input.setText(new_id)
    

    def on_add_pressed(self):
        print("Patient Added")
        
        #add the patients credentials to the patient table with validations
        
        
    