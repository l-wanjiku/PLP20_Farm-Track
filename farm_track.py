# FarmTrack CLI - Main Menu

import mysql.connector
import database
import farm_app

<<<<<<< HEAD
def show_menu():
    print("\n==============================")
    print("        FARMTRACK CLI ")
    print("===============================")
    print("1. Add a crop")
    print("2. Record a harvest")
    print("3. REcord a sale")
    print("4. Record an expense")
    print("5. Record produce loss")
    print("6. View current inventory"),
    print("7. View financial report")
    print("8. View harvest and sales history")
    print("9. Edit or delete a record")
    print("10. Search transactions by crop")
    print("0. Exit")

def main():
    while True:
        show_menu()

        choice = input("Enter your choice: ")
        if choice =="1":
            farm_app.add_crop()

        elif choice =="2":
            farm_app.record_harvest()

        elif choice == "3":
            farm_app.record_sale()
=======

def show_menu():
    print("\n================================================")
    print("           WELCOME TO FARMTRACK CLI")
    print("    FARM INVENTORY, PRODUCE AND SALES TRACKER")
    print("================================================")
    print("What would you like to do today?")
    print("1. View Recorded Harvests")
    print("2. Record Farm Input Purchase")
    print("4. Record a New Harvest")
    print("5. Record Produce Sale")
    print("6. Record Produce Loss")
    print("7. Record Farm Expense")
    print("8. View Current Inventory")
    print("9. View Farm Summary")
    print("10. View Transaction History")
    print("0. Exit Program")


def main():
    try:
        database.init_db()
    except mysql.connector.Error as err:
        print(f"Database initialization error: {err}")
        print("Please verify MySQL is running and DB_HOST/DB_USER/DB_PASSWORD/DB_NAME are configured.")
        return

    while True:
        show_menu()

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            farm_app.view_harvests_flow()

        elif choice == "2":
            farm_app.record_expense_flow(is_input_purchase=True)
>>>>>>> 86acf5ea74e329b727e5e3decf8f10e0c0dd5bf5

        elif choice == "4":
            farm_app.record_harvest_flow()

        elif choice == "5":
            farm_app.record_sale_flow()

        elif choice == "6":
            farm_app.record_loss_flow()

        elif choice == "7":
            farm_app.record_expense_flow(is_input_purchase=False)

        elif choice == "8":
            farm_app.view_inventory_flow()

        elif choice == "9":
            farm_app.view_financial_summary_flow()

        elif choice == "10":
            farm_app.view_transaction_history_flow()

        elif choice == "0":
            print("Thank you for using FarmTrack. Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")


<<<<<<< HEAD

if __name__ == "__main__":

=======
if __name__ == "__main__":
>>>>>>> 86acf5ea74e329b727e5e3decf8f10e0c0dd5bf5
    main()
