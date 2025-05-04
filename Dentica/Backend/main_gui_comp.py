from Frontend.Dialogues.UserPopup import LoginPopup

from Backend.mysql_initializer import connectDBF, createAllTables, set_credentials
from .sub_comp import dashboard_comp



#===== Database Login ================
def  database_login():  
    login_popup = LoginPopup()
    login_popup.credentialsSubmitted.connect(handle_credentials)
    login_popup.exec()

def handle_credentials(host, user, password, databaseName):
    print(f"Received credentials: host={host}, user={user}, password={password}, databse name={databaseName}")
    
    connection = connectDBF(host, user, password, databaseName)
    if connection:
        print(f"Successfully connected to {databaseName} database")

        set_credentials(host, user, password, databaseName) # later for global use 
        
        createAllTables(connection)
        load_data()
         
    else:
        print("Failed to connect to the database.")
        
    #ToDO
    #Notify to gui
    
    
def load_data():
    dashboard_comp.CONNECTED_TO_DATABASE = True
    
    dashboard_comp.count_patients()
    dashboard_comp.todays_appointments()
    dashboard_comp.pending_payments()
    dashboard_comp.completed_treatments()
    
    
  
    
    
    
    