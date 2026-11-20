
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
        origin/logic-sales

from datetime import datetime
import mysql.connector
from database import (
    add_expense,
    add_loss,
    create_expenses_table,
    create_losses_table,
)


def _expense_ask_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print('Error: this field cannot be empty. Try again.')


def _expense_ask_positive_number(prompt):
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


def _expense_ask_date(prompt):
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return value
        except ValueError:
            print('Error: use this format YYYY-MM-DD (e.g. 2026-11-20).')


def record_expense_flow(is_input_purchase=False):
    '''Asks for input purchase (Option 2) or general expense (Option 7) details and saves.'''
    print()
    if is_input_purchase:
        print('--------- RECORD FARM INPUT PURCHASE ----------')
    else:
        print('--------- RECORD FARM EXPENSE ----------')
    try:
        create_expenses_table()
        if is_input_purchase:
            item = _expense_ask_text('Enter input item (e.g., seeds, fertilizer): ')
            qty = _expense_ask_positive_number('Enter quantity: ')
            unit = _expense_ask_text('Enter unit (e.g., kg, bags): ')
            amount = _expense_ask_positive_number('Enter total cost (RWF): ')
            expense_date = _expense_ask_date('Enter purchase date (YYYY-MM-DD): ')
            description = f'{qty:g} {unit} {item.title()}'
        else:
            description = _expense_ask_text('Enter expense description: ')
            amount = _expense_ask_positive_number('Enter amount (RWF): ')
            expense_date = _expense_ask_date('Enter expense date (YYYY-MM-DD): ')

        expense_id = add_expense(description, amount, expense_date)
        print()
        print('Expense recorded successfully!')
        print(f'Record ID: {expense_id}')
        print(f'Description: {description}')
        print(f'Amount: {amount:,.2f} RWF')
    except ValueError as error:
        print(f'Error: {error}')
    except mysql.connector.Error as error:
        print(f'Database error: {error}')
    finally:
        input('Press Enter to return to the main menu...')


def record_loss_flow():
    '''Asks for produce loss details (Option 6) and saves to the losses table.'''
    print()
    print('--------- RECORD PRODUCE LOSS ----------')
    try:
        create_losses_table()
        crop = _expense_ask_text('Enter crop name: ').title()
        quantity_kg = _expense_ask_positive_number('Enter quantity lost (kg): ')
        reason = _expense_ask_text('Enter reason for loss: ')
        loss_date = _expense_ask_date('Enter loss date (YYYY-MM-DD): ')

        loss_id = add_loss(crop, quantity_kg, reason, loss_date)
        print()
        print('Produce loss recorded successfully!')
        print(f'Record ID: {loss_id}')
        print(f'Crop: {crop}')
        print(f'Quantity lost: {quantity_kg:.2f} kg')
    except ValueError as error:
        print(f'Error: {error}')
    except mysql.connector.Error as error:
        print(f'Database error: {error}')
    finally:
        input('Press Enter to return to the main menu...')


def handle_expense_loss_option(choice):
    '''Routes menu options 2, 6, and 7. Returns True if handled.'''
    pick = choice.strip()
    if pick == '2':
        record_expense_flow(is_input_purchase=True)
        return True
    if pick == '6':
        record_loss_flow()
        return True
    if pick == '7':
        record_expense_flow(is_input_purchase=False)
        return True
    return False
