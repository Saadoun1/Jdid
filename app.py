from flask import Flask, render_template, request
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

TIME_SLOTS = [
    {"label": "11:00 - 12:30", "available": True},
    {"label": "13:00 - 14:30", "available": False},
    {"label": "15:00 - 16:30", "available": True},
    {"label": "17:00 - 18:30", "available": True},
    {"label": "19:00 - 20:30", "available": False}
]

# -------- EMAIL CONFIG --------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"
RECEIVER_EMAIL = "your_email@gmail.com"
# ------------------------------


def get_days(num_days=14):
    days = []
    today = datetime.today().date()

    for i in range(num_days):
        current_day = today + timedelta(days=i)

        if i == 0:
            main_label = "Today"
        elif i == 1:
            main_label = "Tomorrow"
        else:
            main_label = current_day.strftime("%a")

        sub_label = current_day.strftime("%d %b %Y")

        days.append({
            "value": current_day.strftime("%Y-%m-%d"),
            "main_label": main_label,
            "sub_label": sub_label
        })

    return days


@app.route('/')
def home():
    days = get_days()
    return render_template("index.html", slots=TIME_SLOTS, days=days)


@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    phone = request.form['phone']
    sport = request.form['sport']
    date = request.form['date']
    slot = request.form['slot']

    subject = f"New Booking Request - {sport}"
    body = f"""
New reservation request

Name: {name}
Phone: {phone}
Sport: {sport}
Date: {date}
Time Slot: {slot}
"""

    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()

        return f"""
        <h2>Reservation request sent successfully</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Phone:</strong> {phone}</p>
        <p><strong>Sport:</strong> {sport}</p>
        <p><strong>Date:</strong> {date}</p>
        <p><strong>Time Slot:</strong> {slot}</p>
        <br>
        <a href="/">Go back</a>
        """

    except Exception as e:
        return f"""
        <h2>Error sending reservation</h2>
        <p>{str(e)}</p>
        <br>
        <a href="/">Go back</a>
        """


if __name__ == '__main__':
    app.run(debug=True)