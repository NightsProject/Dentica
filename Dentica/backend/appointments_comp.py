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

def generate_new_appointment_id():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Appointment_ID 
        FROM Appointment 
        ORDER BY CAST(SUBSTRING(Appointment_ID, 2) AS UNSIGNED) DESC 
        LIMIT 1
    """)

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        last_id = int(result[0][1:])  # Remove the 'A' and convert the number part
        new_id_num = last_id + 1
    else:
        new_id_num = 1  # Start from 1 if there are no appointments yet

    new_appointment_id = f'A{new_id_num:05d}'  # Zero-padded to 5 digits
    return new_appointment_id






def save_appointment_to_db(appointment_data):
    conn = connectDB()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO Appointment (Appointment_ID, Patient_ID, Schedule, Status)
            VALUES (%s, %s, %s, %s)
        """, (appointment_data["Appointment_ID"], appointment_data["Patient_ID"], appointment_data["Schedule"], appointment_data["Status"]))

        for treatment in appointment_data["Treatments"]:
            cursor.execute("""
                INSERT INTO Treatment (Appointment_ID, Treatment_ID, Diagnosis, Cost, Treatment_Procedure, Treatment_Date_Time, Treatment_Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (treatment["Appointment_ID"], treatment["Treatment_ID"], treatment["Diagnosis"], treatment["Cost"], treatment["Treatment_Procedure"], treatment["Treatment_Date_Time"], treatment["Treatment_Status"]))

        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        conn.close()
        
        
        