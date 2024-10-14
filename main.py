from flask import Flask, Response, stream_with_context, request, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from models import db, Transaction, User
from datetime import datetime, timedelta
import json
import time
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')  # Replace with a real secret key

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/stream')
@login_required
def stream():
    def event_stream():
        while True:
            # Check for new transactions
            new_transactions = Transaction.query.filter(Transaction.timestamp > (datetime.utcnow() - timedelta(seconds=10))).all()
            if new_transactions:
                for transaction in new_transactions:
                    data = {
                        'id': transaction.id,
                        'transaction_hash': transaction.transaction_hash,
                        'timestamp': transaction.timestamp.isoformat(),
                        'amount': str(transaction.amount),
                        'currency': transaction.currency,
                        'status': transaction.status
                    }
                    yield f"data: {json.dumps(data)}\n\n"
            time.sleep(5)  # Check every 5 seconds

    return Response(stream_with_context(event_stream()), content_type='text/event-stream')

@app.route('/')
@login_required
def dashboard():
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).limit(10).all()
    return render_template('dashboard.html', transactions=transactions)

@app.route('/api/alerts', methods=['POST'])
@login_required
def set_alerts():
    data = request.json
    # Here you would typically save the alert settings to the database
    # For simplicity, we'll just return the received data
    return jsonify(data), 200

@app.route('/transaction/<int:id>')
@login_required
def transaction_details(id):
    transaction = Transaction.query.get_or_404(id)
    return render_template('transaction_details.html', transaction=transaction)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
