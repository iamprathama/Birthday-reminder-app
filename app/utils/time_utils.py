from datetime import datetime
import pytz

def get_ist_today():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist).date()
