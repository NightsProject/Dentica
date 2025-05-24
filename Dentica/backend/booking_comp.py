from backend.DB import connectDB


def get_all_bookings():
    bookings = []

    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            b.Booking_ID,
            b.Appointment_ID,
            CONCAT(p.First_Name, ' ', p.Middle_Name, ' ', p.Last_Name) AS Patient_Full_Name,
            b.Booking_Date_Time
        FROM Books b
        JOIN Patient p ON b.Patient_ID = p.Patient_ID
        ORDER BY CAST(SUBSTRING(b.Booking_ID, 2) AS UNSIGNED)
    """)

    results = cursor.fetchall()
    for row in results:
        # Format datetime string if needed
        booking_dt = row[3]
        if hasattr(booking_dt, 'strftime'):
            booking_dt = booking_dt.strftime('%Y-%m-%d %H:%M:%S')

        bookings.append([row[0], row[1], row[2], booking_dt])

    cursor.close()
    conn.close()

    return bookings


def generate_new_booking_id():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Booking_ID
        FROM Books
        ORDER BY CAST(SUBSTRING(Booking_ID, 2) AS UNSIGNED)
    """)

    existing_ids = cursor.fetchall()
    cursor.close()
    conn.close()

    # Look for the first missing ID in sequence
    expected_id = 1
    for (booking_id,) in existing_ids:
        num_id = int(booking_id[1:])  # Remove 'B' prefix and convert to int
        if num_id != expected_id:
            break
        expected_id += 1

    new_booking_id = f'B{expected_id:05d}'  # Zero-padded to 5 digits
    return new_booking_id

def search_bookings(keyword):
    conn   = connectDB()
    cursor = conn.cursor()

    kw = keyword.lower()
    like_kw = f"%{kw}%"

    query = """
        SELECT
            b.Booking_ID,
            b.Appointment_ID,
            CONCAT(p.First_Name, ' ',
                   p.Middle_Name, ' ',
                   p.Last_Name)       AS Patient_Full_Name,
            b.Booking_Date_Time
        FROM Books AS b
        JOIN Patient AS p
          ON b.Patient_ID = p.Patient_ID
        WHERE
            LOWER(b.Booking_ID)                    LIKE %s
         OR LOWER(b.Appointment_ID)              LIKE %s
         OR LOWER(CONCAT(p.First_Name, ' ',
                         p.Middle_Name, ' ',
                         p.Last_Name))             LIKE %s
         OR CAST(b.Booking_Date_Time AS CHAR)    LIKE %s
        ORDER BY b.Booking_Date_Time
    """

    params = [like_kw, like_kw, like_kw, like_kw]

    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Each row: [Booking_ID, Patient_Full_Name, Appointment_ID, Booking_Date_Time]
    return [list(r) for r in rows]
