from mysql.connector import Error as MySQLError


def add_expense(description: str, amount_rwf: float, expense_date: str, conn=None) -> int:
    """Save a farm input purchase or expense in the expenses table and return its ID."""
    owns_conn = conn is None
    if owns_conn:
        conn = get_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO expenses (description, amount_rwf, expense_date) VALUES (%s, %s, %s)",
                (description, amount_rwf, expense_date),
            )
            conn.commit()
            return int(cursor.lastrowid)
        finally:
            cursor.close()
    finally:
        if owns_conn:
            conn.close()


def add_loss(crop_name: str, quantity_kg: float, reason: str, loss_date: str, conn=None) -> int:
    """Save a crop loss entry in the losses table and return its ID."""
    owns_conn = conn is None
    if owns_conn:
        conn = get_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO losses (crop_name, quantity_kg, reason, loss_date) VALUES (%s, %s, %s, %s)",
                (crop_name, quantity_kg, reason, loss_date),
            )
            conn.commit()
            return int(cursor.lastrowid)
        finally:
            cursor.close()
    finally:
        if owns_conn:
            conn.close()
