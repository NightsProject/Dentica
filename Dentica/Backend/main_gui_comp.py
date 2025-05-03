from Frontend.Dialogues.UserPopup import LoginPopup
from Backend.mysql_initializer import connectDB, createAllTables

#===== Database Login ================
def  database_login():  
    login_popup = LoginPopup()
    login_popup.credentialsSubmitted.connect(handle_credentials)
    login_popup.exec()

def handle_credentials(host, user, password, databaseName):
    print(f"Received credentials: host={host}, user={user}, password={password}, databse name={databaseName}")
    
    connection = connectDB(host, user, password, databaseName)
    if connection:
        print(f"Successfully connected to {databaseName} database")
        createAllTables(connection)
    else:
        print("Failed to connect to the database.")
        
    #ToDO
    #Notify to gui