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



def _sale_ask_date(prompt):
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return value
        except ValueError:
            print('Error: use this format YYYY-MM-DD (e.g. 2026-11-20).')



def record_sale_flow():
    '''Asks for the sale details, block overselling, save, show the revenue.'''
    print()
    print('--------- RECORD PRODUCE SALE ----------')
    try:
        create_sales_table()
        crop = _sale_ask_text('Enter crop name: ')

        if not crop_has_harvest(crop):
            print(f'Error: no harvest found for {crop!r}. Record a harvest first.')
            return

        stock = get_available_stock(crop)
        print(f'Available stock for {crop}: {stock:.2f} kg')
        if stock <= 0:
            print('Warning: this crop is out of stock. Sale not allowed.')
            return

        quantity = _sale_ask_positive_number('Enter quantity sold (kg): ')
        if quantity > stock:
            print(f'Warning: cannot sell {quantity:.2f} kg. Only {stock:.2f} kg in stock.')
            return

        price = _sale_ask_positive_number('Enter price per kg (RWF): ')
        sale_date = _sale_ask_date('Enter sale date (YYYY-MM-DD): ')

        total = add_sale(crop, quantity, price, sale_date)
        print()
        print('Sale recorded successfully!')
        print(f'Total revenue: {total:,.2f} RWF')
        print(f'Remaining stock: {stock - quantity:.2f} kg')

    except ValueError as error:
        print(f'Error: {error}')
    except mysql.connector.Error as error:
        print(f'Database error: {error}')
    finally:
        input('Press Enter to return to the main menu...')