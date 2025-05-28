#format: class

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6 import QtCore, QtGui, QtWidgets
from ui.ui_main_window import Ui_MainWindow
from PyQt6.QtWidgets import QMessageBox

from PyQt6.QtGui import QColor, QBrush

from ui.Dialogues.ui_exit_dialog import Exit_App
from controller.database_login_ctr import Database_Dialog_Ctr
from controller.appointment_ctr import Appointment_Dialog_Ctr
from controller.patient_ctr import Patient_Dialog_Ctr
from controller.patient_page_ctr import Patient_Page_Ctr
from controller.viewapp_ctr import View_Appointent_Ctr
from controller.billing_ctr import Billing_Dialog_Ctr

from backend.DB import connectDBF, set_credentials, createAllTables
from backend.dashboard_comp import load_summary, get_todays_appointments, get_todays_appointment_status_counts, create_appointment_status_chart, refresh_appointment_chart
from backend.patients_comp import get_all_patients, perform_patient_deletion, get_patient_data, search_patients
from backend.appointments_comp import get_appointment_data, get_all_appointments_with_treatment_count, perform_appointment_deletion, search_appointments
from backend.billing_comp import get_all_billings, search_payments
from backend.booking_comp import get_all_bookings, search_bookings
from backend.reports_comp import load_graphs, refresh_graphs
from backend.cancelations_comp import get_all_cancellations, search_cancellations
from backend.treatment_comp import update_treatment, check_treatment_completion, auto_handle_all_treatments_canceled, update_total_amount_treatment_canceled



"""
Key Features

    Inheritance:
        The MainController class inherits from QMainWindow and Ui_MainWindow, allowing it to utilize the main window's features and the UI layout defined in Ui_MainWindow.

    Initialization:
        The constructor (__init__) initializes the main window and sets up connections between UI elements (buttons, text fields) and their corresponding methods. This includes connecting buttons for user login, adding appointments, adding patients, and exiting the application.

    User Interaction:
        The class provides methods to open various dialogs for user interactions:
            open_login_popup: Opens a dialog for database login.
            open_appointment: Opens a dialog for adding or updating appointments.
            open_patient: Opens a dialog for adding or updating patient information.
            confirm_exit: Confirms if the user wants to exit the application.

    Handling Credentials:
        The handle_credentials method is called when the user submits the login form. It attempts to connect to the database using the provided credentials. If successful, it loads data into the UI, including appointment summaries, patient lists, and charts.

    Data Loading:
        The reload_all_tables method refreshes all data tables in the UI, including today's appointments, patients, appointments, billings, and bookings. It calls various backend functions to retrieve the necessary data.

    Dashboard Updates:
        The update_summary method updates the summary section of the dashboard with relevant statistics, such as the number of scheduled, completed, and canceled appointments.
        The update_todays_appointments_table, update_patients_list, update_appointments_list, and update_billing_list methods populate their respective tables with data retrieved from the backend.

    Action Buttons:
        The class provides methods to create action buttons for patients and appointments, allowing users to view, edit, or delete records. Each button is connected to its respective method, which handles the action when clicked.

    Search Functionality:
        The class includes methods for searching patients, appointments, payments, and bookings. These methods call backend search functions and update the corresponding lists in the UI.

    Error Handling:
        Throughout the class, error handling is implemented using message boxes to inform the user of any issues, such as failed database connections or unsuccessful operations.

"""





filepath = "Dentica/ui/icons/"


class MainController(QMainWindow, Ui_MainWindow):
    def __init__(self): 
        super().__init__()
        
        self.setupUi(self)
        self.dark_mode = False
        self.first_login = True
        self.open_login_popup()
        
        
        self.userbtn.clicked.connect(lambda: self.open_login_popup())
        self.AddApp_btn.clicked.connect(lambda: self.open_appointment())
        self.add_icon.clicked.connect(lambda: self.open_patient())
        self.exitbtn.clicked.connect(lambda: self.confirm_exit())
        
        self.search_patient.textChanged.connect(self.search_patient_data)
        self.Search_app.textChanged.connect(self.search_appointment_data)
        self.Search_bill.textChanged.connect(self.search_payment_data)
        self.Search_book.textChanged.connect(self.search_booking_data)
        self.Search_cancel.textChanged.connect(self.search_cancel_data)
        self.calendar.clicked.connect(self.on_calendar_date_clicked)
        
        #appointment button
        self.pushButton_8.clicked.connect(self.reload_all_tables) #all button
        self.pushButton_9.clicked.connect(lambda: self.search_appointment_data("Scheduled")) #scheduled button
        self.pushButton_7.clicked.connect(lambda: self.search_appointment_data("Completed")) #completed button
        self.pushButton_6.clicked.connect(lambda: self.search_appointment_data("Cancelled")) #canceled button
        
        #payment button
        self.pushButton_12.clicked.connect(self.reload_all_tables)
        self.pushButton_13.clicked.connect(lambda: self.search_payment_data("Paid"))
        self.pushButton_14.clicked.connect(lambda: self.search_payment_data("unpaid"))
        
  
        
        
    def open_login_popup(self):
        login_popup = Database_Dialog_Ctr(self.first_login)
        login_popup.credentialsSubmitted.connect(self.handle_credentials)
        login_popup.exec()
    
    def open_appointment(self):
        app_popup = Appointment_Dialog_Ctr()
        app_popup.dark_mode = self.dark_mode
        app_popup.apply_theme()
        app_popup.appointment_added.connect(self.reload_all_tables)
        app_popup.exec()

        
    def open_patient(self):
        patient_popup = Patient_Dialog_Ctr()
        patient_popup.dark_mode = self.dark_mode  
        patient_popup.apply_theme()
        patient_popup.patient_added.connect(self.reload_all_tables) 
        patient_popup.exec()
        
    def confirm_exit(MainWindow):
        confirm_popup = Exit_App()
        if confirm_popup.exec():
            MainWindow.close()
    
    #=========================================================
    #====================HANDLE CREDENTIALS================= start
    # This function is called when the user submits the login form
    # It receives the credentials and attempts to connect to the database
    # If successful, it loads the data into the UI
    # If not, it shows an error message
    # It also handles the case where the connection is None
    def handle_credentials(self, host, port, user, password, databaseName, first_login):
        
        try:
            connection = connectDBF(host, port, user, password, databaseName)
            if not connection:
                raise Exception("Connection returned None")
            
            print(f"Successfully connected to {databaseName} database")
            
         
            set_credentials(host,port, user, password, databaseName)
            if connection:
                self.first_login = first_login
                QMessageBox.information(self, "Success", f"Successfully connected to {databaseName} Database!")
           
                
                createAllTables(connection)
                
                summary_data = load_summary()
                
                todays_appointment_status = get_todays_appointment_status_counts()
                self.update_summary(summary_data, todays_appointment_status)
                self.appointment_chart = create_appointment_status_chart()
                self.tot_appstat_chart, self.payment_method_chart, self.gender_dist_chart, self.age_dist_chart, self.app_ot_chart, self.quarterly_rev_chart, self.Comm_treat_chart, self.treat_cost_chart = load_graphs()
                
                if self.appointment_chart:
                        self.today_stat_layout.addWidget(self.appointment_chart)
                        
                if self.tot_appstat_chart:
                        self.tot_appstat_layout.addWidget(self.tot_appstat_chart)
                        
                if self.payment_method_chart:
                        self.payment_method_layout.addWidget(self.payment_method_chart)
                
                if self.gender_dist_chart:
                        self.gender_dist_layout.addWidget(self.gender_dist_chart)

                if self.age_dist_chart:
                        self.age_dist_layout.addWidget(self.age_dist_chart)
                        
                if self.app_ot_chart:
                        self.app_ot_layout.addWidget(self.app_ot_chart)

                if self.quarterly_rev_chart:
                    self.quarterly_rev_layout.addWidget(self.quarterly_rev_chart)
                
                if self.Comm_treat_chart:
                        self.common_treatments_layout.addWidget(self.Comm_treat_chart)
                
                if self.treat_cost_chart:
                        self.treat_cost_layout.addWidget(self.treat_cost_chart)
                    
                todays_appointments_list = get_todays_appointments()
                self.update_todays_appointments_table(todays_appointments_list)

                all_patients_list = get_all_patients()
                self.update_patients_list(all_patients_list)
                
                all_appointments_list = get_all_appointments_with_treatment_count()
                self.update_appointments_list(all_appointments_list)

                all_billings_list = get_all_billings()
                self.update_billing_list(all_billings_list)
                
                all_bookings_list = get_all_bookings()
                self.update_bookings_list(all_bookings_list)
                             
                all_canceled_list = get_all_cancellations()
                self.update_cancel_list(all_canceled_list)
            
            connection.close()
            
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
    #====================HANDLE CREDENTIALS================= end
    #===========================================================


          
    
    #=========================================================
    #====================LOAD DATAS TO UI=============== start
    # This function is called to load data into the UI
    # It receives the data and updates the UI elements accordingly
    # It updates the summary, today's appointments, patients, appointments, and billing tables
    # It also handles the case where the connection is None
    # It uses the functions from the backend to get the data
    # It also handles the case where the connection is None
    
    # This function reloads all the tables in the UI
    # It calls the functions to get the data from the backend
    def reload_all_tables(self):
        
        summary_data = load_summary()
        
        todays_appointment_status = get_todays_appointment_status_counts()
        self.update_summary(summary_data, todays_appointment_status)                

        todays_appointments_list = get_todays_appointments()
        self.update_todays_appointments_table(todays_appointments_list)

        all_patients_list = get_all_patients()
        self.update_patients_list(all_patients_list)
                
        all_appointments_list = get_all_appointments_with_treatment_count()
        self.update_appointments_list(all_appointments_list)

        all_billings_list = get_all_billings()
        self.update_billing_list(all_billings_list)
        
        all_bookings_list = get_all_bookings()
        self.update_bookings_list(all_bookings_list)
        
        all_canceled_list = get_all_cancellations()
        self.update_cancel_list(all_canceled_list)
        
        refresh_appointment_chart(self)
        refresh_graphs(self)
    #=========================================================
    
    #DASHBOARD TAB=============== start
    def update_summary(self, data, status):
       
        self.label_5.setText(str(data[0]))
        self.label_6.setText(str(data[1]))
        self.label_7.setText(str(data[2]))
        self.label_9.setText(f"{data[3][0]}/{data[3][1]}")
        self.scheduled_label.setText(f"Scheduled:                                                                 {status[0]}")
        self.completed_label.setText (f"Completed:                                                                {status[1]}")
        self.cancelled_label.setText(f"Cancelled:                                                                 {status[2]}")
        
        #update the chart values
        
    #update_todays_appointments_table
    # This function updates the table with today's appointments
    # It receives the appointments data and populates the table
    # It sets the row count to 0 and then inserts rows for each appointment
    # It sets the items for each column in the row
    # It uses the appointment data to set the values for each column
    def update_todays_appointments_table(self, appointments):
        """
        appointments is a list of tuples:
        (appointment_id, treatment_id, patient_name, treatment_time, procedure, status)
        """
        self.UpAp_table.setRowCount(0)
        for appointment in appointments:
            row = self.UpAp_table.rowCount()
            self.UpAp_table.insertRow(row)

            # Unpack including treatment_id
            appointment_id, treatment_id, patient_name, treatment_time, procedure, status = appointment

            # Populate cells
            self.UpAp_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(patient_name)))
            self.UpAp_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(treatment_time)))
            self.UpAp_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(procedure)))
            self.UpAp_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(status)))

            # Create action widget based on status and both IDs
            action_widget = self.create_todApp_action_buttons(appointment_id, treatment_id, status, row)
            self.UpAp_table.setCellWidget(row, 4, action_widget)

        total = self.UpAp_table.rowCount()
        self.UpAp_pagination.set_total_rows(total)
        self.UpAp_pagination.show_current_page()

            
        
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
            action_widget = self.create_patient_action_buttons(patient_id, row_position)
            self.Patients_table.setCellWidget(row_position, 6, action_widget)
            
            total_patients = self.Patients_table.rowCount()
            self.patients_pagination.set_total_rows(total_patients)
            self.patients_pagination.show_current_page()

           
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
            
            total_appointments = self.Appointments_table.rowCount()
            self.appointments_pagination.set_total_rows(total_appointments)
            self.appointments_pagination.show_current_page()
    #Appointments TAB=================end
    
    #Billing TAB=================start
    def update_billing_list(self, billings):
        self.Billing_table.setRowCount(0)
        for billing in billings:
            row_position = self.Billing_table.rowCount()
            self.Billing_table.insertRow(row_position)
            self.Billing_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(billing[1])))
            self.Billing_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(billing[2])))
            self.Billing_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(f"{billing[3]:.2f}")) # cost value
            self.Billing_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(billing[4])))
            self.Billing_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(billing[6])))
            self.Billing_table.setItem(row_position, 5, QtWidgets.QTableWidgetItem(str(billing[5])))
            

            billing_id = billing[0]
            status = billing[5]  # 'Paid' or 'Unpaid'
            action_widget = self.create_billing_action_buttons(billing_id, row_position, status)
            self.Billing_table.setCellWidget(row_position,6,action_widget)

            total_billing = self.Billing_table.rowCount()
            self.Billing_pagination.set_total_rows(total_billing)
            self.Billing_pagination.show_current_page()
    #Billing TAB=================end
           
    #Bookings TAB=================start
    def update_bookings_list(self, bookings):
        self.Booking_table.setRowCount(0)
        for booking in bookings:
            row_position = self.Booking_table.rowCount()
            self.Booking_table.insertRow(row_position)
            self.Booking_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(booking[0])))
            self.Booking_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(booking[1])))
            self.Booking_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(booking[2])))
            self.Booking_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(booking[3])))
            
            total_bookings = self.Booking_table.rowCount()
            self.Booking_pagination.set_total_rows(total_bookings)
            self.Booking_pagination.show_current_page()       
    #Bookings TAB ===================end
    
    #Cancelation TAB =================start
    def update_cancel_list(self, canceled):
        self.Cancel_table.setRowCount(0)
        for canceled in canceled:
            row_position = self.Cancel_table.rowCount()
            self.Cancel_table.insertRow(row_position)
            self.Cancel_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(canceled[1]))) #patient full name
            self.Cancel_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(canceled[2]))) #appointment id
            self.Cancel_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(canceled[3]))) #appointment schedule
            self.Cancel_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(canceled[4]))) #date cancelled
            self.Cancel_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(canceled[5]))) #reason
           
            #canceled is =canceled[0]
            total_bookings = self.Cancel_table.rowCount()
            self.Cancel_pagination.set_total_rows(total_bookings)
            self.Cancel_pagination.show_current_page()       
            
    def on_calendar_date_clicked(self, date):
        # date is a QDate object
        clicked_date_str = date.toString("yyyy-MM-dd")
        print(f"Date clicked: {clicked_date_str}")

  
            
    #====================LOAD DATAS TO UI=============== end
    #=======================================================
    
    

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

        # Delete old patient profile page if it exists
        if hasattr(self, 'patient_profile_page'):
            self.Pages.removeWidget(self.patient_profile_page)
            self.patient_profile_page.deleteLater()
            del self.patient_profile_page

        # Create a new patient profile page
        self.patient_profile_page = Patient_Page_Ctr(self.Pages, patient_id)
        self.patient_profile_page.dark_mode = self.dark_mode
        self.patient_profile_page.apply_theme()
        self.patient_profile_page.reload_patient_signal.connect(self.reload_all_tables)

        # Add the new widget and switch to it
        self.Pages.addWidget(self.patient_profile_page)
        self.Pages.setCurrentWidget(self.patient_profile_page)

    def edit_patient(self):
        button = self.sender()
        patient_id = button.property("Patient ID")
        patient_data = get_patient_data(patient_id)
        if not patient_data:
            QMessageBox.warning(self, "Error", "Could not load patient data")
            return
        
        patient_popup = Patient_Dialog_Ctr(patient_data=patient_data)
        patient_popup.dark_mode = self.dark_mode  
        patient_popup.apply_theme()
        patient_popup.patient_added.connect(self.reload_all_tables)
        patient_popup.exec()
        
   
 
    def delete_patient(self):
        button = self.sender()
        patient_id = button.property("Patient ID")

        # Create confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the patient with ID: {patient_id} along with all associated records?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Proceed with deletion
            success = perform_patient_deletion(patient_id)
            if success:
                QMessageBox.information(self, "Success", "Patient deleted successfully along with all associated records.")
                self.reload_all_tables()  # Refresh the patient list
            else:
                QMessageBox.warning(self, "Failure", "Failed to delete patient.")
        else:
            # Deletion canceled
            print("Deletion canceled.")

    # Create action buttons for appointments
    def create_appointment_action_buttons(self, appointment_id, row):
        widget = QtWidgets.QWidget()

        widget.setStyleSheet("background: none;")

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        # View More Button
        view_btn2 = QtWidgets.QPushButton()
        view_icon = QtGui.QIcon(f"{filepath}View.svg")
        view_btn2.setIcon(view_icon)
        view_btn2.setIconSize(QtCore.QSize(20, 20))
        view_btn2.setMaximumWidth(60)
        view_btn2.setStyleSheet("""
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
        view_btn2.clicked.connect(self.view_appointment)
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
        layout.addWidget(view_btn2)
        layout.addWidget(edit_btn2)
        layout.addWidget(delete_btn2)
        
        widget.setLayout(layout)
        
        #set the property of the button to the appointment id
        view_btn2.setProperty("Appointment ID", appointment_id)
        edit_btn2.setProperty("Appointment ID", appointment_id)
        delete_btn2.setProperty("Appointment ID", appointment_id)
        
        return widget

    def view_appointment(self):
        button = self.sender()
        appointment_id = button.property("Appointment ID")
        view_appointment = View_Appointent_Ctr(appointment_id)
        view_appointment.dark_mode = self.dark_mode 
        view_appointment.apply_theme()
        #view_appointment.view_app_reload.connect(self.reload_all_tables)
        view_appointment.exec()
  
    def edit_appointment(self):
        button = self.sender()
        appointment_id = button.property("Appointment ID")
        
        appointment_data = get_appointment_data(appointment_id)
        if not appointment_data:
            QMessageBox.warning(self, "Error", "Could not load appointment data")
            return
        
        app_popup = Appointment_Dialog_Ctr(appointment_data=appointment_data)
        app_popup.dark_mode = self.dark_mode  
        app_popup.apply_theme()
        app_popup.appointment_added.connect(self.reload_all_tables)
        app_popup.exec()
        
    def delete_appointment(self):
        button = self.sender()
        appointment_id = button.property("Appointment ID")

        # Create confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the appointment with ID: {appointment_id} along with the all associated treatments?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Proceed with deletion
            success = perform_appointment_deletion(appointment_id)
            if success:
                QMessageBox.information(self, "Success", "Appointment deleted successfully along with the all associated treatments.")
                self.reload_all_tables()  # Refresh the appointments list
            else:
                QMessageBox.warning(self, "Failure", "Failed to delete appointment.")
        else:
            # Deletion canceled
            print("Deletion canceled.")


    def create_billing_action_buttons(self, billing_id, row, status):
        widget = QtWidgets.QWidget()
        widget.setStyleSheet("background: none;")

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)

        if status == "Unpaid":
            # Pay Button
            pay = QtWidgets.QPushButton("Pay")
            pay.setMaximumWidth(60)
            pay.setStyleSheet("""
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
            pay.clicked.connect(self.pay_billing)
            pay.setProperty("Billing_ID", billing_id)
            layout.addWidget(pay)

        elif status == "Paid":
            # Edit Button
            edit_bill = QtWidgets.QPushButton()
            edit_icon = QtGui.QIcon(f"{filepath}Edit.svg")
            edit_bill.setIcon(edit_icon)
            edit_bill.setIconSize(QtCore.QSize(20, 20))
            edit_bill.setMaximumWidth(60)
            edit_bill.setStyleSheet("""
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
            edit_bill.clicked.connect(self.edit_billing)
            edit_bill.setProperty("Billing_ID", billing_id)
            layout.addWidget(edit_bill)

        widget.setLayout(layout)
        return widget

        
    def pay_billing(self):
        button = self.sender()
        billing_id = button.property("Billing_ID")
        bill_popup = Billing_Dialog_Ctr(billing_id)
        bill_popup.dark_mode = self.dark_mode  
        bill_popup.apply_theme()
        bill_popup.payment_added.connect(self.reload_all_tables)
        bill_popup.exec()

    
    def edit_billing(self):
        button = self.sender()
        billing_id = button.property("Billing_ID")
        bill_popup = Billing_Dialog_Ctr(billing_id)
        bill_popup.dark_mode = self.dark_mode  
        bill_popup.apply_theme()
        bill_popup.payment_added.connect(self.reload_all_tables)
        bill_popup.exec()
    
    def create_todApp_action_buttons(self, appointment_id, treatment_id, status, row):
        """
        appointment_id: ID of the appointment
        treatment_id: ID of the treatment
        status: 'Waiting', 'In-Progress', or 'Completed'
        row: the row index in UpAp_table
        """
        widget = QtWidgets.QWidget()
        widget.setStyleSheet("background: none;")
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)

        # Shared style template
        btn_style = """
            QPushButton {
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
        """

        def set_props(button):
            button.setProperty("Appointment ID", appointment_id)
            button.setProperty("Treatment ID", treatment_id)

        # 1) Waiting → show In-Progress (orange) & Cancel (red)
        if status == "Waiting":
            btn_ip = QtWidgets.QPushButton("In-Progress")
            btn_ip.setMaximumWidth(90)
            btn_ip.setStyleSheet(btn_style + "QPushButton { background-color: #FFA500; }")  # orange
            btn_ip.clicked.connect(self.in_progress_treatment)
            set_props(btn_ip)
            layout.addWidget(btn_ip)

            btn_cancel = QtWidgets.QPushButton("Cancel")
            btn_cancel.setMaximumWidth(60)
            btn_cancel.setStyleSheet(btn_style + "QPushButton { background-color: #E74C3C; }")  # red
            btn_cancel.clicked.connect(self.cancel_treatment)
            set_props(btn_cancel)
            layout.addWidget(btn_cancel)

        # 2) In-Progress → show Done (green) & Cancel (red)
        elif status == "In-Progress":
            btn_done = QtWidgets.QPushButton("Done")
            btn_done.setMaximumWidth(60)
            btn_done.setStyleSheet(btn_style + "QPushButton { background-color: #27AE60; }")  # green
            btn_done.clicked.connect(self.done_treatment)
            set_props(btn_done)
            layout.addWidget(btn_done)

            btn_cancel = QtWidgets.QPushButton("Cancel")
            btn_cancel.setMaximumWidth(60)
            btn_cancel.setStyleSheet(btn_style + "QPushButton { background-color: #E74C3C; }")  # red
            btn_cancel.clicked.connect(self.cancel_treatment)
            set_props(btn_cancel)
            layout.addWidget(btn_cancel)

        widget.setLayout(layout)
        return widget
  
    def done_treatment(self):
        button = self.sender()
        appointment_id = button.property("Appointment ID")
        treatment_id = button.property("Treatment ID")

        reply = QMessageBox.question(
            self,
            "Confirm Completion",
            f"Are you sure you want to mark treatment {treatment_id} as Completed?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success = update_treatment(self, appointment_id, treatment_id, "Completed")
            if success:
                check_treatment_completion(appointment_id, parent=self)
                self.reload_all_tables()

    def in_progress_treatment(self):
        button = self.sender()
        appointment_id = button.property("Appointment ID")
        treatment_id = button.property("Treatment ID")

        reply = QMessageBox.question(
            self,
            "Confirm In-Progress",
            f"Are you sure you want to mark treatment {treatment_id} as In-Progress?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success = update_treatment(self, appointment_id, treatment_id, "In-Progress")
            if success:
                self.reload_all_tables()

    def cancel_treatment(self):
        button = self.sender()
        appointment_id = button.property("Appointment ID")
        treatment_id = button.property("Treatment ID")

        reply = QMessageBox.question(
            self,
            "Confirm Cancellation",
            f"Are you sure you want to cancel treatment {treatment_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success = update_treatment(self, appointment_id, treatment_id, "Canceled")
            if success:
                all_canceled = auto_handle_all_treatments_canceled(appointment_id, self)
                if not all_canceled:
                    update_total_amount_treatment_canceled(appointment_id, self)
                self.reload_all_tables()



        
    #====================ACTION BUTTONS================= end
    #=======================================================
    
    #search implementations
    
    def search_patient_data(self, keyword):
        data = search_patients(keyword)
        self.update_patients_list(data)
        
    def search_appointment_data(self, keyword):
        data = search_appointments(keyword)
        self.update_appointments_list(data)
    
    def search_payment_data(self, keyword):
        data = search_payments(keyword)
        self.update_billing_list(data)
        
    def search_booking_data(self, keyword):
        data = search_bookings(keyword)
        self.update_bookings_list(data)
        
    def search_cancel_data(self, keyword):
        data = search_cancellations(keyword)
        self.update_cancel_list(data)
        