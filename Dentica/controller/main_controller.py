#format: class

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QWidget
from PyQt6 import QtCore, QtGui, QtWidgets
from ui.ui_main_window import Ui_MainWindow
from PyQt6.QtWidgets import QMessageBox
import mysql.connector

from ui.Dialogues.ui_exit_dialog import Exit_App
from controller.database_login_ctr import Database_Dialog_Ctr
from controller.appointment_ctr import Appointment_Dialog_Ctr
from controller.patient_ctr import Patient_Dialog_Ctr

from backend.DB import connectDBF, set_credentials, createAllTables
from backend.dashboard_comp import load_summary, get_todays_appointments
from backend.patients_comp import get_all_patients, generate_new_patient_id
from backend.appointments_comp import get_all_appointments_with_treatment_count
from backend.billing_comp import get_all_billings

filepath = "Dentica/ui/icons/"


class MainController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        
        self.userbtn.clicked.connect(lambda: self.open_login_popup())
        self.AddApp_btn.clicked.connect(lambda: self.open_appointment())
        self.add_icon.clicked.connect(lambda: self.open_patient())
        self.exitbtn.clicked.connect(lambda: self.confirm_exit())

    def open_login_popup(self):
        login_popup = Database_Dialog_Ctr()
        login_popup.credentialsSubmitted.connect(self.handle_credentials)
        login_popup.exec()
    
    def open_appointment(self):
        app_popup = Appointment_Dialog_Ctr()
        #app_popup.appointment_details.connect()
        app_popup.exec()
    
    def open_patient(self):
        patient_popup = Patient_Dialog_Ctr()
        patient_popup.patient_added.connect(self.reload_patient_table) 
        patient_popup.exec()
        
    def confirm_exit(MainWindow):
        confirm_popup = Exit_App()
        if confirm_popup.exec():
            MainWindow.close()
            
    #=========================================================
    #====================ACTION BUTTONS================= start
    # This function creates action buttons for each patient/appointment in the table
    # It creates a widget with buttons for viewing, editing, and deleting the patient/appointment
    # It sets the patient ID as a property of each button
    # This allows the buttons to be connected to their respective functions
    # It uses a horizontal layout to arrange the buttons
    # It sets the style of the buttons and the layout
  
    # Create action buttons for patients
    def create_patient_action_buttons(self, patient_id, row):
        widget = QtWidgets.QWidget()

        widget.setStyleSheet("background: none;")

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        # View More Button
        view_btn = QtWidgets.QPushButton()
        view_icon = QtGui.QIcon(f"{filepath}View.svg")
        view_btn.setIcon(view_icon)
        view_btn.setIconSize(QtCore.QSize(20, 20))
        view_btn.setMaximumWidth(60)
        view_btn.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                background-color: #37547A;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #8DB8E0;
            }
        """)
        view_btn.clicked.connect(self.view_patient)
        
        # Edit Button
        edit_btn = QtWidgets.QPushButton()
        edit_icon = QtGui.QIcon(f"{filepath}Edit.svg")
        edit_btn.setIcon(edit_icon)
        edit_btn.setIconSize(QtCore.QSize(20, 20))
        edit_btn.setMaximumWidth(60)
        edit_btn.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                background-color: #37547A;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #8DB8E0;
            }
        """)
        edit_btn.clicked.connect(self.edit_patient)
        
        # Delete Button
        delete_btn = QtWidgets.QPushButton()
        delete_icon = QtGui.QIcon(f"{filepath}Delete.svg")
        delete_btn.setIcon(delete_icon)
        delete_btn.setIconSize(QtCore.QSize(20, 20))
        delete_btn.setMaximumWidth(60)
        delete_btn.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                background-color: #37547A;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #8DB8E0;
            }
        """)
        delete_btn.clicked.connect(self.delete_patient)
        

        layout.addWidget(view_btn)
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)
        
        widget.setLayout(layout)
        
        #set the property of the button to the patient id
        view_btn.setProperty("Patient ID", patient_id)
        edit_btn.setProperty("Patient ID", patient_id)
        delete_btn.setProperty("Patient ID", patient_id)
        
        return widget
    
    def view_patient(self):
        button = self.sender()
        patient_id = button.property("Patient ID")
        QMessageBox.information(self, "View", f"Viewing patient ID: {patient_id}")

    def edit_patient(self):
        button = self.sender()
        patient_id = button.property("Patient ID")
        QMessageBox.information(self, "Edit", f"Editing patient ID: {patient_id}")

    def delete_patient(self):
        button = self.sender()
        patient_id = button.property("Patient ID")
        QMessageBox.information(self, "Delete", f"Deleting patient ID: {patient_id}")

    # Create action buttons for appointments
    def create_appointment_action_buttons(self, appointment_id, row):
        widget = QtWidgets.QWidget()

        widget.setStyleSheet("background: none;")

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        # Edit Button
        edit_btn2 = QPushButton()
        edit_icon = QtGui.QIcon(f"{filepath}Edit.svg")
        edit_btn2.setIcon(edit_icon)
        edit_btn2.setIconSize(QtCore.QSize(20, 20))
        edit_btn2.setMaximumWidth(60)
        edit_btn2.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                background-color: #37547A;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #8DB8E0;
            }
        """)
        edit_btn2.clicked.connect(self.edit_appointment)
        
        # Delete Button
        delete_btn2 = QPushButton()
        delete_icon = QtGui.QIcon(f"{filepath}Delete.svg")
        delete_btn2.setIcon(delete_icon)
        delete_btn2.setIconSize(QtCore.QSize(20, 20))
        delete_btn2.setMaximumWidth(60)
        delete_btn2.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                background-color: #37547A;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #8DB8E0;
            }
        """)
        delete_btn2.clicked.connect(self.delete_appointment)
        
        layout.addWidget(edit_btn2)
        layout.addWidget(delete_btn2)
        
        widget.setLayout(layout)
        
        #set the property of the button to the appointment id
        edit_btn2.setProperty("Appointment ID", appointment_id)
        delete_btn2.setProperty("Appointment ID", appointment_id)
        
        return widget

    def edit_appointment(self):
        button = self.sender()
        appointment_id = button.property("Appointment ID")
        QMessageBox.information(self, "Edit", f"Editing appointment ID: {appointment_id}")
        
    def delete_appointment(self):
        button = self.sender()
        appointment_id = button.property("Appointment ID")
        QMessageBox.information(self, "Delete", f"Deleting appointment ID: {appointment_id}")
    #====================ACTION BUTTONS================= end
    #=======================================================
    
    
    
    #=========================================================
    #====================LOAD DATAS TO UI=============== start
    # This function is called to load data into the UI
    # It receives the data and updates the UI elements accordingly
    # It updates the summary, today's appointments, patients, appointments, and billing tables
    # It also handles the case where the connection is None
    # It uses the functions from the backend to get the data
    # It also handles the case where the connection is None
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
    def reload_patient_table(self):
        all_patients = get_all_patients()
        self.update_patients_list(all_patients)

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
            action_widget = self.create_patient_action_buttons(patient_id, row_position)
            self.Patients_table.setCellWidget(row_position, 6, action_widget)

           
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
            
            appointment_id = appointment[0]
            action_widget = self.create_appointment_action_buttons(appointment_id, row_position)
            self.Appointments_table.setCellWidget(row_position, 4, action_widget)
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
    
    
    
    #=========================================================
    #====================HANDLE CREDENTIALS================= start
    # This function is called when the user submits the login form
    # It receives the credentials and attempts to connect to the database
    # If successful, it loads the data into the UI
    # If not, it shows an error message
    # It also handles the case where the connection is None
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
    #====================HANDLE CREDENTIALS================= end
    #===========================================================
