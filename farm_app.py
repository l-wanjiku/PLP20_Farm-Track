from datetime import datetime
import mysql.connector
from database import (
    add_sale,
    crop_has_harvest,
    create_sales_table,
    get_available_stock,
)


def _sale_ask_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print('Error: this field cannot be empty. Try again.')


def _sale_ask_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
        except ValueError:
            print('Error: please enter a number (e.g. 25 or 25.5).')
            continue
        if value <= 0:
            print('Error: the number must be greater than 0.')
            continue
        return value