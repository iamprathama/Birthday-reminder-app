# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from dotenv import load_dotenv
# from app.model import User

# load_dotenv()

# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")

# def send_admin_email(birthday):
#     try:
#         user = User.query.get(birthday.user_id)
#         if not user or not user.email:
#             print("⚠️ User not found or has no email.")
#             return

#         msg = MIMEMultipart()
#         msg['From'] = EMAIL_USER
#         msg['To'] = user.email
#         msg['Subject'] = f"🎉 Birthday Reminder: {birthday.name}'s Birthday Today!"

#         body = f"""
#         Hi {user.name},

#         🎂 Just a reminder that today is {birthday.name}'s birthday!
#         🎈 Relationship: {birthday.relationship or "Not specified"}
#         📅 Date: {birthday.date.strftime('%d %B')}

#         Don’t forget to wish them! 😊
#         """
#         msg.attach(MIMEText(body, 'plain'))

#         with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
#             server.login(EMAIL_USER, EMAIL_PASS)
#             server.send_message(msg)

#         print(f"✅ Email sent to {user.email} for {birthday.name}")
#     except Exception as e:
#         print(f"❌ Failed to send email: {str(e)}")

# import smtplib
# import os
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from dotenv import load_dotenv
# from flask import session
# load_dotenv()


# EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
# ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

# def send_admin_email(birthday):
#     try:
#         user_email = session.get('user_email')
#         if not user_email:
#             print("❌ No user email in session. Cannot send email.")
#             return

#         msg = MIMEMultipart()
#         msg['From'] = ADMIN_EMAIL
#         msg['To'] =  user_email
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

#         # Send the email
#         with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             server.starttls()
#             server.login(ADMIN_EMAIL, EMAIL_PASSWORD)
#             server.send_message(msg)

#         print(f"✅ Email reminder sent for {birthday.name}")
#     except Exception as e:
#         print("❌ Email sending failed:", e)  
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
from flask import session
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

def send_admin_email(birthday):
    try:
        user_email = session.get('user_email') or ADMIN_EMAIL
        if not user_email:
            print("❌ No user email in session. Cannot send email.")
            return

        msg = MIMEMultipart()
        msg['From'] = ADMIN_EMAIL
        msg['To'] = user_email
        msg['Subject'] = f"🎂 Reminder: {birthday.name}'s Birthday Today!"

        body = f"Hi! 🎉\n\nJust a reminder that {birthday.name}'s birthday is today! 🎂\n\nRelationship: {birthday.relationship or 'Not specified'}\n\n🎈 Have a great day!"
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(ADMIN_EMAIL, EMAIL_PASSWORD)
            server.sendmail(ADMIN_EMAIL, user_email, msg.as_string())

        print(f"✅ Email sent to {user_email} for {birthday.name}'s birthday.")
    except Exception as e:
        print(f"❌ Email error: {e}")
