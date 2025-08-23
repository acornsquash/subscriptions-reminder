import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env and sets os.environ

EMAIL = os.environ["EMAIL"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]


def send_email(subject: str, body: str):
    
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = os.environ["EMAIL"]
    msg["To"] = os.environ["EMAIL"]

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.environ["EMAIL"], os.environ["EMAIL_PASSWORD"])
        smtp.send_message(msg)
