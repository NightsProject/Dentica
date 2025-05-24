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

def get_appointment_data(appointment_id):
    """Get complete appointment data including treatments"""
    conn = connectDB()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get appointment details
        cursor.execute("""
            SELECT a.Appointment_ID, a.Patient_ID, a.Schedule, a.Status,
                   CONCAT(p.First_Name, ' ', p.Last_Name) AS Patient_Name
            FROM Appointment a
            JOIN Patient p ON a.Patient_ID = p.Patient_ID
            WHERE a.Appointment_ID = %s
        """, (appointment_id,))
        appointment = cursor.fetchone()
        
        if not appointment:
            return None
        
        # Convert datetime to string if needed
        if hasattr(appointment['Schedule'], 'strftime'):
            appointment['Schedule'] = appointment['Schedule'].strftime('%Y-%m-%d %H:%M:%S')
        
        # Get treatments for this appointment
        cursor.execute("""
            SELECT Treatment_ID, Treatment_Procedure, Cost
            FROM Treatment
            WHERE Appointment_ID = %s
        """, (appointment_id,))
        treatments = cursor.fetchall()
        appointment['Treatments'] = treatments
        
        return appointment
        
    except Exception as e:
        print("Error getting appointment data:", e)
        return None
    finally:
        cursor.close()
        conn.close()

def update_appointment_in_db(appointment_data):
    """Update an existing appointment and its treatments"""
    conn = connectDB()
    if not conn:
        return False
        
    try:
        cursor = conn.cursor()
        
        # Update appointment
        cursor.execute("""
            UPDATE Appointment SET
                Patient_ID = %s,
                Schedule = %s,
                Status = %s
            WHERE Appointment_ID = %s
        """, (
            appointment_data['Patient_ID'],
            appointment_data['Schedule'],
            appointment_data['Status'],
            appointment_data['Appointment_ID']
        ))
        
        # Delete existing treatments
        cursor.execute("""
            DELETE FROM Treatment
            WHERE Appointment_ID = %s
        """, (appointment_data['Appointment_ID'],))
        
        # Add new treatments
        for treatment in appointment_data['Treatments']:
            cursor.execute("""
                INSERT INTO Treatment (
                    Treatment_ID,
                    Appointment_ID,
                    Treatment_Procedure,
                    Cost
                ) VALUES (%s, %s, %s, %s)
            """, (
                treatment['Treatment_ID'],
                appointment_data['Appointment_ID'],
                treatment['Treatment_Procedure'],
                treatment['Cost']
            ))
        
        conn.commit()
        return True
        
    except Exception as e:
        print("Error updating appointment:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# Function to search patients by name
# This function searches for patients by their first, middle, or last name.
# It returns a list of dictionaries containing the Patient_ID and Full_Name of matched patients.
# The search is case-insensitive and uses wildcards to match any part of the name.
def get_patients_name():
    matched_patients = []

    conn = connectDB()
    cursor = conn.cursor()

    query = """
        SELECT 
            Patient_ID,
            CONCAT(First_Name, ' ', Middle_Name, ' ', Last_Name) AS Full_Name
        FROM Patient
    """
    cursor.execute(query)

    result = cursor.fetchall()
    if result:
        for row in result:
            matched_patients.append({
                "Patient_ID": row[0],
                "Full_Name": row[1]
            })

    cursor.close()
    conn.close()

    return matched_patients














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
        
        
from backend.DB import connectDB




def perform_appointment_deletion(appointment_id):
    conn = connectDB()
    cursor = conn.cursor()
    try:
        # Delete all treatments related to the appointment first
        cursor.execute("""
            DELETE FROM Treatment
            WHERE Appointment_ID = %s
        """, (appointment_id,))
        
        # Delete the appointment itself
        cursor.execute("""
            DELETE FROM Appointment
            WHERE Appointment_ID = %s
        """, (appointment_id,))

        conn.commit()
        success = True
    except Exception as e:
        print("Delete Appointment Error:", e)
        import traceback
        traceback.print_exc()
        conn.rollback()
        success = False
    finally:
        cursor.close()
        conn.close()
    return success



        