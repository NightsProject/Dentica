import random
import datetime
from faker import Faker

fake = Faker()

# Dental-specific constants
dental_diagnoses = [
    'Caries', 'Gingivitis', 'Periodontitis', 'Tooth Sensitivity',
    'Oral Ulcer', 'Impacted Tooth', 'Abscess'
]
dental_procedures = [
    'Cleaning', 'Filling', 'Extraction', 'Root Canal',
    'Crown', 'Bridge', 'Teeth Whitening', 'Implant'
]

# General constants
genders = ['Male', 'Female', 'Other']
statuses = ['Scheduled', 'Completed', 'Cancelled']
treatment_statuses = ['Completed', 'In-Progress', 'Waiting', 'Canceled']
payment_methods = ['Cash', 'Card', 'GCash', 'None']
payment_statuses = ['Paid', 'Unpaid']

# Helper functions
def generate_id(prefix, num, length=6):
    return prefix + str(num).zfill(length - len(prefix))

def fmt(val):
    if val is None:
        return "NULL"
    if isinstance(val, (datetime.date, datetime.datetime)):
        return f"'{val}'"
    return "'" + str(val).replace("'", "''") + "'"

# Generate Patients
patients = []
for i in range(100):
    patients.append({
        'Patient_ID': generate_id('P', i),
        'First_Name': fake.first_name(),
        'Middle_Name': fake.first_name(),
        'Last_Name': fake.last_name(),
        'Gender': random.choice(genders),
        'Birth_Date': fake.date_of_birth(minimum_age=1, maximum_age=90),
        'Contact_Number': fake.phone_number()[:15],
        'Email': fake.email(),
        'Address': fake.address().replace("\n", ", "),
    })

# Generate Appointments
appointments = []
today = datetime.datetime.now().replace(microsecond=0)
for i in range(100):
    sched = today + datetime.timedelta(
        days=random.randint(-30, 10),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    appointments.append({
        'Appointment_ID': generate_id('A', i),
        'Patient_ID': random.choice(patients)['Patient_ID'],
        'Schedule': sched,
        'Status': random.choice(statuses),
    })

# Generate Treatments (1–3 per appointment)
treatments = []
for appt in appointments:
    for tid in range(1, random.randint(1, 3) + 1):
        treatments.append({
            'Appointment_ID': appt['Appointment_ID'],
            'Treatment_ID': tid,
            'Diagnosis': random.choice(dental_diagnoses),
            'Cost': round(random.uniform(100, 1000), 4),
            'Treatment_Procedure': random.choice(dental_procedures),
            'Treatment_Date_Time': appt['Schedule'] + datetime.timedelta(hours=random.randint(0, 2)),
            'Treatment_Status': random.choice(treatment_statuses),
        })

# Generate Bookings
bookings = []
for idx, appt in enumerate(appointments):
    bookings.append({
        'Booking_ID': generate_id('B', idx),
        'Patient_ID': appt['Patient_ID'],
        'Appointment_ID': appt['Appointment_ID'],
        'Booking_Date_Time': appt['Schedule'] - datetime.timedelta(days=random.randint(1, 5)),
    })

# Generate Cancellations
cancellations = []
for appt in appointments:
    if appt['Status'] == 'Cancelled':
        cancellations.append({
            'Patient_ID': appt['Patient_ID'],
            'Appointment_ID': appt['Appointment_ID'],
            'Cancellation_Date_Time': appt['Schedule'] - datetime.timedelta(hours=random.randint(1, 12)),
            'Reason': fake.sentence(nb_words=6),
        })

# Generate Payments (with 'PY' prefix for Payment_ID)
payments = []
for idx, appt in enumerate(appointments):
    status = random.choice(payment_statuses)
    method = random.choice(payment_methods) if status == 'Paid' else 'None'
    pay_date = appt['Schedule'] + datetime.timedelta(days=1) if status == 'Paid' else None
    payments.append({
        'Payment_ID': generate_id('PY', idx, length=7),
        'Patient_ID': appt['Patient_ID'],
        'Appointment_ID': appt['Appointment_ID'],
        'Total_Amount': round(random.uniform(150, 2000), 4),
        'Payment_Method': method,
        'Payment_Status': status,
        'Payment_Date': pay_date,
    })

# Function to generate INSERT statements
def insert_statements(table, rows):
    if not rows:
        return ""
    cols = list(rows[0].keys())
    stmts = f"INSERT INTO {table} ({', '.join(cols)}) VALUES\n"
    vals = []
    for r in rows:
        vals.append("(" + ", ".join(fmt(r[c]) for c in cols) + ")")
    return stmts + ",\n".join(vals) + ";\n\n"

# Compose and save the SQL file
sql = ''
for tbl, data in [
    ('Patient', patients),
    ('Appointment', appointments),
    ('Treatment', treatments),
    ('Books', bookings),
    ('Cancel', cancellations),
    ('Pays', payments)
]:
    sql += insert_statements(tbl, data)

with open('dental_data.sql', 'w') as f:
    f.write(sql)

print('dental_data.sql generated with dental-specific records.')
