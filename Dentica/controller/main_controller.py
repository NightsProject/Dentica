#format: class

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow
from ui.ui_main_window import Ui_MainWindow


from controller.database_login_ctr import Database_Dialog_Ctr
from backend.DB import connectDBF, set_credentials, createAllTables
from backend.dashboard_comp import load_summary, get_todays_appointments
from backend.patients_comp import get_all_patients

class MainController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
     
        self.userbtn.clicked.connect(lambda: self.open_login_popup())
    

    def open_login_popup(self):
        login_popup = Database_Dialog_Ctr()
        login_popup.credentialsSubmitted.connect(self.handle_credentials)
        login_popup.exec()
        
    #=========================================================
    #====================LOAD DATAS TO UI=============== start
    
    #DASHBOARD TAB=============== start
    def update_summary(self, data):
        self.label_5.setText(str(data[0]))
        self.label_6.setText(str(data[1]))
        self.label_7.setText(str(data[2]))
        self.label_9.setText(str(data[3]))
        
        
    def update_todays_appointments_table(self, appointments):   
        
        self.UpAp_table.setRowCount(0)
        for appointment in appointments:
            row_position = self.UpAp_table.rowCount()
            self.UpAp_table.insertRow(row_position)

            self.UpAp_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(appointment[0])))  # Patient name
            self.UpAp_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(appointment[1])))  # Time
            self.UpAp_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(appointment[2])))  # Procedure
            self.UpAp_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(appointment[3])))  # Status
            self.UpAp_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem("View"))              # Placeholder
    #DASHBOARD TAB================ end
    
    #PATIENTS TAB=================start
    def update_patients_list(self, patients):
        
        print("test")
        self.Patients_table.setRowCount(0)
        for patient in patients:
            row_position = self.Patients_table.rowCount()
            self.Patients_table.insertRow(row_position)
            self.Patients_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(patient[0])))
            self.Patients_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(patient[1])))
            self.Patients_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(patient[2])))
            self.Patients_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(patient[3])))
            self.Patients_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(patient[4])))
            self.Patients_table.setItem(row_position, 5, QtWidgets.QTableWidgetItem(str(patient[5])))
            self.Patients_table.setItem(row_position, 6, QtWidgets.QTableWidgetItem(str(patient[6])))
           
    #====================LOAD DATAS TO UI=============== end
    #=======================================================

    def handle_credentials(self, host, user, password, databaseName):
        print(f"Received credentials: host={host}, user={user}, password={password}, databse name={databaseName}")
        
        connection = connectDBF(host, user, password, databaseName)
        if connection:
            print(f"Successfully connected to {databaseName} database")

            set_credentials(host, user, password, databaseName) # later for global use 
            
            createAllTables(connection)
            
            #===========LOAD DATAS=============
            #Dashboard
            summary_data = load_summary() 
            self.update_summary(summary_data)
            
            todays_appointments_list = get_todays_appointments()
            self.update_todays_appointments_table(todays_appointments_list)
            
            all_patients_list = get_all_patients()
            self.update_patients_list(all_patients_list)
            
            
        else:
            print("Failed to connect to the database.")
            
        #ToDO
        #Notify to gui
 