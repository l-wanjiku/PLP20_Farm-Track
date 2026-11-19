
def add_expense(description: str, amount_rwf: float, expense_date: str, db_path: str = "farmtrack.db") -> int:
    """Save a farm input purchase or expense in the expenses table and return its ID."""
    pass


def add_loss(crop_name: str, quantity_kg: float, reason: str, loss_date: str, db_path: str = "farmtrack.db") -> int:
    """Save a crop loss entry in the losses table and return its ID."""
    pass

import sqlite3


def add_expense(description: str, amount_rwf: float, expense_date: str, db_path: str = "farmtrack.db") -> int:
    """Save a farm input purchase or expense in the expenses table and return its ID."""
    conn = sqlite3.connect(db_path)
    try:
        with conn:
            cur = conn.execute(
                "INSERT INTO expenses (description, amount_rwf, expense_date) VALUES (?, ?, ?)",
                (description, amount_rwf, expense_date),
            )
            return int(cur.lastrowid)
    finally:
        conn.close()


def add_loss(crop_name: str, quantity_kg: float, reason: str, loss_date: str, db_path: str = "farmtrack.db") -> int:
    """Save a crop loss entry in the losses table and return its ID."""
    conn = sqlite3.connect(db_path)
    try:
        with conn:
            cur = conn.execute(
                "INSERT INTO losses (crop_name, quantity_kg, reason, loss_date) VALUES (?, ?, ?, ?)",
                (crop_name, quantity_kg, reason, loss_date),
            )
            return int(cur.lastrowid)
    finally:
        conn.close()
