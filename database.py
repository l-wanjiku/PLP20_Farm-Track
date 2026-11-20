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
