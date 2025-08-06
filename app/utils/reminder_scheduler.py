# utils/scheduler.py

# utils/scheduler.py

from datetime import date
from app import create_app, db
from app.model import Birthday
from app.utils.email_reminder import send_admin_email

def run_scheduler():
    today = date.today()

    birthdays_today = Birthday.query.filter(
        db.extract('month', Birthday.date) == today.month,
        db.extract('day', Birthday.date) == today.day
    ).all()

    for birthday in birthdays_today:
        send_admin_email(birthday)

    print(f"✅ Scheduler ran successfully. Emails sent: {len(birthdays_today)}")
    return f"✅ Scheduler ran successfully. Emails sent: {len(birthdays_today)}"