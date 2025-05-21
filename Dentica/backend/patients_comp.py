from backend.DB import connectDB
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
