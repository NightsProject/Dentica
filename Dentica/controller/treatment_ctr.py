from PyQt6.QtCore import pyqtSignal
from ui.Dialogues.ui_treatment_dialog import Add_Treatment

class Treatment_Dialog_Ctr(Add_Treatment):
    
    credentialsSubmitted = pyqtSignal(str, str, str, str, str)

    def __init__(self):
        super().__init__()
        self.add_btn.clicked.connect(self.on_login_pressed)
        
    def on_login_pressed(self):
        id = self.treat_id_input.text()
        diagnosis = self.diagnosis_input.text()
        procedure = self.procedure_input.text()
        schedule = self.sched_input.dateTime()
        cost = self.cost_input.text()
        
        self.credentialsSubmitted.emit(id, diagnosis, procedure, schedule, cost)
        
        #ToDO
        #notify in the login panel for succesful or failed connection
        #database created succesfully if not exists
            
  
       
            