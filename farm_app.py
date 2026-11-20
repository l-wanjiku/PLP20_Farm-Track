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
