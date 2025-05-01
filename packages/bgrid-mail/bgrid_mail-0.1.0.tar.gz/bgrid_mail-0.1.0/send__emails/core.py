import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(email, subject, body):
    # Prompt for the sender's email and password
    sender_email = input("Enter your email: ")
    password = input("Enter your email password (App password preferred): ")

    smtp_server = "smtp.zoho.in"
    smtp_port = 465

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = email
    message.attach(MIMEText(body, "html"))

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())

    print(f"✅ Email sent to {email}")
