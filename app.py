from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.user import User
from dao.user_dao import UserDAO
from dao.medicine_dao import MedicineDAO
from dao.customer_dao import CustomerDAO
from dao.prescription_dao import PrescriptionDAO
from dao.bill_dao import BillDAO
import pandas as pd
from datetime import datetime, timedelta
import os
from sqlalchemy import or_

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize DAOs
user_dao = UserDAO()
medicine_dao = MedicineDAO()
customer_dao = CustomerDAO()
prescription_dao = PrescriptionDAO()
bill_dao = BillDAO()

@login_manager.user_loader
def load_user(user_id):
    return user_dao.get_user_by_id(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = user_dao.get_user_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Medicine routes
@app.route('/medicines')
@login_required
def medicines():
    medicines_list = medicine_dao.get_all_medicines()
    return render_template('medicines/index.html', medicines=medicines_list)

@app.route('/medicines/add', methods=['GET', 'POST'])
@login_required
def add_medicine():
    if request.method == 'POST':
        # Handle medicine addition
        medicine = Medicine(
            id=0,
            name=request.form['name'],
            batch_number=request.form['batch_number'],
            expiry_date=datetime.strptime(request.form['expiry_date'], '%Y-%m-%d'),
            quantity=int(request.form['quantity']),
            price=float(request.form['price']),
            manufacturer=request.form['manufacturer']
        )
        if medicine_dao.add_medicine(medicine):
            flash('Medicine added successfully')
            return redirect(url_for('medicines'))
        flash('Error adding medicine')
    return render_template('medicines/add.html')

# Customer routes
@app.route('/customers')
@login_required
def customers():
    search = request.args.get('search', '')
    if search:
        customers = customer_dao.search_customers(search)
    else:
        customers = customer_dao.get_all_customers()
    return render_template('customers/index.html', customers=customers)

# Prescription routes
@app.route('/prescriptions')
@login_required
def prescriptions():
    customer = request.args.get('customer', '')
    doctor = request.args.get('doctor', '')
    date_str = request.args.get('date', '')
    
    filters = {}
    if customer:
        filters['customer_name'] = customer
    if doctor:
        filters['doctor_name'] = doctor
    if date_str:
        filters['prescription_date'] = datetime.strptime(date_str, '%Y-%m-%d')
    
    prescriptions = prescription_dao.search_prescriptions(filters)
    return render_template('prescriptions/index.html', prescriptions=prescriptions)

# Billing routes
@app.route('/bills')
@login_required
def bills():
    customer = request.args.get('customer', '')
    date_str = request.args.get('date', '')
    min_amount = request.args.get('min_amount', type=float)
    max_amount = request.args.get('max_amount', type=float)
    
    filters = {}
    if customer:
        filters['customer_name'] = customer
    if date_str:
        filters['bill_date'] = datetime.strptime(date_str, '%Y-%m-%d')
    if min_amount is not None:
        filters['min_amount'] = min_amount
    if max_amount is not None:
        filters['max_amount'] = max_amount
    
    bills = bill_dao.search_bills(filters)
    return render_template('bills/index.html', bills=bills)

# Report routes
@app.route('/reports')
@login_required
def reports():
    return render_template('reports/index.html')

@app.route('/reports/low-stock')
@login_required
def low_stock_report():
    threshold = request.args.get('threshold', 10, type=int)
    medicines = medicine_dao.get_low_stock_medicines(threshold)
    
    if request.args.get('export') == 'excel':
        df = pd.DataFrame([{
            'Name': m.name,
            'Batch': m.batch_number,
            'Quantity': m.quantity,
            'Manufacturer': m.manufacturer
        } for m in medicines])
        
        filename = f'low_stock_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        df.to_excel(f'static/reports/{filename}', index=False)
        return redirect(url_for('static', filename=f'reports/{filename}'))
    
    return render_template('reports/low_stock.html', medicines=medicines)

if __name__ == '__main__':
    app.run(debug=True) 