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
