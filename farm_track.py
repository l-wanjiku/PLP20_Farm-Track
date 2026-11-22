#Farm Track Main Menugit

import farm_app

def show_menu():
    print("\n==============================")
    print("        FARMTRACK CLI ")
    print("===============================")
    print("1. Add a crop")
    print("2. Record a harvest")
    print("3. Record a sale")
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
        elif choice =="4":
            farm_app.record_expense()

        elif choice =="5":
            farm_app.record_loss()

        elif choice =="6":
            farm_app.view_inventory()

        elif choice =="7":
            farm_app.view_financial_report()

        elif choice =="8":
            farm_app.view_history()
            
        elif choice =="9":
            farm_app.edit_or_delete_record()

        elif choice =="10":
            farm_app.Search_transactions_by_crop()

        elif choice == "0":
            print("Thank you for using FarmTrack. Goodbye!")
            break
        
        else:
            print("Invalid choice! Please try again.")


if __name__=="__main__":
    main()

