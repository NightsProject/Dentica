from backend.DB import connectDB
from Frontend.Graphs.Total_Appointment_Status import DonutChart1
from Frontend.Graphs.Payment_Method import PaymentMethodPie
from Frontend.Graphs.Gender_Distribution import GenderDistributionPie
from Frontend.Graphs.Age_Distribution import PatientAgeDistributionPie

def load_graphs():
    total_status = create_total_appointment_status_graph()
    payment_method = create_payment_method_dist_graph()
    gender_dist = create_gender_dist_graph()
    age_dist = create_age_dist_graph()
    
    return total_status, payment_method, gender_dist, age_dist

def get_total_appointment_status_counts():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Status, COUNT(*) 
        FROM Appointment 
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

def create_total_appointment_status_graph():
    try:
        status_counts = get_total_appointment_status_counts()
        labels = ['Scheduled', 'Completed', 'Cancelled']
        chart_widget = DonutChart1(labels, status_counts)
        return chart_widget
    except Exception as e:
        print("Error loading chart:", e)
        return None
    
def get_payment_method_counts():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Payment_method, COUNT(*) 
        FROM Pays 
        GROUP BY Payment_method
    """)
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    # Set default values
    cash = 0
    card = 0
    gcash = 0

    for status, count in results:
        if status == "Cash":
            cash = count
        elif status == "Card":
            card = count
        elif status == "GCash":
            gcash = count
    return [cash, card, gcash]

def create_payment_method_dist_graph():
    try:
        status_counts = get_payment_method_counts()
        labels = ['Cash', 'Card', 'Gcash']
        chart_widget = PaymentMethodPie(labels, status_counts)
        return chart_widget
    except Exception as e:
        print("Error loading chart:", e)
        return None

def get_gender_count():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Gender, COUNT(*) 
        FROM Patient 
        GROUP BY Gender
    """)
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    # Set default values
    female = 0
    male = 0

    for status, count in results:
        if status == "Female":
            female = count
        elif status == "Male":
            male = count
    return [female, male]

def create_gender_dist_graph():
        try:
            status_counts = get_gender_count()
            labels = ['Female', 'Male']
            chart_widget = GenderDistributionPie(labels, status_counts)
            return chart_widget
        except Exception as e:
            print("Error loading chart:", e)
            return None

def get_age_dist_count():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
        CASE
            WHEN TIMESTAMPDIFF(YEAR, Birth_Date, CURDATE()) < 18 THEN '<18'
            WHEN TIMESTAMPDIFF(YEAR, Birth_Date, CURDATE()) BETWEEN 18 AND 30 THEN '18-30'
            WHEN TIMESTAMPDIFF(YEAR, Birth_Date, CURDATE()) BETWEEN 31 AND 50 THEN '31-50'
            ELSE '51+'
        END AS Age_Group,
        COUNT(*) AS Count
        FROM Patient
        GROUP BY Age_Group
    """)
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    # Set default values
    under_18 = 0
    age_18_30 = 0
    age_31_50 = 0
    age_51_plus = 0

    for status, count in results:
        if status == "<18":
            under_18 = count
        elif status == "18-30":
            age_18_30 = count
        elif status == "31-50":
            age_31_50 = count
        elif status == "51+":
            age_51_plus = count
    return [under_18, age_18_30, age_31_50, age_51_plus]

def create_age_dist_graph():
        try:
            status_counts = get_age_dist_count()
            labels = ['<18', '18-30', '31-50', '51+']
            chart_widget = PatientAgeDistributionPie(labels, status_counts)
            return chart_widget
        except Exception as e:
            print("Error loading chart:", e)
            return None