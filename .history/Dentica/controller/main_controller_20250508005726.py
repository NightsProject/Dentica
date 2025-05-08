#format: class

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow
from ui.ui_main_window import Ui_MainWindow
from PyQt6.QtWidgets import QMessageBox
import mysql.connector

from controller.database_login_ctr import Database_Dialog_Ctr
from controller.appointment_ctr import Appointment_Dialog_Ctr
from backend.DB import connectDBF, set_credentials, createAllTables
from backend.dashboard_comp import load_summary, get_todays_appointments
from backend.patients_comp import get_all_patients
from backend.appointments_comp import get_all_appointments_with_treatment_count
from backend.billing_comp import get_all_billings

class MainController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.logout_btn.clicked.connect(lambda: self.open_login_popup())
        self.AddApp_btn.clicked.connect(lambda: self.open_appointment())

    def open_login_popup(self):
        login_popup = Database_Dialog_Ctr()
        login_popup.credentialsSubmitted.connect(self.handle_credentials)
        login_popup.exec()
    def open_appointment(self):
        app_popup = Appointment_Dialog_Ctr()
        #app_popup.appointment_details.connect()
        app_popup.exec()
        
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

            self.UpAp_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(appointment[0])))  # Appointment ID
            self.UpAp_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(appointment[1])))  # Patient Name
            self.UpAp_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(appointment[2])))  # Treatment time
            self.UpAp_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(appointment[3])))  # Treatment Procedure
            self.UpAp_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(appointment[4])))  # Treatment Status     
    #DASHBOARD TAB================ end
    
    #PATIENTS TAB=================start
    def update_patients_list(self, patients):
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
           
    #Appointments TAB=================start
    def update_appointments_list(self, appointments):
        self.Appointments_table.setRowCount(0)
        for appointment in appointments:
            row_position = self.Appointments_table.rowCount()
            self.Appointments_table.insertRow(row_position)
            self.Appointments_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(appointment[0])))
            self.Appointments_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(appointment[1])))
            self.Appointments_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(appointment[2])))
            self.Appointments_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(appointment[3])))
            self.Appointments_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(appointment[4])))
    #Appointments TAB=================end
    
    #Billing TAB=================start
    def update_billing_list(self, billings):
        self.Billing_table.setRowCount(0)
        for billing in billings:
            row_position = self.Billing_table.rowCount()
            self.Billing_table.insertRow(row_position)
            self.Billing_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(billing[0])))
            self.Billing_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(billing[1])))
            self.Billing_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(billing[2])))
            self.Billing_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(billing[3])))
            self.Billing_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(billing[4])))
            self.Billing_table.setItem(row_position, 5, QtWidgets.QTableWidgetItem(str(billing[5])))
        
    #Billing TAB=================end
           
    
    #====================LOAD DATAS TO UI=============== end
    #=======================================================
    
    def handle_credentials(self, host, port, user, password, databaseName):
        print(f"Received credentials: host={host}, port ={port}, user={user}, password={password}, database name={databaseName}")
        
        try:
            connection = connectDBF(host, port, user, password, databaseName)
            if not connection:
                raise Exception("Connection returned None")
            
            print(f"Successfully connected to {databaseName} database")
            
         
            set_credentials(host,port, user, password, databaseName)

            createAllTables(connection)

            summary_data = load_summary()
            self.update_summary(summary_data)

            todays_appointments_list = get_todays_appointments()
            self.update_todays_appointments_table(todays_appointments_list)

            all_patients_list = get_all_patients()
            self.update_patients_list(all_patients_list)
            
            all_appointments_list = get_all_appointments_with_treatment_count()
            self.update_appointments_list(all_appointments_list)

            all_billings_list = get_all_billings()
            self.update_billing_list(all_billings_list)
            
            connection.close()
            
        except mysql.connector.InterfaceError as e:
            print("MySQL Interface Error:", e)
            QMessageBox.critical(None, "MySQL Connection Error", str(e))
        except mysql.connector.DatabaseError as e:
            print("MySQL Database Error:", e)
            QMessageBox.critical(None, "MySQL Connection Error", str(e))
        except mysql.connector.ProgrammingError as e:
            print("MySQL Programming Error:", e)
            QMessageBox.critical(None, "MySQL Connection Error", str(e))
        except mysql.connector.OperationalError as e:
            print("MySQL Operational Error:", e)
            QMessageBox.critical(None, "MySQL Connection Error", str(e))
        except mysql.connector.IntegrityError as e:
            print("MySQL Integrity Error:", e)
            QMessageBox.critical(None, "MySQL Connection Error", str(e))
        except mysql.connector.DataError as e:
            print("MySQL Data Error:", e)
            QMessageBox.critical(None, "MySQL Connection Error", str(e))
        except mysql.connector.NotSupportedError as e:
            print("MySQL Not Supported Error:", e)
            QMessageBox.critical(None, "MySQL Connection Error", str(e))
        except mysql.connector.Error as e:
            print("MySQL Error:", e)
            QMessageBox.critical(None, "MySQL Connection Error", str(e))
        except Exception as e:
            print("Unexpected Error:", e)
            QMessageBox.critical(None, "Error", str(e))
