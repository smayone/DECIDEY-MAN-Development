# Add these imports at the top of the file
from flask import Response, stream_with_context
import json
import time

# Add this new route after the existing routes
@app.route('/stream')
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

# Update the dashboard route to include SSE
@app.route('/')
@login_required
def dashboard():
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).limit(10).all()
    return render_template('dashboard.html', transactions=transactions, custom_icon=current_user.custom_icon)

# Add this new route for alerts
@app.route('/api/alerts', methods=['POST'])
@login_required
def set_alerts():
    data = request.json
    # Here you would typically save the alert settings to the database
    # For simplicity, we'll just return the received data
    return jsonify(data), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, threaded=True)
