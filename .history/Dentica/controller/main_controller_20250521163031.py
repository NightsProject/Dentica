#format: class

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QPushButton
from ui.ui_main_window import Ui_MainWindow
from PyQt6.QtWidgets import QMessageBox
import mysql.connector

from ui.Dialogues.ui_exit_dialog import Exit_App
from controller.database_login_ctr import Database_Dialog_Ctr
from controller.appointment_ctr import Appointment_Dialog_Ctr
from controller.user_login_ctr import User_Dialog_Ctr
from controller.patient_ctr import Patient_Dialog_Ctr

from backend.DB import connectDBF, set_credentials, createAllTables
from backend.dashboard_comp import load_summary, get_todays_appointments
from backend.patients_comp import get_all_patients, generate_new_patient_id
from backend.appointments_comp import get_all_appointments_with_treatment_count
from backend.billing_comp import get_all_billings


class MainController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        
        self.userbtn.clicked.connect(lambda: self.open_login_popup())
        # self.settings_btn.clicked.connect(lambda: self.user_login_popup())
        self.AddApp_btn.clicked.connect(lambda: self.open_appointment())
        self.add_icon.clicked.connect(lambda: self.open_patient())
        self.exitbtn.clicked.connect(lambda: self.confirm_exit())

    def open_login_popup(self):
        login_popup = Database_Dialog_Ctr()
        login_popup.credentialsSubmitted.connect(self.handle_credentials)
        login_popup.exec()
    
    def user_login_popup(self):
        user_popup = User_Dialog_Ctr()
        user_popup.exec()
        
    def open_appointment(self):
        app_popup = Appointment_Dialog_Ctr()
        #app_popup.appointment_details.connect()
        app_popup.exec()
    
    def open_patient(self):
        patient_popup = Patient_Dialog_Ctr()
        patient_popup.exec()
        
    def confirm_exit(MainWindow):
        confirm_popup = Exit_App()
        if confirm_popup.exec():
            MainWindow.close()
            
    def create_patient_action_buttons(self, patient_id, row):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        # View More Button
        view_btn = QtWidgets.QPushButton("View")
        view_btn.setMaximumWidth(60)
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        view_btn.clicked.connect(lambda: self.button_clicked(patient_id))
        # Edit Button
        edit_btn = QtWidgets.QPushButton("Edit")
        edit_btn.setMaximumWidth(60)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1e7e34;
            }
        """)
        
        # Delete Button
        delete_btn = QtWidgets.QPushButton("Delete")
        delete_btn.setMaximumWidth(60)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        
        layout.addWidget(view_btn)
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)
        
        widget.setLayout(layout)
        return widget

    def create_appointment_action_buttons(self, appointment_id, row):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        # View More Button
        view_btn = QtWidgets.QPushButton("View")
        view_btn.setMaximumWidth(60)
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        view_btn.clicked.connect(lambda: self.button_clicked(appointment_id))
        # Edit Button
        edit_btn = QtWidgets.QPushButton("Edit")
        edit_btn.setMaximumWidth(60)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1e7e34;
            }
        """)
        
        # Delete Button
        delete_btn = QtWidgets.QPushButton("Delete")
        delete_btn.setMaximumWidth(60)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        
        layout.addWidget(view_btn)
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)
        
        widget.setLayout(layout)
        return widget

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
            self.Patients_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(patient[1])))
            self.Patients_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(patient[2])))
            self.Patients_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(patient[3])))
            self.Patients_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(patient[4])))
            self.Patients_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(patient[5])))
            self.Patients_table.setItem(row_position, 5, QtWidgets.QTableWidgetItem(str(patient[6])))
            

            patient_id = patient[0]
            action_widget = self.create_action_buttons(patient_id, row_position)
            self.Patients_table.setCellWidget(row_position, 6, action_widget)


    def button_clicked(self):
        # Get the button that was clicked
        button = self.sender()
        name = button.property("Patient ID")
        QMessageBox.information(self, "Greeting", f"Hello, {name}!")
           
    #Appointments TAB=================start
    def update_appointments_list(self, appointments):
        self.Appointments_table.setRowCount(0)
        for appointment in appointments:
            row_position = self.Appointments_table.rowCount()
            self.Appointments_table.insertRow(row_position)
            self.Appointments_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(appointment[1])))
            self.Appointments_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(appointment[2])))
            self.Appointments_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(appointment[3])))
            self.Appointments_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(appointment[4])))
            # the appointment is stored in appointment[0]
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
            if connection:
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
