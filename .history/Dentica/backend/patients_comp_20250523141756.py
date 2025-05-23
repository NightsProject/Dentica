from backend.DB import connectDB

# Function to get all patients from the database
# This function retrieves all patients from the Patient table and returns them as a list of tuples.
def get_all_patients():
    all_patients = []

    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            Patient_ID,
            CONCAT(First_Name, ' ', Middle_Name, ' ', Last_Name) AS Full_Name,
            Gender,
            Birth_Date,
            Contact_Number,
            Email,
            Address
        FROM Patient
    """)
    result = cursor.fetchall()
    if result:
        for row in result:
            all_patients.append(row)

    cursor.close()
    conn.close()
    
    #print("\nAll Patients:", all_patients)
    return all_patients


def generate_new_patient_id():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Patient_ID 
        FROM Patient 
        ORDER BY CAST(SUBSTRING(Patient_ID, 2) AS UNSIGNED) DESC 
        LIMIT 1
    """)

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        last_id = int(result[0][1:])  # Remove the 'P' and convert the number part
        new_id_num = last_id + 1
    else:
        new_id_num = 1  # Start from 1 if there are no patients yet

    new_patient_id = f'P{new_id_num:05d}'  # Zero-padded to 5 digits
    return new_patient_id



## Function to insert a new patient into the database
# This function takes various patient details as parameters and inserts them into the Patient table.
# It returns True if the insertion is successful, otherwise it returns False.
# The function uses a try-except block to handle any exceptions that may occur during the database operation.
def insert_patient(
    patient_id,
    first_name,
    middle_name,
    last_name,
    gender,
    birth_date,
    contact_number,
    email,
    address
):
    conn = connectDB()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Patient (
                Patient_ID,
                First_Name,
                Middle_Name,
                Last_Name,
                Gender,
                Birth_Date,
                Contact_Number,
                Email,
                Address
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            patient_id,
            first_name,
            middle_name,
            last_name,
            gender,
            birth_date,
            contact_number,
            email,
            address
        ))
        conn.commit()
        success = True
    except Exception as e:
        print("Insert Patient Error:", e)
        import traceback
        traceback.print_exc()
        success = False
    finally:
        cursor.close()
        conn.close()
    return success

# Function to delete a patient from the database and its assiocated datas
# This function takes a patient ID as a parameter and deletes the corresponding record from the Patient table.

def perform_patient_deletion(patient_id):
    conn = connectDB()
    cursor = conn.cursor()
    try:
        # Delete all treatments related to appointments of the patient
        cursor.execute("""
            DELETE t FROM Treatment t
            JOIN Appointment a ON t.Appointment_ID = a.Appointment_ID
            WHERE a.Patient_ID = %s
        """, (patient_id,))

        # Delete all appointments of the patient
        cursor.execute("""
            DELETE FROM Appointment
            WHERE Patient_ID = %s
        """, (patient_id,))

        # Delete all bookings related to the patient
        cursor.execute("""
            DELETE FROM Books
            WHERE Patient_ID = %s
        """, (patient_id,))

        # Delete all cancellations related to the patient
        cursor.execute("""
            DELETE FROM Cancel
            WHERE Patient_ID = %s
        """, (patient_id,))

        # Delete all payments related to the patient
        cursor.execute("""
            DELETE FROM Pays
            WHERE Patient_ID = %s
        """, (patient_id,))

        # Finally, delete the patient
        cursor.execute("""
            DELETE FROM Patient
            WHERE Patient_ID = %s
        """, (patient_id,))

        conn.commit()
        success = True
    except Exception as e:
        print("Delete Patient Error:", e)
        import traceback
        traceback.print_exc()
        conn.rollback()
        success = False
    finally:
        cursor.close()
        conn.close()
    return success
