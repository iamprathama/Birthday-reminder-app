# utils/scheduler.py

import os
from datetime import date
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the Flask app and required modules
from app import create_app, db
from app.model import Birthday
from app.utils.email_reminder import send_admin_email

# Create the Flask app
app = create_app()

# Use app context to access the database
with app.app_context():
    today = date.today()

    # Query all birthdays matching today's month and day
    birthdays_today = Birthday.query.filter(
        db.extract('month', Birthday.date) == today.month,
        db.extract('day', Birthday.date) == today.day
    ).all()

    # Send email for each birthday
    for birthday in birthdays_today:
        send_admin_email(birthday)

    print(f"✅ Scheduler ran successfully. Emails sent: {len(birthdays_today)}")
