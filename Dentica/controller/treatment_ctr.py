from PyQt6.QtCore import pyqtSignal
from ui.Dialogues.ui_treatment_dialog import Add_Treatment

class Treatment_Dialog_Ctr(Add_Treatment):
    
    treatment_added = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.cost_input.setText("0.00")
        
        self.add_btn.clicked.connect(self.on_add_treatment_clicked)
        self.cancel_btn.clicked.connect(self.reject)

    def on_add_treatment_clicked(self):
        treatment_data = {
            "Treatment_ID": self.treat_id_input.text(),
            "Diagnosis": self.diagnosis_input.text(),
            "Cost": float(self.cost_input.text()),
            "Treatment_Procedure": self.procedure_input.text(),
            "Treatment_Date_Time": self.sched_input.dateTime().toPyDateTime(),
            "Treatment_Status": self.treat_status.currentText()
        }
        self.treatment_added.emit(treatment_data)  # 🚀 Emit the signal
        print("Treatment data emitted:", treatment_data)    
        self.close()
        
        #ToDO
        #notify in the login panel for succesful or failed connection
        #database created succesfully if not exists
        #TODO Validation to all fields in treatments form
  
       
            