# SOLVY - ISO20022 to Ethereum Translator
# A project by S.A. Nathan LLC

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from models import db, User, Transaction, DebitCard
from iso20022_parser import parse_iso20022
from config import Config
import os
from flask_migrate import Migrate
from decidey import process_transaction
from man import process_ach_transaction
import logging
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# SOLVY: User Interface Routes
@app.route('/')
@login_required
def dashboard():
    transactions = Transaction.query.all()
    debit_cards = DebitCard.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', transactions=transactions, debit_cards=debit_cards)

@app.route('/login', methods=['GET', 'POST'])
def login():
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

@app.route('/transaction/<int:id>')
@login_required
def transaction_details(id):
    transaction = Transaction.query.get_or_404(id)
    return render_template('transaction_details.html', transaction=transaction)

# New route for debit card registration
@app.route('/register_debit_card', methods=['GET', 'POST'])
@login_required
def register_debit_card():
    if request.method == 'POST':
        new_card = DebitCard(
            user_id=current_user.id,
            card_number=request.form['card_number'],
            expiration_date=datetime.strptime(request.form['expiration_date'], '%Y-%m').date(),
            cvv=request.form['cvv'],
            cardholder_name=request.form['cardholder_name'],
            billing_address=request.form['billing_address']
        )
        db.session.add(new_card)
        db.session.commit()
        flash('Debit card registered successfully')
        return redirect(url_for('dashboard'))
    return render_template('register_debit_card.html')

# New route for debit card management
@app.route('/manage_debit_cards')
@login_required
def manage_debit_cards():
    debit_cards = DebitCard.query.filter_by(user_id=current_user.id).all()
    return render_template('manage_debit_cards.html', debit_cards=debit_cards)

# API Route (SOLVY to DECIDEY/MAN)
@app.route('/api/transaction', methods=['POST'])
def receive_transaction():
    iso20022_data = request.json.get('iso20022_data')
    bank_name = request.json.get('bank_name', 'example_bank')
    ach_name = request.json.get('ach_name', 'example_ach')

    if not iso20022_data:
        return jsonify({'error': 'No ISO20022 data provided'}), 400

    try:
        parsed_data = parse_iso20022(iso20022_data)
    except ValueError as e:
        logger.error(f"Error parsing ISO20022 data: {str(e)}")
        return jsonify({'error': str(e)}), 400

    # DECIDEY: Process transaction and store on blockchain
    try:
        decidey_result = process_transaction(parsed_data, bank_name)
    except Exception as e:
        logger.error(f"Error processing transaction with DECIDEY: {str(e)}")
        return jsonify({'error': f"Error processing transaction: {str(e)}"}), 500

    # MAN: Process ACH transaction if applicable
    man_result = {}
    if parsed_data['message_type'] in ['credit_transfer', 'direct_debit']:
        try:
            man_result = process_ach_transaction(parsed_data, ach_name)
        except Exception as e:
            logger.error(f"Error processing ACH transaction with MAN: {str(e)}")
            return jsonify({'error': f"Error processing ACH transaction: {str(e)}"}), 500

    # Store transaction in database
    new_transaction = Transaction(
        message_type=parsed_data['message_type'],
        transaction_id=parsed_data['transaction_id'],
        status=parsed_data.get('status'),
        reason=parsed_data.get('reason'),
        amount=parsed_data['amount'],
        currency=parsed_data['currency'],
        debtor_name=parsed_data.get('debtor_name'),
        debtor_account=parsed_data.get('debtor_account'),
        creditor_name=parsed_data.get('creditor_name'),
        creditor_account=parsed_data.get('creditor_account'),
        remittance_info=parsed_data.get('remittance_info'),
        mandate_id=parsed_data.get('mandate_id'),
        iso20022_data=iso20022_data,
        ethereum_data=str(decidey_result.get('ethereum_data')),
        transaction_hash=decidey_result.get('transaction_hash'),
        original_message_id=parsed_data.get('original_message_id'),
        original_message_type=parsed_data.get('original_message_type'),
        group_status=parsed_data.get('group_status'),
        requested_execution_date=parsed_data.get('requested_execution_date'),
        requested_collection_date=parsed_data.get('requested_collection_date'),
        return_reason=parsed_data.get('return_reason'),
        case_id=parsed_data.get('case_id'),
        creator=parsed_data.get('creator'),
        account_id=parsed_data.get('account_id'),
        statement_id=parsed_data.get('statement_id'),
        creation_date_time=parsed_data.get('creation_date_time'),
        balance=parsed_data.get('balance'),
        bank_response=str(decidey_result.get('bank_response')),
        ach_response=str(man_result.get('ach_response')) if man_result else None
    )
    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({
        'success': True,
        'transaction_hash': decidey_result.get('transaction_hash'),
        'bank_response': decidey_result.get('bank_response'),
        'ach_response': man_result.get('ach_response')
    }), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
