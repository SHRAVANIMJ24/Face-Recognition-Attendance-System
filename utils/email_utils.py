import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import tkinter.messagebox as mess
import time
import os

def send_email(recipient_email, selected_domain, date):
    if not recipient_email:
        mess._show(title='Error', message='Please enter a recipient email address.')
        return

    recipient_email += "@" + selected_domain

    from_email = "gudujadhav007@gmail.com"
    password = "iypg sllt qvkh uvsy"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = recipient_email
    msg['Subject'] = "Today's Attendance Report , Date = " + date + ", Time = " + time.strftime('%I:%M:%S %p')

    body = "Please find attached the attendance report."
    msg.attach(MIMEText(body, 'plain'))

    filename = f"Attendance/Attendance_{date}.csv"
    try:
        with open(filename, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={filename}")
            msg.attach(part)
    except FileNotFoundError:
        mess._show(title='Error', message=f"Attendance file {filename} not found.")
        return

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, recipient_email, msg.as_string())
        server.quit()
        mess._show(title='Success', message='Attendance report sent successfully.')
    except Exception as e:
        print(e)
        mess._show(title='Error', message='Failed to send email. Please try again.')
