import sqlite3

DB_NAME = 'bank.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            principal REAL,
            interest REAL,
            total REAL,
            emi REAL,
            period_years INTEGER,
            rate REAL,
            emIs_left INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            loan_id INTEGER,
            amount REAL,
            payment_type TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    return sqlite3.connect(DB_NAME)
