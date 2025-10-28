import pymysql
import datetime

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "ganesh",
    "db": "medical_db"
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name TEXT NOT NULL,
            batch_no TEXT NOT NULL,
            expiry_date DATE NOT NULL,
            quantity INT NOT NULL,
            price FLOAT NOT NULL,
            supplier TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_medicine(name, batch_no, expiry_date, quantity, price, supplier):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO medicines (name, batch_no, expiry_date, quantity, price, supplier)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (name, batch_no, expiry_date, quantity, price, supplier))
    conn.commit()
    conn.close()

def view_medicines():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines")
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_medicine(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM medicines
        WHERE name LIKE %s OR batch_no LIKE %s
    ''', ('%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_stock(medicine_id, quantity_change):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE medicines
        SET quantity = quantity + %s
        WHERE id = %s
    ''', (quantity_change, medicine_id))
    conn.commit()
    conn.close()

def check_expiry():
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.date.today()
    cursor.execute('''
        SELECT * FROM medicines
        WHERE expiry_date <= %s
    ''', (today,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def check_low_stock(threshold=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM medicines
        WHERE quantity <= %s
    ''', (threshold,))
    rows = cursor.fetchall()
    conn.close()
    return rows
