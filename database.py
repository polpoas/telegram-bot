# database.py

import sqlite3
from config import DB_NAME

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        price INTEGER NOT NULL
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        amount INTEGER NOT NULL,
                        payment_status TEXT NOT NULL DEFAULT 'pending',
                        FOREIGN KEY (product_id) REFERENCES products(id)
                    )''')
    conn.commit()
    conn.close()

# Инициализация базы данных
init_db()
