from flask import Flask, Response, stream_with_context, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_socketio import SocketIO, emit
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User, Business, Client, SolvyCard, Transaction, Alert
import os
import logging
from decimal import Decimal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
socketio = SocketIO(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register_business', methods=['GET', 'POST'])
@login_required
def register_business():
    if request.method == 'POST':
        business_name = request.form.get('business_name')
        business_address = request.form.get('business_address')
        business_phone = request.form.get('business_phone')
        business_email = request.form.get('business_email')

        if not all([business_name, business_address, business_phone, business_email]):
            flash('All fields are required', 'error')
            return render_template('register_business.html')

        existing_business = Business.query.filter_by(business_email=business_email).first()
        if existing_business:
            flash('A business with this email already exists', 'error')
            return render_template('register_business.html')

        new_business = Business(
            owner=current_user,
            business_name=business_name,
            business_address=business_address,
            business_phone=business_phone,
            business_email=business_email
        )

        try:
            db.session.add(new_business)
            db.session.commit()
            flash('Business registered successfully', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error registering business: {str(e)}")
            flash('An error occurred while registering the business', 'error')

    return render_template('register_business.html')

@socketio.on('connect')
def handle_connect():
    logger.info(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('set_alert')
def handle_set_alert(data):
    user_id = current_user.id
    amount_threshold = data.get('amount_threshold')
    currency = data.get('currency')
    
    new_alert = Alert(user_id=user_id, amount_threshold=amount_threshold, currency=currency)
    db.session.add(new_alert)
    db.session.commit()
    
    logger.info(f"Alert set for user {user_id}: {amount_threshold} {currency}")
    
    emit('alert_set', {'status': 'success', 'message': 'Alert set successfully'})

def send_transaction_update(transaction):
    socketio.emit('transaction_update', {
        'id': transaction.id,
        'amount': str(transaction.amount),
        'currency': transaction.currency,
        'status': transaction.status,
        'timestamp': transaction.timestamp.isoformat(),
        'debtor_name': transaction.debtor_name,
        'creditor_name': transaction.creditor_name
    })

def check_alerts(transaction):
    alerts = Alert.query.filter_by(user_id=transaction.user_id, currency=transaction.currency).all()
    for alert in alerts:
        if Decimal(transaction.amount) >= Decimal(alert.amount_threshold):
            socketio.emit('alert_triggered', {
                'message': f'Alert: Transaction amount {transaction.amount} {transaction.currency} exceeds threshold {alert.amount_threshold} {alert.currency}',
                'transaction_id': transaction.id
            }, room=str(transaction.user_id))

@app.route('/api/transaction', methods=['POST'])
@login_required
def process_transaction():
    data = request.json
    new_transaction = Transaction(
        user_id=current_user.id,
        amount=data['amount'],
        currency=data['currency'],
        status=data['status'],
        debtor_name=data['debtor_name'],
        creditor_name=data['creditor_name'],
        transaction_type=data['transaction_type']
    )
    db.session.add(new_transaction)
    db.session.commit()

    send_transaction_update(new_transaction)
    check_alerts(new_transaction)

    return jsonify({'message': 'Transaction processed successfully', 'transaction_id': new_transaction.id}), 201

@app.route('/dashboard')
@login_required
def dashboard():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).limit(10).all()
    return render_template('dashboard.html', transactions=transactions)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
