import sqlite3
from datetime import datetime

class DatabaseHandler:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                title TEXT,
                price REAL,
                rating REAL,
                platform TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                product_id INTEGER,
                review_text TEXT,
                sentiment_label TEXT,
                sentiment_score REAL,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        self.conn.commit()

    def insert_product(self, product_data):
        self.cursor.execute('''
            INSERT INTO products (title, price, rating, platform, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (product_data['title'], product_data['price'], product_data['rating'], product_data['platform'], datetime.now()))
        product_id = self.cursor.lastrowid
        self.conn.commit()
        return product_id

    def insert_reviews(self, product_id, reviews, sentiments):
        for review, sentiment in zip(reviews, sentiments):
            self.cursor.execute('''
                INSERT INTO reviews (product_id, review_text, sentiment_label, sentiment_score)
                VALUES (?, ?, ?, ?)
            ''', (product_id, review, sentiment['label'], sentiment['score']))
        self.conn.commit()

    def get_product_history(self, product_id):
        self.cursor.execute('''
            SELECT price, platform, timestamp
            FROM products
            WHERE id = ?
            ORDER BY timestamp
        ''', (product_id,))
        return self.cursor.fetchall()

    def get_all_products(self):
        self.cursor.execute('''
            SELECT id, title, price, rating, platform, timestamp
            FROM products
            ORDER BY timestamp DESC
        ''')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
