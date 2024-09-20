from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from models import db, User, Transaction
from iso20022_parser import parse_iso20022
from ethereum_integration import translate_to_ethereum, store_on_blockchain
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def dashboard():
    transactions = Transaction.query.all()
    return render_template('dashboard.html', transactions=transactions)

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

@app.route('/api/transaction', methods=['POST'])
def receive_transaction():
    iso20022_data = request.json.get('iso20022_data')
    if not iso20022_data:
        return jsonify({'error': 'No ISO20022 data provided'}), 400

    parsed_data = parse_iso20022(iso20022_data)
    ethereum_data = translate_to_ethereum(parsed_data)
    transaction_hash = store_on_blockchain(ethereum_data)

    new_transaction = Transaction(
        iso20022_data=iso20022_data,
        ethereum_data=ethereum_data,
        transaction_hash=transaction_hash
    )
    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({'success': True, 'transaction_hash': transaction_hash}), 201

@app.route('/transaction/<int:id>')
@login_required
def transaction_details(id):
    transaction = Transaction.query.get_or_404(id)
    return render_template('transaction_details.html', transaction=transaction)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
