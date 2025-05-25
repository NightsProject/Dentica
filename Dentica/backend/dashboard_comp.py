from backend.DB import connectDB
from ui.ui_main_window import Ui_MainWindow
from Frontend.Graphs.Appointment_status import DonutChart

def load_summary():
    patients = count_patients()
    appointments = todays_appointments()
    payments = pending_payments()
    treatments = completed_treatments()
    
    data = [patients, appointments, payments, treatments]
    
    return data

def count_patients():
    """
    Returns the number of unique patients who have at least one *scheduled* appointment for today.
    """
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS patient_count
        FROM (
            SELECT 1
            FROM Appointment
            WHERE DATE(Schedule) = CURDATE()
              AND Status = 'Scheduled'
            GROUP BY Patient_ID
        ) AS unique_patients;
    """)

    result = cursor.fetchone()
    patient_count = result[0] if result else 0

    cursor.close()
    conn.close()

    print("Patients with scheduled appointments today:", patient_count)
    return patient_count

def todays_appointments():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) 
        FROM Appointment 
        WHERE DATE(Schedule) = CURDATE()
    """)

    result = cursor.fetchone()
    appointments = result[0] if result else 0

    cursor.close()
    conn.close()

    return str(appointments)


def pending_payments():
    unpaid_payments = 0
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Pays 
        WHERE Payment_Status = 'Unpaid'
    """)
    result = cursor.fetchone()
    if result:
        unpaid_payments = result[0]
    cursor.close()
    conn.close()
    return str(unpaid_payments)


def completed_treatments():
    conn = connectDB()
    cursor = conn.cursor()

    # Count completed treatments for today on Scheduled appointments (excluding canceled treatments)
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Treatment t
        JOIN Appointment a 
          ON t.Appointment_ID = a.Appointment_ID
        WHERE t.Treatment_Status = 'Completed'
          AND DATE(t.Treatment_Date_Time) = CURDATE()
          AND a.Status = 'Scheduled'
    """)
    completed_result = cursor.fetchone()
    completed_treatments = completed_result[0] if completed_result else 0

    # Count all non-canceled treatments for today on Scheduled appointments
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Treatment t
        JOIN Appointment a 
          ON t.Appointment_ID = a.Appointment_ID
        WHERE t.Treatment_Status != 'Canceled'
          AND DATE(t.Treatment_Date_Time) = CURDATE()
          AND a.Status = 'Scheduled'
    """)
    total_result = cursor.fetchone()
    total_treatments = total_result[0] if total_result else 0

    cursor.close()
    conn.close()

    print("Today's Completed Treatments on Scheduled Appointments:", completed_treatments)
    print("Today's Non-Canceled Treatments on Scheduled Appointments:", total_treatments)
    
    return [completed_treatments, total_treatments]


def get_todays_appointments():
    todays_appointments = []

    conn = connectDB()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            a.Appointment_ID,
            t.Treatment_ID,
            CONCAT(p.First_Name, ' ', p.Middle_Name, ' ', p.Last_Name) AS Patient_Full_Name,
            TIME(t.Treatment_Date_Time) AS Treatment_Time,
            t.Treatment_Procedure,
            t.Treatment_Status
        FROM Appointment a
        JOIN Patient p ON a.Patient_ID = p.Patient_ID
        LEFT JOIN Treatment t ON a.Appointment_ID = t.Appointment_ID
        WHERE DATE(a.Schedule) = CURDATE()
          AND a.Status = 'Scheduled'
        ORDER BY 
            CASE t.Treatment_Status
                WHEN 'Waiting' THEN 1
                WHEN 'In-Progress' THEN 2
                WHEN 'Completed' THEN 3
                ELSE 4
            END,
            t.Treatment_Date_Time
    """)
    
    result = cursor.fetchall()
    if result:
        for row in result:
            todays_appointments.append(row)

    cursor.close()
    conn.close()
    
    return todays_appointments




def get_todays_appointment_status_counts():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Status, COUNT(*) 
        FROM Appointment 
        WHERE DATE(Schedule) = CURDATE()
        GROUP BY Status
    """)
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    # Set default values
    scheduled = 0
    completed = 0
    cancelled = 0

    for status, count in results:
        if status == "Scheduled":
            scheduled = count
        elif status == "Completed":
            completed = count
        elif status == "Cancelled":
            cancelled = count

    return [scheduled, completed, cancelled]

def create_appointment_status_chart():
    try:
        status_counts = get_todays_appointment_status_counts()
        labels = ['Scheduled', 'Completed', 'Cancelled']
        chart_widget = DonutChart(labels, status_counts)
        return chart_widget
    except Exception as e:
        print("Error loading chart:", e)
        return None
    
def refresh_appointment_chart(self):
    if self.appointment_chart:
        self.today_stat_layout.removeWidget(self.appointment_chart)
        self.appointment_chart.deleteLater()
        self.appointment_chart = None

    self.appointment_chart = create_appointment_status_chart()
    if self.appointment_chart:
        self.today_stat_layout.addWidget(self.appointment_chart)


