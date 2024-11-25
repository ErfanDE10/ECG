import streamlit as st
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random 
import requests  

# firebase URL
firebase_url = "https://precg-e4e8e-default-rtdb.firebaseio.com/"

# normal ranges
NORMAL_HEART_RATE_MIN = 60
NORMAL_HEART_RATE_MAX = 100
LOW_OXYGEN_THRESHOLD = 90

# email init
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "tech.core.engine@gmail.com"
SENDER_PASSWORD = "nkpo liry nguz aogk"  
RECIPIENT_EMAIL = "m.erfanzarabadipour@gmail.com"

# email status
last_email_time = {"heart_rate": 0, "oxygen": 0}
EMAIL_INTERVAL = 300  # 5 min


def get_data_from_firebase():
    try:
        heart_rate = requests.get(f"{firebase_url}/heart_rate.json").json()
        oxygen_level = requests.get(f"{firebase_url}/oxygen_level.json").json()

        # set range if the data cant get from data base 
        heart_rate = int(heart_rate) if heart_rate is not None else -1
        oxygen_level = int(oxygen_level) if oxygen_level is not None else -1

        return heart_rate, oxygen_level
    except Exception as e:
        st.error(f"Error fetching data from Firebase: {e}")
        return -1, -1

# simulation
def get_test_data():
    heart_rate = random.randint(50, 120)  
    oxygen_level = random.randint(85, 100)  
    return heart_rate, oxygen_level

# send email
def send_email(subject, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        st.success(f"Email sent: {subject}")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# alert
def check_alerts(heart_rate, oxygen_level):
    global last_email_time
    current_time = time.time()

    if heart_rate > NORMAL_HEART_RATE_MAX and current_time - last_email_time["heart_rate"] > EMAIL_INTERVAL:
        message = f"High Heart Rate Alert! Current heart rate: {heart_rate} bpm"
        send_email("High Heart Rate Alert", message)
        last_email_time["heart_rate"] = current_time

    elif heart_rate < NORMAL_HEART_RATE_MIN and current_time - last_email_time["heart_rate"] > EMAIL_INTERVAL:
        message = f"Low Heart Rate Alert! Current heart rate: {heart_rate} bpm"
        send_email("Low Heart Rate Alert", message)
        last_email_time["heart_rate"] = current_time

    if oxygen_level < LOW_OXYGEN_THRESHOLD and current_time - last_email_time["oxygen"] > EMAIL_INTERVAL:
        message = f"Low Oxygen Level Alert! Current oxygen level: {oxygen_level}%"
        send_email("Low Oxygen Level Alert", message)
        last_email_time["oxygen"] = current_time

# Streamlit
st.title("Heart Rate and Oxygen Monitoring")

mode = st.radio("Select Mode", ["Test Mode", "Real Mode"])

placeholder = st.empty()

if st.button("Start Monitoring"):
    while True:
        if mode == "Test Mode":
            heart_rate, oxygen_level = get_test_data()
        elif mode == "Real Mode":
            heart_rate, oxygen_level = get_data_from_firebase()

        with placeholder.container():
            st.metric("Heart Rate", f"{heart_rate} bpm")
            st.metric("Oxygen Level", f"{oxygen_level}%")

        check_alerts(heart_rate, oxygen_level)
        time.sleep(2)
