import os, csv
import datetime

def create_file():
    print("\n----- CREATE FILE -----")
    csv_create_file_input = input("Create a name file: ")
    csv_create_file = f"{csv_create_file_input}.csv"

    if not os.path.exists(csv_create_file):
        with open(csv_create_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Description", "Amount"])
        print("\nList has been created successfully.")
        print("You must quit the program to access the newly created list.")
    else:
        print("\nFile already exists.")

def open_file():
    print("\n----- OPEN FILE -----")
    csv_existing_file_input = input("Name of Expenses File: ")
    csv_existing_file = f"{csv_existing_file_input}.csv"
    expenses = []

    if os.path.exists(csv_existing_file):
        with open(csv_existing_file, "r") as file:
                rows = csv.DictReader(file)
                for row in rows:
                    expenses.append(row)
        print("\nFile has been successfully opened.")
        return expenses, csv_existing_file
    else:
        print("\nList does not exist.")
        return None, None

def delete_file():
    print("\n----- DELETE FILE -----")
    csv_delete_file_input = input("Name of file to delete: ")
    csv_delete_file = f"{csv_delete_file_input}.csv"

    if os.path.exists(csv_delete_file):
        os.remove(csv_delete_file)
        print("\nList deleted.")
    else:
        print("\nList does not exist.")

def read_expenses(csv_existing_file):
    expenses = []

    if os.path.exists(csv_existing_file):
        with open(csv_existing_file, "r") as file:
            rows = csv.DictReader(file)
            for row in rows:
                expenses.append(row)
    return expenses

def add_expenses(csv_existing_file):
    print("\n----- ADD EXPENSE -----")
    description = input("Enter Description: ")
    try:
        amount = float(input("Enter Amount: "))
    except ValueError:
        print("\nInvalid amount. Please enter a number.")
        return

    date = datetime.datetime.today().strftime("%m/%d/%y")
    expenses = read_expenses(csv_existing_file)

    if expenses:
        id = int(expenses[-1]["ID"])
    else:
        id = 0

    current_id = id + 1

    with open(csv_existing_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([current_id, date, description, f"{amount:.2f}"])
    print("\nExpense successfully added.")

def update_expenses(csv_existing_file):
    expenses = read_expenses(csv_existing_file)
    if not expenses:
        print("\nNo expenses to update.")
        return

    view_list_expenses(csv_existing_file)

    current_id = input("\nInput ID to update: ")
    found_id = False

    for row in expenses:
        if row["ID"] == current_id:
            found_id = True
            print("\n----- UPDATE EXPENSE -----")
            print("1. Description")
            print("2. Amount")
            print("3. Both")
            print("4. Exit")

            pick_update = input("Input an action (1-4): ")
            if pick_update == "1":
                print(f"\nCurrent Description: {row['Description']}")
                updated_description = input("Updated Description: ")
                if updated_description:
                    row["Description"] = updated_description

            elif pick_update == "2":
                print(f"\nCurrent Amount: {row['Amount']}")
                updated_amount = input("Updated Amount: ")
                if updated_amount:
                    try:
                        row["Amount"] = f"{float(updated_amount):.2f}"
                    except ValueError:
                        print("Invalid amount. The original amount will be kept.")
                        break

            elif pick_update == "3":
                print(f"\nCurrent Description: {row['Description']}")
                updated_description = input("Updated Description: ")
                if updated_description:
                    row["Description"] = updated_description

                print(f"\nCurrent Amount: {row['Amount']}")
                updated_amount = input("Updated Amount: ")
                if updated_amount:
                    try:
                        row["Amount"] = f"{float(updated_amount):.2f}"
                    except ValueError:
                        print("\nInvalid amount. The original amount will be kept.")
                        break

            elif pick_update == "4":
                get_action(csv_existing_file)
            else:
                print("\nInvalid action. Please try again.")

            break

    if not found_id:
        print("\nNo ID was found. Please try again.")
        return

    with open(csv_existing_file, "w", newline="") as file:
        headers = ["ID", "Date", "Description", "Amount"]
        writer = csv.DictWriter(file, fieldnames = headers)
        writer.writeheader()
        writer.writerows(expenses)

    print("\nExpense Updated.")

def view_list_expenses(csv_existing_file):
    expenses = read_expenses(csv_existing_file)
    if not expenses:
        print("\nNo expenses to show.")
        return

    print("\n--------------- EXPENSE TRACKER LIST ---------------")
    print(f"{'#':<3} {'ID':<3} {'Date':<12} {'Description':<20} {'Amount':<10}")
    print("-" * 50)

    for row in expenses:
        print(f"{'#':<3} {row['ID']:<3} {row['Date']:<12} {row['Description']:<20} P{row['Amount']:<10}")

def view_total_monthly_expenses(input_month, csv_existing_file):
    expenses = read_expenses(csv_existing_file)
    if not expenses:
        return

    total = 0

    for row in expenses:
        try:
            month = datetime.datetime.strptime(row["Date"], "%m/%d/%y")
            if month.strftime("%B").lower() == input_month.lower():
                amount = float(row["Amount"])
                total += amount
        except:
            continue

    print(f"\n----- SUMMARY OF TOTAL EXPENSES IN {input_month.upper()} -----")
    print(f"Total {input_month.capitalize()} Expenses: {total:.2f}")

def view_total_yearly_expenses(input_year, csv_existing_file):
    expenses = read_expenses(csv_existing_file)
    if not expenses:
        return

    total = 0

    try:
        input_year = int(input_year)
    except ValueError:
        print("\nInvalid year input.")
        return

    for row in expenses:
        try:
            year = datetime.datetime.strptime(row["Date"], "%m/%d/%y")
            if year.year == input_year:
                amount = float(row["Amount"])
                total += amount
        except:
            continue

    print(f"\n----- SUMMARY OF TOTAL EXPENSES IN {input_year} -----")
    print(f"Total {input_year} Expenses: {total:.2f}")

def view_total_expenses(csv_existing_file):
    expenses = read_expenses(csv_existing_file)
    if not expenses:
        return

    total = 0

    for row in expenses:
        amount = float(row["Amount"])
        total += amount

    print("\n----- SUMMARY OF TOTAL EXPENSES -----")
    print(f"Total Expenses: P{total:.2f}")

def get_action(csv_existing_file):
    while True:
        # ACTION MENU OF THE PROGRAM
        # This will let the user to:
        # 1. Add expenses - add a description and amount of the expense.
        # 2. Update expenses - edit a description and amount of the expense via ID.
        # 3. View expenses - they can view the expenses by category:
            # 1. List - shows the list of the current expenses.
            # 2. Summary - they can view then again the expenses by category:
                # 1. Month - they can type a month and it will show all expenses in that month.
                # 2. Year - they can type a year and it will show all the expenses in that year.
                # 3. Total - this will show all the expenses made via the program.
        print("\n----- EXPENSE TRACKER -----")
        print("1. Add Expenses")
        print("2. Update Expenses")
        print("3. View Expenses")
        print("4. Exit")

        choice_action = input("Input an action (1-4): ")
        if choice_action == "1":
            add_expenses(csv_existing_file)
        elif choice_action == "2":
            update_expenses(csv_existing_file)
        elif choice_action == "3":
            print("\n----- VIEW EXPENSES -----")
            print("1. List")
            print("2. Summary")
            choice_view_expenses = input("Input an action (1-2): ")
            if choice_view_expenses == "1":
                view_list_expenses(csv_existing_file)
            elif choice_view_expenses == "2":
                print("\n----- SUMMARY -----")
                print("1. Month")
                print("2. Year")
                print("3. Total")
                choice_summary = input("Input an action (1-3): ")
                if choice_summary == "1":
                    input_month = input("Month: ").lower()
                    view_total_monthly_expenses(input_month, csv_existing_file)
                elif choice_summary == "2":
                    input_year = input("Year: ")
                    view_total_yearly_expenses(input_year, csv_existing_file)
                elif choice_summary == "3":
                    view_total_expenses(csv_existing_file)

        elif choice_action == "4":
            main()
        else:
            print("\nInvalid Action")

def main():
    print("----- WELCOME TO EXPENSE TRACKER -----")

    while True:
        # MAIN MENU OF THE PROGRAM
        # This will allow the user to:
        # 1. Create a new list - creating a new csv file to store their expenses.
        # 2. Open existing list - opening an already existing csv file to update or view their expenses.
        # 3. Delete existing list - deleting an already existing csv file.
        print("\n----- EXPENSE TRACKER MEN  U -----")
        print("1. Create New List")
        print("2. Open Existing List")
        print("3. Delete Existing List")
        print("4. Exit")

        choice_start = input("Input an action (1-4): ")
        if choice_start == "1":
            create_file()
        elif choice_start == "2":
            expenses, csv_existing_file = open_file()
            if csv_existing_file:
                get_action(csv_existing_file)
        elif choice_start == "3":
            delete_file()
        elif choice_start == "4":
            print("\nThank you for using the Expense Tracker!")
            break
        else:
            print("\nInvalid Action. Please try again.")

if __name__ == "__main__":
    main()