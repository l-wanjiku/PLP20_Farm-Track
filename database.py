import os
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "farmtrack_db"),
        ssl_disabled=os.getenv("DB_SSL_DISABLED", "true").lower() == "true",
    )

def init_db():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS harvests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                crop_name VARCHAR(100) NOT NULL,
                field_name VARCHAR(100) NOT NULL,
                quantity DECIMAL(10, 2) NOT NULL CHECK (quantity > 0),
                unit VARCHAR(20) NOT NULL DEFAULT 'kg',
                harvest_date DATE NOT NULL,
                notes TEXT
            );
            """
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def add_harvest(crop_name, field_name, quantity, harvest_date, unit="kg", notes=""):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO harvests (crop_name, field_name, quantity, unit, harvest_date, notes)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (crop_name, field_name, quantity, unit, harvest_date, notes),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()


def get_all_harvests():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, crop_name, field_name, quantity, unit, harvest_date, notes
            FROM harvests
            ORDER BY harvest_date DESC, id DESC;
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
def create_sales_table():
    '''Create the sales table if it does not exist yet (safe to run many times).'''
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS sales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                crop_name VARCHAR(100) NOT NULL,
                quantity DECIMAL(10, 2) NOT NULL CHECK (quantity > 0),
                price_per_kg DECIMAL(10, 2) NOT NULL CHECK (price_per_kg > 0),
                total_amount DECIMAL(12, 2) NOT NULL,
                sale_date DATE NOT NULL
            );
            '''
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()