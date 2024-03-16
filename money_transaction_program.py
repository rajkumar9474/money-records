import os
import json
import datetime
import getpass

def register():
    print("=== Registration ===")
    name = input("Enter your name: ")
    phone_number = input("Enter your phone number: ")

    # Generate a random pin and password
    pin = getpass.getpass("Enter your PIN: ")
    password = getpass.getpass("Enter your password: ")

    # Save user details to a new file
    user_data = {"name": name, "phone_number": phone_number, "pin": pin, "password": password}
    user_data_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "money record", r"C:\Users\APURBA\OneDrive\Desktop\money record\user_data_{}.json".format(name))

    with open(user_data_file_path, "w") as file:
        json.dump(user_data, file)

    # Create an empty transaction file for the user
    transaction_data_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "records", r"C:\Users\APURBA\OneDrive\Desktop\money record\{}_transactions.json".format(name))
    with open(transaction_data_file_path, "w") as file:
        pass

    print("Registration successful.!!")
    return name, pin


def login():
    print("=== Login ===")
    name = input("Enter your name: ")
    password = input("Enter your password: ")

    # Check if user exists and Password is correct
    user_data_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "money record", r"C:\Users\APURBA\OneDrive\Desktop\money record\user_data_{}.json".format(name))
    
    try:
        with open(user_data_file_path, "r") as file:
            user_data = json.load(file)
            if user_data["name"] == name and user_data["password"] == password:
                print("Login successful.")
                return name
            else:
                print("Invalid credentials.")
                return None
    except FileNotFoundError:
        print("User not found.")
        return None


def write_transaction(amount, action, product_name="", bill_softcopy_path=""):
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    transaction_data = {
        "amount": amount,
        "action": action,
        "product_name": product_name,
        "bill_softcopy_path": bill_softcopy_path,
        "date_time": date_time
    }

    folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "records")
    os.makedirs(folder_path, exist_ok=True)

    with open(os.path.join(folder_path, r"C:\Users\APURBA\OneDrive\Desktop\money record\{}_transactions.json").format(name), "a") as file:
        json.dump(transaction_data, file)
        file.write("\n")

def total_amount():
    transactions = read_transactions()
    total = sum(transaction["amount"] for transaction in transactions)
    print("Total amount:", total)


def withdraw():
    amount = float(input("Enter the amount: "))
    product_name = input("Enter the name of the product: ")
    bill_softcopy_available = input("Is bill softcopy available? (yes/no): ").lower() == "yes"
    bill_softcopy_path = ""

    if bill_softcopy_available:
        bill_softcopy_path = input("Enter the path to the bill softcopy file: ")

    transactions = read_transactions()
    total = sum(transaction["amount"] for transaction in transactions)

    if total < amount:
        print("Error: Insufficient funds for withdrawal.")
    else:
        write_transaction(-amount, "withdraw", product_name, bill_softcopy_path)
        print("Withdrawal successful.")



def credited():
    amount = float(input("Enter the credited amount: "))
    product_name = input("Enter the name of the product: ")
    write_transaction(amount, "credited",product_name)
    print("Amount credited successfully.")

def show_records_by_date():
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    transactions = read_transactions()
    filtered_transactions = [transaction for transaction in transactions if start_date <= transaction["date_time"] <= end_date]

    if not filtered_transactions:
        print("No records found for the specified date range.")
    else:
        print("Records for the specified date range:")
        for transaction in filtered_transactions:
            formatted_path = transaction.get("bill_softcopy_path", "").replace("\\\\", "\\")
            amount = abs(transaction["amount"])
            action = "credited" if transaction["amount"] >= 0 else "withdrawn"
            print(f"{action.capitalize()} Amount: {amount}, Product: {transaction['product_name']}, "
                  f"Bill Softcopy Path: {formatted_path}, Date and Time: {transaction['date_time']}")


def other_settings():
    # Implement other settings as needed (change name, phone number, password, pin)
    pass

def read_transactions():
    try:
        with open((r"C:\Users\APURBA\OneDrive\Desktop\money record\{}_transactions.json").format(name), "r") as file:
            transactions = [json.loads(line) for line in file]
        return transactions
    except FileNotFoundError:
        return []

if __name__ == "__main__":
    name = None
    while not name:
        choice = input("Do you want to register (1) or login (2)? ")
        if choice == "1":
            name, pin = register()
        elif choice == "2":
            name = login()

    while True:
        print("\nOptions:")
        print("1 --> Total amount")
        print("2 --> Withdraw")
        print("3 --> Credited")
        print("4 --> Show records by date")
        print("5 --> Other settings")
        print("0 --> Exit")

        option = input("Enter your choice: ")

        if option == "1":
            total_amount()
        elif option == "2":
            withdraw()
        elif option == "3":
            credited()
        elif option == "4":
            show_records_by_date()
        elif option == "5":
            other_settings()
        elif option == "0":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
