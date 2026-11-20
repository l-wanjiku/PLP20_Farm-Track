
# ---------- REPORTS (Sonia, branch logic-reports) ----------
import mysql.connector
from database import get_crop_inventory, get_financial_summary, get_transaction_history


def view_inventory_flow():
    """Option 8: show the current stock for each crop."""
    print("\n--------------- CURRENT INVENTORY ---------------\n")
    try:
        inventory = get_crop_inventory()
    except mysql.connector.Error as error:
        print(f"Could not read the inventory: {error}")
        return

    if not inventory:
        print("No harvests recorded yet.")
        return

    for crop, harvested, sold, lost, stock in inventory:
        print(f"{crop}: {stock} kg left (harvested {harvested}, sold {sold}, lost {lost})")





def view_financial_summary_flow():
    """Option 9: show revenue, expenses and net profit/loss."""
    print("\n--------------- FARM SUMMARY ---------------\n")
    try:
        revenue, expenses, net = get_financial_summary()
    except mysql.connector.Error as error:
        print(f"Could not read the farm summary: {error}")
        return

    label = "PROFIT" if net >= 0 else "LOSS"
    print(f"Total revenue:  {revenue:,.0f} RWF")
    print(f"Total expenses: {expenses:,.0f} RWF")
    print(f"Net {label}:     {abs(net):,.0f} RWF")

