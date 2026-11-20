from datetime import datetime
import database


def _prompt_non_empty(prompt_text):
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Error: This field cannot be empty.")


def _prompt_positive_float(prompt_text):
    while True:
        raw = input(prompt_text).strip()
        try:
            value = float(raw)
            if value > 0:
                return value
            print("Error: Quantity must be greater than 0.")
        except ValueError:
            print("Error: Please enter a valid number.")


def _prompt_date(prompt_text):
    while True:
        raw = input(prompt_text).strip()
        if not raw:
            return datetime.today().strftime("%Y-%m-%d")
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("Error: Date must be in YYYY-MM-DD format.")

def record_harvest_flow():
    """Handles CLI input, validation, and saving a harvest record."""
    print("\n--- Record New Harvest ---")
    crop_name = _prompt_non_empty("Crop name (e.g., Maize, Beans): ")
    field_name = _prompt_non_empty("Field/Plot name: ")
    quantity = _prompt_positive_float("Quantity harvested: ")
    unit = input("Unit [default: kg]: ").strip() or "kg"
    harvest_date = _prompt_date("Harvest date (YYYY-MM-DD) [default: today]: ")
    notes = input("Notes (optional): ").strip()

    try:
        harvest_id = database.add_harvest(
            crop_name=crop_name,
            field_name=field_name,
            quantity=quantity,
            harvest_date=harvest_date,
            unit=unit,
            notes=notes,
        )
        print(f"Success: Harvest #{harvest_id} ({quantity} {unit} of {crop_name}) recorded.")
    except Exception as exc:
        print(f"Database error while recording harvest: {exc}")


def view_harvests_flow():
    """Displays all recorded harvests from the database."""
    print("\n--- Harvest Records ---")
    try:
        harvests = database.get_all_harvests()
        if not harvests:
            print("No harvest records found.")
            return

        for row in harvests:
            note_text = f" | Notes: {row['notes']}" if row.get("notes") else ""
            print(
                f"[{row['id']}] {row['harvest_date']} - {row['crop_name']} "
                f"({row['quantity']} {row['unit']}) from {row['field_name']}{note_text}"
            )
    except Exception as exc:
        print(f"Database error while fetching harvests: {exc}")

if __name__ == "__main__":
    database.init_db()
    while True:
        print("\n=== Harvest Module Test ===")
        print("1. Record Harvest")
        print("2. View Harvests")
        print("0. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            record_harvest_flow()
        elif choice == "2":
            view_harvests_flow()
        elif choice == "0":
            break
        else:
            print("Invalid option.")
