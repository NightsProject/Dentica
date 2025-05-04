from ..mysql_initializer import connectDB

CONNECTED_TO_DATABASE = False

def count_patients():
    patients = 0
    
    if CONNECTED_TO_DATABASE:
        conn = connectDB()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Patient")
        result = cursor.fetchone()
        if result:
            patients = result[0]
        cursor.close()
        conn.close()
    print(patients)     
    return str(patients)
     
def todays_appointments():
    appointments = 0
     
    if CONNECTED_TO_DATABASE:
        conn = connectDB()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Appointment WHERE DATE(Schedule) = CURDATE()")
        result = cursor.fetchone()
        if result:
            appointments = result[0]
        cursor.close()
        conn.close()
        #count todays appointments
        
    print(appointments)
    return str(appointments)

def pending_payments():
    unpaid_payments = 0
      
    if CONNECTED_TO_DATABASE:
        pass
        #count the unpaid payments
    return str(unpaid_payments)

def completed_treatments():
    treatments_completed = 0

    if CONNECTED_TO_DATABASE:
        pass
        #count the completed treatments
    return str(treatments_completed)