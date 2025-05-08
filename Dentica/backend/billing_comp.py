
from backend.DB import connectDB
 
def get_all_billings():
    billings = []

    conn = connectDB()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            p.Payment_ID,
            CONCAT(pa.First_Name, ' ', pa.Middle_Name, ' ', pa.Last_Name) AS Patient_Full_Name,
            p.Appointment_ID,
            p.Total_Amount,
            p.Payment_Method,
            p.Payment_Status
        FROM Pays p
        JOIN Patient pa ON p.Patient_ID = pa.Patient_ID
        ORDER BY p.Payment_ID
    """)
    
    result = cursor.fetchall()
    if result:
        for row in result:
            billings.append(row)

    cursor.close()
    conn.close()
    
    return billings
