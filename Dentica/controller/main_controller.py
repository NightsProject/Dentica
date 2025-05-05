#format: class

from PyQt6.QtWidgets import QMainWindow
from ui.ui_main_window import Ui_MainWindow

from controller.database_dialog_ctr import Database_Dialog_Ctr
from backend.DB import connectDBF, set_credentials, createAllTables
from backend.dashboard_comp import load_summary

class MainController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
     
        self.userbtn.clicked.connect(lambda: self.open_login_popup())
    

    def open_login_popup(self):
        login_popup = Database_Dialog_Ctr()
        login_popup.credentialsSubmitted.connect(self.handle_credentials)
        login_popup.exec()
    
    def update_summary(self, data):
        self.label_5.setText(str(data[0]))
        self.label_6.setText(str(data[1]))
        self.label_7.setText(str(data[2]))
        self.label_9.setText(str(data[3]))


    def handle_credentials(self, host, user, password, databaseName):
        print(f"Received credentials: host={host}, user={user}, password={password}, databse name={databaseName}")
        
        connection = connectDBF(host, user, password, databaseName)
        if connection:
            print(f"Successfully connected to {databaseName} database")

            set_credentials(host, user, password, databaseName) # later for global use 
            
            createAllTables(connection)
            
            data = load_summary() 
            self.update_summary(data)
            
        else:
            print("Failed to connect to the database.")
            
        #ToDO
        #Notify to gui
 