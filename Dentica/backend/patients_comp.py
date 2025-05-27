from backend.DB import connectDB
from PyQt6.QtWidgets import QMessageBox
from PyQt6 import QtWidgets

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
        SELECT CAST(SUBSTRING(Patient_ID, 2) AS UNSIGNED) AS num_id
        FROM Patient
        ORDER BY num_id
    """)

    existing_ids = cursor.fetchall()
    cursor.close()
    conn.close()

    # Extract existing numeric parts into a set for faster lookup
    existing_id_set = set(num_id for (num_id,) in existing_ids)

    # Find the smallest missing positive integer
    expected_id = 1
    while expected_id in existing_id_set:
        expected_id += 1

    new_patient_id = f'P{expected_id:05d}'  # e.g., P00002
    return new_patient_id

def update_patient(
    self,
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
        # Check if another patient (not this one) has the same first and last name
        cursor.execute("""
            SELECT * FROM Patient
            WHERE First_Name = %s AND Last_Name = %s AND Patient_ID != %s AND Middle_Name = %s
        """, (first_name, last_name, patient_id, middle_name))
        duplicate = cursor.fetchone()

        if duplicate:
            QtWidgets.QMessageBox.warning(self, "Duplicate Entry",
                "Another patient with the same name already exists.")
            return False

        # Proceed to update
        cursor.execute("""
            UPDATE Patient SET
                First_Name = %s,
                Middle_Name = %s,
                Last_Name = %s,
                Gender = %s,
                Birth_Date = %s,
                Contact_Number = %s,
                Email = %s,
                Address = %s
            WHERE Patient_ID = %s
        """, (
            first_name,
            middle_name,
            last_name,
            gender,
            birth_date,
            contact_number,
            email,
            address,
            patient_id
        ))

        conn.commit()
        return True

    except Exception as e:
        print("Update Patient Error:", e)
        import traceback
        traceback.print_exc()
        return False

    finally:
        cursor.close()
        conn.close()


## Function to insert a new patient into the database
# This function takes various patient details as parameters and inserts them into the Patient table.
# It returns True if the insertion is successful, otherwise it returns False.
# The function uses a try-except block to handle any exceptions that may occur during the database operation.

def insert_patient(self, 
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
        # Check for duplicate full name of the patient
        cursor.execute("""
            SELECT COUNT(*) FROM Patient
            WHERE First_Name = %s AND Last_Name = %s AND Middle_Name = %s
        """, (first_name, last_name, middle_name))
        count = cursor.fetchone()[0]

        if count > 0:
            QMessageBox.warning(self, "Duplicate Entry",
                    f"A patient with the name {first_name} {middle_name} {last_name} already exists.")
            
            return False

        # Proceed with insertion
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
        return True
    except Exception as e:
        print("Insert Patient Error:", e)
        import traceback
        traceback.print_exc()
        return False
    finally:
        cursor.close()
        conn.close()


# Function to delete a patient from the database and its assiocated datas
# This function takes a patient ID as a parameter and deletes the corresponding record from the Patient table.

def perform_patient_deletion(patient_id):
    conn = connectDB()
    cursor = conn.cursor()
    try:
        # 1) Delete all treatments for this patient’s appointments
        cursor.execute("""
            DELETE t
            FROM Treatment t
            JOIN Appointment a
              ON t.Appointment_ID = a.Appointment_ID
            WHERE a.Patient_ID = %s
        """, (patient_id,))

        # 2) Delete all bookings for this patient
        cursor.execute("""
            DELETE FROM Books
            WHERE Patient_ID = %s
        """, (patient_id,))

        # 3) Delete all cancellations for this patient
        cursor.execute("""
            DELETE FROM Cancel
            WHERE Patient_ID = %s
        """, (patient_id,))

        # 4) Delete all payments for this patient
        cursor.execute("""
            DELETE FROM Pays
            WHERE Patient_ID = %s
        """, (patient_id,))

        # 5) Delete all appointments for this patient
        cursor.execute("""
            DELETE FROM Appointment
            WHERE Patient_ID = %s
        """, (patient_id,))

        # 6) Finally, delete the patient record itself
        cursor.execute("""
            DELETE FROM Patient
            WHERE Patient_ID = %s
        """, (patient_id,))

        conn.commit()
        return True

    except Exception as e:
        print("Delete Patient Error:", e)
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()

def get_patient_data(patient_id):
        try:
            connection = connectDB()
            if connection:
                cursor = connection.cursor(dictionary=True)
                query = ("SELECT Patient_ID, First_Name, Middle_Name, Last_Name, Gender, "
                        "Birth_Date, Contact_Number, Email, Address "
                        "FROM Patient WHERE Patient_ID = %s")
                
                cursor.execute(query, (patient_id,))
                result = cursor.fetchone()
                cursor.close()
                connection.close()
                
                if result:
                    if hasattr(result['Birth_Date'], 'strftime'):
                        result['Birth_Date'] = result['Birth_Date'].strftime('%Y-%m-%d')
                    return result
                return None
        except Exception as e:
            print("Unexpected Error:", e)
            QMessageBox.critical(None, "Error", str(e))
      
def search_patients(keyword):
    conn = connectDB()
    cursor = conn.cursor()

    like_keyword = f"%{keyword}%"
    exact_keyword = keyword.strip()

    cursor.execute("""
        SELECT 
            Patient_ID, 
            CONCAT(First_Name, ' ', Middle_Name, ' ', Last_Name) AS Patient_Full_Name,
            Gender,
            Birth_Date,
            Contact_Number,
            Email,
            Address
        FROM Patient
        WHERE Patient_ID LIKE %s
           OR First_Name LIKE %s
           OR Middle_Name LIKE %s
           OR Last_Name LIKE %s
           OR Gender = %s
           OR Birth_Date LIKE %s
           OR Contact_Number LIKE %s
           OR Email LIKE %s
           OR Address LIKE %s
    """, (
        like_keyword, like_keyword, like_keyword, like_keyword,
        exact_keyword,  
        like_keyword, like_keyword, like_keyword, like_keyword
    ))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    patient_data = [list(row) for row in rows]
    return patient_data

