from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date
from app.utils.email_reminder import send_admin_email

db = SQLAlchemy()
today_birthday_cache = []  # Global list to store today’s birthdays

def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Scheduler function OUTSIDE the app context block
    def check_today_birthdays():
        with app.app_context():  # ✅ This ensures the function always runs in context
            from app.model import Birthday
            global today_birthday_cache
            today = date.today()
            today_birthday_cache = Birthday.query.filter(
                db.extract('month', Birthday.date) == today.month,
                db.extract('day', Birthday.date) == today.day
            ).all()
            for birthday in  today_birthday_cache:
                send_admin_email(birthday)
            
            print("Today's birthdays:", today_birthday_cache)
            print(f"✅ Checked birthdays on {today}. Sent {len(today_birthday_cache)} emails.")
  
    with app.app_context():
        from app import routes
        from app.model import Birthday
        db.create_all()

    # 🔁 Start scheduler AFTER app is ready
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_today_birthdays, trigger="cron", hour=9, minute=0)

    scheduler.start()

    return app
