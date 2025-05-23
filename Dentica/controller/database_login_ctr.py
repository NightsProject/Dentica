from PyQt6.QtCore import pyqtSignal
from ui.Dialogues.ui_database_dialog import Database_Login

class Database_Dialog_Ctr(Database_Login):
    
    credentialsSubmitted = pyqtSignal(str, str, str, str, str)

    def __init__(self):
        super().__init__()
        self.login_btn.clicked.connect(self.on_login_pressed)
        
    def on_login_pressed(self):
        host = self.host_input.text()
        port = self.port_input.text()
        user = self.username_input.text()
        password = self.password_input.text()
        databaseName = self.dbname_input.text()
        
        self.credentialsSubmitted.emit(host, port, user, password, databaseName)
        self.close()
        
        #ToDO
        #notify in the login panel for succesful or failed connection
        #database created succesfully if not exists
            
  
       
            