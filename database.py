
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

def _sum_quantity(cursor, table, crop_name):
    ''' add up to the quantity or kg in one table and returns float'''
    cursor.execute(
        f'SELECT COALESCE(SUM(quantity), 0) FROM {table} '
        'WHERE LOWER(crop_name) = LOWER(%s);',
        (crop_name,),
    )
    return float(cursor.fetchone()[0])

def _sum_losses(cursor, crop_name):
    '''Kg lost for a crop. If the losses table does not exist yet, return 0.'''
    try:
        return _sum_quantity(cursor, 'losses', crop_name)
    except mysql.connector.ProgrammingError:
        return 0.0

def crop_has_harvest(crop_name):
    '''it checks if crop was harvested atleast once'''
    conn = get_connection()
    try:
        cursor = conn.cursor()
        return _sum_quantity(cursor, 'harvests', crop_name) > 0
    finally:
        cursor.close()
        conn.close()


def get_available_stock(crop_name):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        harvested = _sum_quantity(cursor, 'harvests', crop_name)
        sold = _sum_quantity(cursor, 'sales', crop_name)
        lost = _sum_losses(cursor, crop_name)
        return harvested - sold - lost
    finally:
        cursor.close()
        conn.close()



def add_sale(crop_name, quantity, price_per_kg, sale_date):
    '''It saves a sale, it also raises valueerror when there is no crop harvest or qty is above stock'''
    conn = get_connection()
    try:
        cursor = conn.cursor()
        harvested = _sum_quantity(cursor, 'harvests', crop_name)
        if harvested == 0:
            raise ValueError(f'No harvest recorded for {crop_name!r}.')
        stock = (harvested
                 - _sum_quantity(cursor, 'sales', crop_name)
                 - _sum_losses(cursor, crop_name))
        if quantity > stock:
            raise ValueError(
                f'Not enough stock. Available: {stock} kg, requested: {quantity} kg.'
            )
        total = round(quantity * price_per_kg, 2)
        cursor.execute(
            '''
            INSERT INTO sales (crop_name, quantity, price_per_kg, total_amount, sale_date)
            VALUES (%s, %s, %s, %s, %s);
            ''',
            (crop_name.strip().title(), quantity, price_per_kg, total, sale_date),
        )
        conn.commit()
        return total
    finally:
        cursor.close()
        conn.close()
        origin/logic-sales


def create_expenses_table():
    """Create the expenses table if it does not exist yet (safe to run many times)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                description VARCHAR(255) NOT NULL,
                amount_rwf DECIMAL(12, 2) NOT NULL CHECK (amount_rwf > 0),
                expense_date DATE NOT NULL
            );
            """
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def create_losses_table():
    """Create the losses table if it does not exist yet (safe to run many times)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS losses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                crop_name VARCHAR(100) NOT NULL,
                quantity_kg DECIMAL(10, 2) NOT NULL CHECK (quantity_kg > 0),
                reason VARCHAR(255) NOT NULL,
                loss_date DATE NOT NULL
            );
            """
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def add_expense(description, amount_rwf, expense_date):
    """Save a farm input purchase or general expense in expenses and return its ID."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO expenses (description, amount_rwf, expense_date)
            VALUES (%s, %s, %s);
            """,
            (description.strip(), amount_rwf, expense_date),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()


def add_loss(crop_name, quantity_kg, reason, loss_date):
    """Save a produce loss entry in losses and return its ID."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO losses (crop_name, quantity_kg, reason, loss_date)
            VALUES (%s, %s, %s, %s);
            """,
            (crop_name.strip().title(), quantity_kg, reason.strip(), loss_date),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()


def _sum_losses(cursor, crop_name):
    """Sum recorded loss quantity (kg) for a crop and return as float."""
    cursor.execute(
        """
        SELECT COALESCE(SUM(quantity_kg), 0)
        FROM losses
        WHERE LOWER(crop_name) = LOWER(%s);
        """,
        (crop_name.strip(),),
    )
    row = cursor.fetchone()
    return float(row[0]) if row and row[0] is not None else 0.0
