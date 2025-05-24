from backend.DB import connectDB

from Frontend.Graphs.Total_Appointment_Status import DonutChart1
from Frontend.Graphs.Payment_Method import PaymentMethodPie
from Frontend.Graphs.Gender_Distribution import GenderDistributionPie
from Frontend.Graphs.Age_Distribution import PatientAgeDistributionPie
from Frontend.Graphs.Appointment_overtime import AppointmentLineChart
from Frontend.Graphs.Monthly_Revenue import QuarterlyRevenueLineChart
from Frontend.Graphs.Common_Treatments import CommonTreatmentsBarChart
from Frontend.Graphs.Treatment_Cost import TreatmentCostsLineChart

def load_graphs():
    total_status = create_total_appointment_status_graph()
    payment_method = create_payment_method_dist_graph()
    gender_dist = create_gender_dist_graph()
    age_dist = create_age_dist_graph()
    app_quarterly = create_quarterly_app_graph()
    rev_quarterly = create_quarterly_revenue_graph()
    comm_treat = create_common_treatments_graph()
    treat_cost = create_treatment_costs_over_time_graph()
    
    return total_status, payment_method, gender_dist, age_dist, app_quarterly,  rev_quarterly,  comm_treat, treat_cost

def refresh_graphs(self):
    if self.tot_appstat_chart:
        self.tot_appstat_layout.removeWidget(self.tot_appstat_chart)
        self.tot_appstat_chart.deleteLater()
        self.tot_appstat_chart = None

    if self.payment_method_chart:
        self.payment_method_layout.removeWidget(self.payment_method_chart)
        self.payment_method_chart.deleteLater()
        self.payment_method_chart = None

    if self.gender_dist_chart:
        self.gender_dist_layout.removeWidget(self.gender_dist_chart)
        self.gender_dist_chart.deleteLater()
        self.gender_dist_chart = None

    if self.age_dist_chart:
        self.age_dist_layout.removeWidget(self.age_dist_chart)
        self.age_dist_chart.deleteLater()
        self.age_dist_chart = None

    if self.app_ot_chart:
         self.app_ot_layout.removeWidget(self.app_ot_chart)
         self.app_ot_chart.deleteLater()
         self.app_ot_chart = None
         
    if self.quarterly_rev_chart:
         self.quarterly_rev_layout.removeWidget(self.quarterly_rev_chart)
         self.quarterly_rev_chart.deleteLater()
         self.quarterly_rev_chart = None
    
    if self.Comm_treat_chart:
         self.common_treatments_layout.removeWidget(self.Comm_treat_chart)
         self.Comm_treat_chart.deleteLater()
         self.Comm_treat_chart = None
         
    if self.treat_cost_chart:
         self.treat_cost_layout.removeWidget(self.treat_cost_chart)
         self.treat_cost_chart.deleteLater()
         self.treat_cost_chart = None
         
    self.tot_appstat_chart, self.payment_method_chart, self.gender_dist_chart, self.age_dist_chart, self.app_ot_chart, self.quarterly_rev_chart, self.Comm_treat_chart, self.treat_cost_chart = load_graphs()

    self.tot_appstat_layout.addWidget(self.tot_appstat_chart)
    self.payment_method_layout.addWidget(self.payment_method_chart)
    self.gender_dist_layout.addWidget(self.gender_dist_chart)
    self.age_dist_layout.addWidget(self.age_dist_chart)
    self.app_ot_layout.addWidget(self.app_ot_chart)
    self.quarterly_rev_layout.addWidget(self.quarterly_rev_chart)
    self.common_treatments_layout.addWidget(self.Comm_treat_chart)
    self.treat_cost_layout.addWidget(self.treat_cost_chart)
    

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
        
def get_appointments_per_quarter():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            CONCAT(YEAR(Schedule), '-Q', QUARTER(Schedule)) AS Period,
            COUNT(*) AS Appointment_Count
        FROM Appointment
        GROUP BY Period
        ORDER BY Period;
    """)

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    periods = []
    counts = []
    for period, count in results:
        periods.append(period)
        counts.append(count)

    return periods, counts

def create_quarterly_app_graph():
    try:
        periods, counts = get_appointments_per_quarter()
        chart_widget = AppointmentLineChart(periods, counts)
        return chart_widget
    except Exception as e:
        print("Error loading quarterly appointments chart:", e)
        return None

def get_quarterly_revenue():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Quarter,
            SUM(Total_Amount) AS Total_Revenue
        FROM (
            SELECT 
                CONCAT(YEAR(Payment_Date), '-Q', QUARTER(Payment_Date)) AS Quarter,
                Total_Amount
            FROM Pays
            WHERE Payment_Status = 'Paid'
        ) AS sub
        GROUP BY Quarter
        ORDER BY Quarter;
    """)

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    quarters = []
    revenues = []
    for quarter, total in results:
        quarters.append(quarter)
        revenues.append(total)
        
    return quarters, revenues


def create_quarterly_revenue_graph():
    try:
        quarters, revenues = get_quarterly_revenue()
        chart_widget = QuarterlyRevenueLineChart(quarters, revenues)  
        return chart_widget
    except Exception as e:
        print("Error loading quarterly revenue chart:", e)
        return None

def get_common_treatments_count():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Treatment_Procedure, COUNT(*) AS Count
        FROM Treatment
        GROUP BY Treatment_Procedure
        ORDER BY Count DESC
        LIMIT 5;
    """)

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    procedures = []
    counts = []
    for procedure, count in results:
        procedures.append(procedure)
        counts.append(count)

    return procedures, counts


def create_common_treatments_graph():
    try:
        procedures, counts = get_common_treatments_count()
        chart_widget = CommonTreatmentsBarChart(procedures, counts)  
        return chart_widget
    except Exception as e:
        print("Error loading common treatments chart:", e)
        return None

def get_treatment_costs_per_quarter():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            CONCAT(YEAR(Treatment_Date_Time), '-Q', QUARTER(Treatment_Date_Time)) AS Year_Quarter,
            SUM(Cost) AS Total_Cost
        FROM Treatment
        GROUP BY Year_Quarter
        ORDER BY Year_Quarter;
    """)

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    quarters = []
    costs = []
    for quarter, cost in results:
        quarters.append(quarter)
        costs.append(cost)

    return quarters, costs

def create_treatment_costs_over_time_graph():
    try:
        quarters, costs = get_treatment_costs_per_quarter()
        chart_widget = TreatmentCostsLineChart(quarters, costs)
        return chart_widget
    except Exception as e:
        print("Error loading treatment costs over time chart:", e)
        return None
