from backend.DB import connectDB

def get_all_cancellations():
    """
    Retrieves all cancellation records, including patient name and appointment schedule.
    """
    cancellations = []

    conn = connectDB()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            c.Patient_ID,
            CONCAT(p.First_Name, ' ', p.Middle_Name, ' ', p.Last_Name) AS Patient_Full_Name,
            c.Appointment_ID,
            a.Schedule                    AS Appointment_Schedule,
            c.Cancellation_Date_Time,
            c.Reason
        FROM Cancel c
        JOIN Patient p 
          ON c.Patient_ID = p.Patient_ID
        JOIN Appointment a 
          ON c.Appointment_ID = a.Appointment_ID
        ORDER BY c.Cancellation_Date_Time DESC
    """)
    
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            cancellations.append(row)

    cursor.close()
    conn.close()
    
    return cancellations

def search_cancellations(keyword):
    conn = connectDB()
    cursor = conn.cursor()

    like_keyword = f"%{keyword}%"

    cursor.execute("""
        SELECT 
            Cancel.Patient_ID, -- idx 0, not used in UI update
            CONCAT(Patient.First_Name, ' ', Patient.Middle_Name, ' ', Patient.Last_Name) AS Patient_Full_Name, -- idx 1
            Cancel.Appointment_ID, -- idx 2
            Appointment.Schedule, -- idx 3, appointment schedule datetime
            Cancel.Cancellation_Date_Time, -- idx 4, cancellation date
            Cancel.Reason -- idx 5
        FROM Cancel
        LEFT JOIN Patient ON Cancel.Patient_ID = Patient.Patient_ID
        LEFT JOIN Appointment ON Cancel.Appointment_ID = Appointment.Appointment_ID
        WHERE CONCAT(Patient.First_Name, ' ', Patient.Middle_Name, ' ', Patient.Last_Name) LIKE %s
           OR Cancel.Patient_ID LIKE %s
           OR Cancel.Appointment_ID LIKE %s
           OR Cancel.Cancellation_Date_Time LIKE %s
           OR Cancel.Reason LIKE %s
           OR Appointment.Schedule LIKE %s
    """, (
        like_keyword,  # Patient full name search here
        like_keyword,  # Patient_ID
        like_keyword,  # Appointment_ID
        like_keyword,  # Cancellation_Date_Time
        like_keyword,  # Reason
        like_keyword,  # Appointment.Schedule
    ))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    cancellation_data = [list(row) for row in rows]
    return cancellation_data

