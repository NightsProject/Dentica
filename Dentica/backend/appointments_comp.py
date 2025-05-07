from backend.DB import connectDB


def get_all_appointments_with_treatment_count():
    all_appointments = []

    conn = connectDB()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            a.Appointment_ID,
            CONCAT(p.First_Name, ' ', p.Middle_Name, ' ', p.Last_Name) AS Patient_Full_Name,
            DATE(a.Schedule) AS Appointment_Date,
            a.Status,
            COUNT(t.Treatment_ID) AS Treatment_Count
        FROM Appointment a
        JOIN Patient p ON a.Patient_ID = p.Patient_ID
        LEFT JOIN Treatment t ON a.Appointment_ID = t.Appointment_ID
        GROUP BY a.Appointment_ID, Patient_Full_Name, Appointment_Date, a.Status
        ORDER BY a.Schedule DESC
    """)
    
    result = cursor.fetchall()
    if result:
        for row in result:
            all_appointments.append(row)

    cursor.close()
    conn.close()
    
    print(all_appointments)
    return all_appointments
