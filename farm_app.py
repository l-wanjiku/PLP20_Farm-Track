
def record_expense_flow(db_path: str = "farmtrack.db", is_input_purchase: bool = False) -> None:
    """Ask the farmer for input purchase or expense details (Options 2 & 7) and save them."""
    pass


def record_loss_flow(db_path: str = "farmtrack.db") -> None:
    """Ask the farmer for produce loss details (Option 6) and save them."""
    pass

from datetime import datetime
import sqlite3


def record_expense_flow(db_path: str = "farmtrack.db", is_input_purchase: bool = False) -> None:
    """Ask the farmer for input purchase or expense details (Options 2 & 7) and save them."""
    title = "Record Farm Input Purchase" if is_input_purchase else "Record Farm Expense"
    print(f"\n--- {title} ---")
    try:
        if is_input_purchase:
            item = input("Input item (e.g., seeds, fertilizer): ").strip()
            qty = float(input("Quantity: ").strip())
            unit = input("Unit (e.g., kg, bags): ").strip()
            amount = float(input("Total cost in RWF: ").strip())
            date_str = input("Date (YYYY-MM-DD): ").strip()
            description = f"{qty:g} {unit} {item}"
        else:
            description = input("Expense description: ").strip()
            amount = float(input("Amount in RWF: ").strip())
            date_str = input("Date (YYYY-MM-DD): ").strip()

        add_expense(description, amount, date_str, db_path=db_path)
        print("Saved! Returning to menu.")
    except ValueError:
        print("Please enter valid numbers for amounts/quantities.")
    except sqlite3.Error as err:
        print(f"Could not save to database: {err}")


def record_loss_flow(db_path: str = "farmtrack.db") -> None:
    """Ask the farmer for produce loss details (Option 6) and save them."""
    print("\n--- Record Produce Loss ---")
    try:
        crop = input("Crop name: ").strip()
        qty_lost = float(input("Quantity lost (kg): ").strip())
        reason = input("Reason for loss: ").strip()
        date_str = input("Date (YYYY-MM-DD): ").strip()

        add_loss(crop, qty_lost, reason, date_str, db_path=db_path)
        print("Loss recorded! Returning to menu.")
    except ValueError:
        print("Please enter a valid number for the weight lost.")
    except sqlite3.Error as err:
        print(f"Could not save to database: {err}")
