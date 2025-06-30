import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'crm.db')


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT
            )
            """
        )
        conn.commit()


def query_db(query, args=(), one=False, commit=False):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(query, args)
        if commit:
            conn.commit()
        rv = cur.fetchall()
        cur.close()
    return (rv[0] if rv else None) if one else rv


init_db()


@app.route('/customers', methods=['GET'])
def get_customers():
    rows = query_db('SELECT id, name, email, phone FROM customers')
    customers = [
        {'id': r[0], 'name': r[1], 'email': r[2], 'phone': r[3]}
        for r in rows
    ]
    return jsonify(customers)


@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json or {}
    query_db(
        'INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)',
        (data.get('name'), data.get('email'), data.get('phone')),
        commit=True,
    )
    return jsonify({'status': 'created'}), 201


@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    row = query_db(
        'SELECT id, name, email, phone FROM customers WHERE id = ?',
        (customer_id,),
        one=True,
    )
    if row:
        customer = {'id': row[0], 'name': row[1], 'email': row[2], 'phone': row[3]}
        return jsonify(customer)
    return jsonify({'error': 'not found'}), 404


@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.json or {}
    query_db(
        'UPDATE customers SET name = ?, email = ?, phone = ? WHERE id = ?',
        (data.get('name'), data.get('email'), data.get('phone'), customer_id),
        commit=True,
    )
    return jsonify({'status': 'updated'})


@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    query_db('DELETE FROM customers WHERE id = ?', (customer_id,), commit=True)
    return jsonify({'status': 'deleted'})


if __name__ == '__main__':
    app.run(debug=True)
