from database import get_db

def create_loan(data):
    P = data['loan_amount']
    N = data['loan_period']
    R = data['rate_of_interest']
    customer_id = data['customer_id']

    I = P * N * R
    A = P + I
    EMI = A / (N * 12)

    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO loans (customer_id, principal, interest, total, emi, period_years, rate, emIs_left)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (customer_id, P, I, A, EMI, N, R, N * 12))
    conn.commit()
    loan_id = cur.lastrowid
    conn.close()

    return {
        'loan_id': loan_id,
        'total_amount': A,
        'interest': I,
        'monthly_emi': EMI
    }

def make_payment(data):
    loan_id = data['loan_id']
    payment_type = data['payment_type']
    amount = data['payment_amount']
    date = data['date']

    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT emi, emIs_left FROM loans WHERE loan_id = ?', (loan_id,))
    row = cur.fetchone()

    if not row:
        return {'error': 'Loan not found'}

    emi, emIs_left = row

    if payment_type.lower() == 'emi':
        emIs_left = max(emIs_left - 1, 0)
    else:
        # lump sum could potentially reduce more EMIs based on amount
        reduction = int(amount // emi)
        emIs_left = max(emIs_left - reduction, 0)

    cur.execute('UPDATE loans SET emIs_left = ? WHERE loan_id = ?', (emIs_left, loan_id))
    cur.execute('INSERT INTO payments (loan_id, amount, payment_type, date) VALUES (?, ?, ?, ?)',
                (loan_id, amount, payment_type, date))
    conn.commit()
    conn.close()

    return {'message': 'Payment recorded', 'remaining_emis': emIs_left}

def get_ledger(loan_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM payments WHERE loan_id = ?', (loan_id,))
    transactions = cur.fetchall()

    cur.execute('SELECT emi, emIs_left FROM loans WHERE loan_id = ?', (loan_id,))
    loan_data = cur.fetchone()
    conn.close()

    return {
        'transactions': transactions,
        'emi': loan_data[0],
        'remaining_emis': loan_data[1]
    }

def get_account_overview(customer_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM loans WHERE customer_id = ?', (customer_id,))
    loans = cur.fetchall()

    overview = []
    for loan in loans:
        loan_id, _, P, I, A, EMI, N, R, emIs_left = loan
        cur.execute('SELECT SUM(amount) FROM payments WHERE loan_id = ?', (loan_id,))
        amount_paid = cur.fetchone()[0] or 0

        overview.append({
            'loan_id': loan_id,
            'principal': P,
            'interest': I,
            'total': A,
            'emi': EMI,
            'paid': amount_paid,
            'remaining_emis': emIs_left
        })

    conn.close()
    return overview
