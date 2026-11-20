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

# ---------- REPORTS (Sonia, branch logic-reports) ----------
def get_crop_inventory():
    """Option 8: return a list of (crop_name, harvested, sold, lost, stock)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT crop_name FROM harvests")
        crops = [row[0] for row in cursor.fetchall()]

        inventory = []
        for crop in crops:
            cursor.execute(
                "SELECT COALESCE(SUM(quantity), 0) FROM harvests WHERE crop_name = %s", (crop,)
            )
            harvested = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COALESCE(SUM(quantity), 0) FROM sales WHERE crop_name = %s", (crop,)
            )
            sold = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COALESCE(SUM(quantity), 0) FROM losses WHERE crop_name = %s", (crop,)
            )
            lost = cursor.fetchone()[0]

            inventory.append((crop, harvested, sold, lost, harvested - sold - lost))

        return inventory
    finally:
        cursor.close()
        conn.close()


def get_financial_summary():
    """Option 9: return (total_revenue, total_expenses, net_profit)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT COALESCE(SUM(quantity * price_per_kg), 0) FROM sales")
        revenue = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
        expenses = cursor.fetchone()[0]

        return revenue, expenses, revenue - expenses
    finally:
        cursor.close()
        conn.close()


def get_transaction_history():
    """Option 10: return (date, type, details) for all records, newest first."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT tx_date, tx_type, details FROM (
                SELECT harvest_date AS tx_date, 'HARVEST' AS tx_type,
                       CONCAT(crop_name, ' - ', quantity, ' kg') AS details
                FROM harvests
                UNION ALL
                SELECT sale_date, 'SALE',
                       CONCAT(crop_name, ' - ', quantity, ' kg at ', price_per_kg, ' RWF/kg')
                FROM sales
                UNION ALL
                SELECT loss_date, 'LOSS',
                       CONCAT(crop_name, ' - ', quantity, ' kg (', COALESCE(reason, 'no reason'), ')')
                FROM losses
                UNION ALL
                SELECT expense_date, 'EXPENSE',
                       CONCAT(description, ' - ', amount, ' RWF')
                FROM expenses
            ) AS all_transactions
            ORDER BY tx_date DESC
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
