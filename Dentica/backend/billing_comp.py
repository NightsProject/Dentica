
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
            p.Payment_Status,
            p.Payment_Date
        FROM Pays p
        JOIN Patient pa ON p.Patient_ID = pa.Patient_ID
        ORDER BY CAST(SUBSTRING(p.Payment_ID, 3) AS UNSIGNED)
    """)
    
    result = cursor.fetchall()
    if result:
        for row in result:
            billings.append(row)

    cursor.close()
    conn.close()
    
    return billings


def generate_new_payment_id():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Payment_ID 
        FROM Pays 
        ORDER BY CAST(SUBSTRING(Payment_ID, 3) AS UNSIGNED)
    """)

    existing_ids = cursor.fetchall()
    cursor.close()
    conn.close()

    # Look for the first missing ID in sequence
    expected_id = 1
    for (payment_id,) in existing_ids:
        num_id = int(payment_id[2:])  # Remove 'PY' prefix and convert to int
        if num_id != expected_id:
            break
        expected_id += 1

    new_payment_id = f'PY{expected_id:05d}'  # Zero-padded to 5 digits
    return new_payment_id


def search_payments(keyword):
    conn   = connectDB()
    cursor = conn.cursor()

    kw = keyword.lower()
    like_kw = f"%{kw}%"

    query = """
        SELECT
            pay.Payment_ID,
            CONCAT(pat.First_Name, ' ',
                   pat.Middle_Name, ' ',
                   pat.Last_Name)    AS Patient_Full_Name,
            pay.Appointment_ID,
            pay.Total_Amount,
            pay.Payment_Method,
            pay.Payment_Status
        FROM Pays AS pay
        JOIN Patient AS pat
          ON pay.Patient_ID = pat.Patient_ID
        WHERE
            LOWER(pay.Payment_ID)         LIKE %s
         OR LOWER(pat.First_Name)       LIKE %s
         OR LOWER(pat.Middle_Name)      LIKE %s
         OR LOWER(pat.Last_Name)        LIKE %s
         OR LOWER(CONCAT(pat.First_Name, ' ',
                         pat.Middle_Name, ' ',
                         pat.Last_Name))    LIKE %s
         OR LOWER(pay.Appointment_ID)   LIKE %s
         OR CAST(pay.Total_Amount AS CHAR) LIKE %s
         OR LOWER(pay.Payment_Method)   LIKE %s
         OR LOWER(pay.Payment_Status)   LIKE %s
        ORDER BY pay.Payment_ID
    """

    # include both individual name‐parts and the full name for maximum flexibility
    params = [
        like_kw,
        like_kw,
        like_kw,
        like_kw,
        like_kw,
        like_kw,
        like_kw,
        like_kw,
        like_kw
    ]

    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Each row: [Payment_ID, Patient_Full_Name, Appointment_ID, Total_Amount, Payment_Method, Payment_Status]
    return [list(r) for r in rows]
