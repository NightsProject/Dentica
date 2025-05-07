from PyQt6.QtCore import pyqtSignal
from ui.Dialogues.ui_database_dialog import User_Login

class User_Dialog_Ctr(User_Login):
    
    userCredentials = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.log_btn.clicked.connect(self.on_login_pressed)
        
    def on_login_pressed(self):
        user = self.user_input.text()
        password = self.pass_input.text()
        
        self.userCredentials.emit(user, password)
        
        #ToDO
        #notify in the login panel for succesful or failed connection
        #database created succesfully if not exists
            
  
       
            