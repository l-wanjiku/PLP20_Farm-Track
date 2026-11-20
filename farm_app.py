from datetime import datetime
import database


def prompt_positive_float(label):
    while True:
        raw = input(f"{label}: ").strip()
        try:
            value = float(raw)
            if value <= 0:
                print("Please enter a number greater than 0.")
                continue
            return value
        except ValueError:
            print("Invalid number. Please try again.")


def prompt_date(label="Harvest date (YYYY-MM-DD)"):
    while True:
        raw = input(f"{label}: ").strip()
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD (e.g., 2026-11-20).")

def handle_add_harvest():
    crop_name = input("Crop name: ").strip()
    field_name = input("Field name: ").strip()
    quantity = prompt_positive_float("Quantity")
    unit = input("Unit [kg]: ").strip() or "kg"
    harvest_date = prompt_date()
    notes = input("Notes (optional): ").strip()

    if not crop_name or not field_name:
        print("Crop name and field name are required.")
        return

    record_id = database.add_harvest(
        crop_name=crop_name,
        field_name=field_name,
        quantity=quantity,
        harvest_date=harvest_date,
        unit=unit,
        notes=notes,
    )
    print(f"Harvest recorded successfully (ID: {record_id}).")


def handle_view_harvests():
    rows = database.get_all_harvests()
    if not rows:
        print("No harvest records found.")
        return

    print("\n--- All Harvests ---")
    for row in rows:
        notes_part = f" | Notes: {row['notes']}" if row.get("notes") else ""
        print(
            f"[{row['id']}] {row['harvest_date']} | {row['crop_name']} "
            f"({row['field_name']}): {row['quantity']} {row['unit']}{notes_part}"
        )
