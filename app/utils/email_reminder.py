import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from flask import session
load_dotenv()


EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

def send_admin_email(birthday):
    try:
        user_email = session.get('user_email')
        if not user_email:
            print("❌ No user email in session. Cannot send email.")
            return

        msg = MIMEMultipart()
        msg['From'] = ADMIN_EMAIL
        msg['To'] =  user_email
        msg['Subject'] = f"🎉 Birthday Reminder: {birthday.name}"

        body = f"""
        Hello 👋,

        Today is {birthday.name}'s birthday! 🥳

        🎂 Date of Birth: {birthday.date.strftime('%d %B, %Y')}

        Don't forget to wish them!

        Regards,
        Your Birthday Reminder App
        """
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(ADMIN_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email reminder sent for {birthday.name}")
    except Exception as e:
        print("❌ Email sending failed:", e)  
# import smtplib
# import os
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from dotenv import load_dotenv

# load_dotenv()

# EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
# ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")  # Email that will receive the reminder

# def send_admin_email(birthday):
#     try:
#         # Use ADMIN_EMAIL or birthday.email depending on your logic
#         recipient_email = ADMIN_EMAIL  

#         msg = MIMEMultipart()
#         msg['From'] = ADMIN_EMAIL
#         msg['To'] = recipient_email
#         msg['Subject'] = f"🎉 Birthday Reminder: {birthday.name}"

#         body = f"""
#         Hello 👋,

#         Today is {birthday.name}'s birthday! 🥳

#         🎂 Date of Birth: {birthday.date.strftime('%d %B, %Y')}

#         Don't forget to wish them!

#         Regards,
#         Your Birthday Reminder App
#         """
#         msg.attach(MIMEText(body, 'plain'))

#         with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             server.starttls()
#             server.login(ADMIN_EMAIL, EMAIL_PASSWORD)
#             server.send_message(msg)

#         print(f"✅ Email reminder sent for {birthday.name}")
#     except Exception as e:
#         print("❌ Email sending failed:", e)
