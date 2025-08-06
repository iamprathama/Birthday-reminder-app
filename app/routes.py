from flask import render_template, request, redirect, url_for, flash,session
from flask import current_app as app
from app import db
from app.model import User , Birthday
from werkzeug.security import generate_password_hash  ,check_password_hash
from datetime import datetime


from app.utils.email_reminder import send_admin_email
from app.utils.time_utils import get_ist_today
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        username=request.form['name']
        email=request.form['email']
        password=request.form['password']
        hashed_password = generate_password_hash(password)
        user=User(name=username, email=email,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Signup successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id 
            session['user_email'] = user.email 
            flash('Login successful! 🎉')
            return redirect(url_for('dashboard'))  # 🎈 balloons trigger
        else:
            flash('Invalid email or password. Try again.')
            return render_template('login.html')
    
    return render_template('login.html')

from datetime import datetime  # Already imported

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    birthdays = Birthday.query.filter_by(user_id=user_id).all()
    today = get_ist_today()

    
    # Filter only current user's birthdays from cached today list
    today_birthdays = [
        b for b in birthdays 
        if b.date.day == today.day and b.date.month == today.month
    ]
    for birthday in today_birthdays :
        send_admin_email(birthday)  # this should be a Birthday object
        

    return render_template('dashboard.html', birthdays=birthdays, today_birthdays=today_birthdays)
@app.route('/add-birthday', methods=['GET', 'POST'])
def add_birthday():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()

        user_id = session['user_id']
        relationship = request.form['relationship']
        birthday = Birthday(name=name, date=date, user_id=user_id, relationship=relationship)
        db.session.add(birthday)
        db.session.commit()
        flash("Birthday added successfully! 🎉")
        return redirect(url_for('dashboard'))

    return render_template('add-birthday.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/delete/<int:id>')
def delete_birthday(id):
    birthday = Birthday.query.get_or_404(id)
    if birthday.user_id !=session.get('user_id'):
        return "Unauthorized", 403
    db.session.delete(birthday)
    db.session.commit()
    
    return redirect(url_for('dashboard'))


@app.route('/send-today-reminders')
def send_today_reminders():
    today = get_ist_today()

    birthdays_today = Birthday.query.filter(
        db.extract('month', Birthday.date) == today.month,
        db.extract('day', Birthday.date) == today.day
    ).all()

    for birthday in birthdays_today:
        send_admin_email(birthday)

    return "Today's birthday reminders sent!"
