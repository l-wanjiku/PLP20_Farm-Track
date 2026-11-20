from datetime import datetime
from mysql.connector import Error as MySQLError


def _clean_text(value: str, name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{name} cannot be blank.")
    return cleaned


def _clean_positive_amount(raw: str, name: str) -> float:
    amount = float(raw.strip())
    if amount <= 0:
        raise ValueError(f"{name} must be more than 0.")
    return amount


def _clean_date_str(raw: str) -> str:
    cleaned = raw.strip()
    datetime.strptime(cleaned, "%Y-%m-%d")
    return cleaned


def record_expense_flow(is_input_purchase: bool = False, conn=None) -> None:
    """Ask the farmer for input purchase or expense details (Options 2 & 7) and save them."""
    title = "Record Farm Input Purchase" if is_input_purchase else "Record Farm Expense"
    print(f"\n--- {title} ---")
    try:
        if is_input_purchase:
            item = _clean_text(input("Input item (e.g., seeds, fertilizer): "), "Input item")
            qty = _clean_positive_amount(input("Quantity: "), "Quantity")
            unit = _clean_text(input("Unit (e.g., kg, bags): "), "Unit")
            amount = _clean_positive_amount(input("Total cost in RWF: "), "Total cost")
            date_str = _clean_date_str(input("Date (YYYY-MM-DD): "))
            description = f"{qty:g} {unit} {item}"
        else:
            description = _clean_text(input("Expense description: "), "Expense description")
            amount = _clean_positive_amount(input("Amount in RWF: "), "Amount")
            date_str = _clean_date_str(input("Date (YYYY-MM-DD): "))

        add_expense(description, amount, date_str, conn=conn)
        print("Saved! Returning to menu.")
    except ValueError as err:
        print(f"Invalid input: {err}")
    except MySQLError as err:
        print(f"Could not save to MySQL database: {err}")


def record_loss_flow(conn=None) -> None:
    """Ask the farmer for produce loss details (Option 6) and save them."""
    print("\n--- Record Produce Loss ---")
    try:
        crop = _clean_text(input("Crop name: "), "Crop name")
        qty_lost = _clean_positive_amount(input("Quantity lost (kg): "), "Quantity lost")
        reason = _clean_text(input("Reason for loss: "), "Reason")
        date_str = _clean_date_str(input("Date (YYYY-MM-DD): "))

        add_loss(crop, qty_lost, reason, date_str, conn=conn)
        print("Loss recorded! Returning to menu.")
    except ValueError as err:
        print(f"Invalid input: {err}")
    except MySQLError as err:
        print(f"Could not save to MySQL database: {err}")


def handle_expense_loss_option(choice: str, conn=None) -> bool:
    """Handle menu options 2, 6, and 7. Returns True if handled."""
    pick = choice.strip()
    if pick == "2":
        record_expense_flow(is_input_purchase=True, conn=conn)
        return True
    if pick == "6":
        record_loss_flow(conn=conn)
        return True
    if pick == "7":
        record_expense_flow(is_input_purchase=False, conn=conn)
        return True
    return False
