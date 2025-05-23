from ui.Patients_Page import PatientPage
from backend.patient_page_comp import get_all_patient_records

class Patient_Page_Ctr(PatientPage):
    
    def __init__(self, stacked_widget):
        super().__init__(stacked_widget)
        self.Pages = stacked_widget
    
    def load_patient_infos(self, patient_id):
        data = get_all_patient_records(patient_id)
        patient_info = data.get("info", None)
        if patient_info:
            patient_id, full_name, gender, birth_date, contact_number, email, address = patient_info
            
            # split the full name into parts
            name_parts = full_name.split()
            first_name = name_parts[0] if len(name_parts) > 0 else ""
            middle_name = name_parts[1] if len(name_parts) > 2 else ""
            last_name = name_parts[-1] if len(name_parts) > 0 else ""
            # Convert birth_date to string
            birth_date_str = str(birth_date) if birth_date else ""
            # Set the values 
            self.pat_id.setText(str(patient_id))
            self.pat_name.setText(full_name or "Unknown")
            self.fnval.setText(first_name)
            self.mnval.setText(middle_name)
            self.lndval.setText(last_name)
            self.genval.setText(gender or "")
            self.bdval.setText(birth_date_str)
            self.condval.setText(contact_number or "")
            self.emailval.setText(email or "")
            self.adval.setText(address or "")
        else:
            # Clear or set empty in case no data found
            self.pat_id.setText("N/A")
            self.pat_name.setText("Unknown")
            self.fnval.setText("")
            self.mnval.setText("")
            self.lndval.setText("")
            self.genval.setText("")
            self.bdval.setText("")
            self.condval.setText("")
            self.emailval.setText("")
            self.adval.setText("")
            
        #TODO get the picture and load it to the profile page