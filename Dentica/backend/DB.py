import mysql.connector
from mysql.connector import Error
from PyQt6.QtWidgets import QMessageBox
import sys
#  store the credentials globally
def set_credentials(host, port, user, password, database):
    global HOST, PORT, USER, PASSWORD, DATABASE_NAME
    HOST = host
    PORT = port
    USER = user
    PASSWORD = password
    DATABASE_NAME = database


#try to connect to the database once
def connectDBF(host, port, user, password, databaseName):
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=databaseName,
            use_pure= True
        )
        print('here')
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Database connection error: {e}")
        raise  # Reraise the exception so the caller can handle it properly

    return None


# Try to connect to the database using the saved credentials
def connectDB():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DATABASE_NAME,
            use_pure=True
        )
        
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        # Show a warning message box for database connection errors
        QMessageBox.warning(None, "Database Connection Error", f"Error: {e}")
    except NameError:
        QMessageBox.warning(None, "No Database Connection", "Please login to a database first.")
        
    return None



def createAllTables(conn):
    cursor = conn.cursor()
    
    
    #Creating patients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Patient (
            Patient_ID VARCHAR(6) NOT NULL,
            First_Name VARCHAR(128) NOT NULL,
            Middle_Name VARCHAR(128) NOT NULL,
            Last_Name VARCHAR(128) NOT NULL,
            Gender VARCHAR(100) NOT NULL,
            Birth_Date DATE NOT NULL,
            Contact_Number VARCHAR(15) NOT NULL,
            Email VARCHAR(100) NOT NULL,
            Address VARCHAR(100) NOT NULL,

            PRIMARY KEY (Patient_ID),
            UNIQUE (Patient_ID)
        );

    """)
    
    
    #Create appointments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Appointment (
            Appointment_ID VARCHAR(6) NOT NULL,
            Patient_ID VARCHAR(6) NOT NULL,
            Schedule DATETIME NOT NULL,
            Status ENUM('Scheduled', 'Completed', 'Cancelled') NOT NULL,

            PRIMARY KEY (Appointment_ID),
            UNIQUE (Appointment_ID),
            FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID)
        );
    """)
    
    #Create Treatments table
    cursor.execute("""   
        CREATE TABLE IF NOT EXISTS Treatment (
            Appointment_ID VARCHAR(6) NOT NULL,
            Treatment_ID INT NOT NULL,
            Diagnosis VARCHAR(256) NOT NULL,
            Cost DECIMAL(10, 4) NOT NULL,
            Treatment_Procedure VARCHAR(128) NOT NULL,
            Treatment_Date_Time DATETIME NOT NULL,
            Treatment_Status ENUM('Completed', 'In-Progress', 'Waiting', 'Canceled'),
            
            PRIMARY KEY (Appointment_ID, Treatment_ID),
            FOREIGN KEY (Appointment_ID) REFERENCES Appointment(Appointment_ID)
        );
    """)
    
    #Create Book table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Books (
            Booking_ID VARCHAR(6) NOT NULL,
            Patient_ID VARCHAR(6) NOT NULL,
            Appointment_ID VARCHAR(6) NOT NULL,
            Booking_Date_Time DATETIME NOT NULL,

            PRIMARY KEY (Booking_ID),
            FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
            FOREIGN KEY (Appointment_ID) REFERENCES Appointment(Appointment_ID)
        );           
    """)
    
    #create Cancel Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cancel (
            Patient_ID VARCHAR(6) NOT NULL,
            Appointment_ID VARCHAR(6) NOT NULL,
            Cancellation_Date_Time DATETIME NOT NULL,
            Reason VARCHAR(256) NOT NULL,

            PRIMARY KEY (Patient_ID, Appointment_ID),
            FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
            FOREIGN KEY (Appointment_ID) REFERENCES Appointment(Appointment_ID)
        ); 
    """)
    
    #Create Pay table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pays (
            Payment_ID VARCHAR(7) NOT NULL,
            Patient_ID VARCHAR(6) NOT NULL,
            Appointment_ID VARCHAR(6) NOT NULL,
            Total_Amount DECIMAL(10, 4) NOT NULL,
            Payment_Method ENUM('Cash', 'Card', 'GCash', 'None') NOT NULL,
            Payment_Status ENUM('Paid','Unpaid') NOT NULL,
            Payment_Date DATETIME,
            
            PRIMARY KEY (Payment_ID),
            FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
            FOREIGN KEY (Appointment_ID) REFERENCES Appointment(Appointment_ID)
        );

    """)