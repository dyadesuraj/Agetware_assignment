from flask import Flask, request, jsonify
from database import init_db, get_db
from models import create_loan, make_payment, get_ledger, get_account_overview

app = Flask(__name__)
init_db()

@app.route('/lend', methods=['POST'])
def lend():
    data = request.get_json()
    loan_details = create_loan(data)
    return jsonify(loan_details), 201

@app.route('/payment', methods=['POST'])
def payment():
    data = request.get_json()
    result = make_payment(data)
    return jsonify(result)

@app.route('/ledger/<int:loan_id>', methods=['GET'])
def ledger(loan_id):
    result = get_ledger(loan_id)
    return jsonify(result)

@app.route('/overview/<int:customer_id>', methods=['GET'])
def overview(customer_id):
    result = get_account_overview(customer_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
