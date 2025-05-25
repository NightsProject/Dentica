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
