import smtplib
import ssl
import os


def send_email(message, category):
    sender_email = 'support@alpha-automate.com'
    receiver_email = 'eleluabdulkareem@gmail.com'
    if category == "New trade":
        subject = "New trade"
    else:
        subject = "Warning notification"
    port = 465  # For SSL
    password = ""
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("mail.privateemail.com", port, context=context) as server:
        server.login(sender_email, password)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, receiver_email, email_message)
