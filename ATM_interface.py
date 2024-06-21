class Account:
    def __init__(self, account_number, pin, balance=0):
        self.account_number = account_number
        self.pin = pin
        self.balance = balance

    def check_balance(self):
        return self.balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

class ATM:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number, pin, initial_balance=0):
        if account_number not in self.accounts:
            self.accounts[account_number] = Account(account_number, pin, initial_balance)
            return True
        return False

    def authenticate(self, account_number, pin):
        account = self.accounts.get(account_number)
        if account and account.pin == pin:
            return account
        return None

    def run(self):
        while True:
            print("\nWelcome to the ATM")
            print("1. Create Account")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.create_account_flow()
            elif choice == "2":
                self.login_flow()
            elif choice == "3":
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def create_account_flow(self):
        account_number = input("Enter new account number: ")
        pin = input("Enter new PIN: ")
        initial_balance = self.get_float_input("Enter initial deposit amount: ")
        if self.create_account(account_number, pin, initial_balance):
            print("Account created successfully!")
        else:
            print("Account number already exists. Please try again.")

    def login_flow(self):
        account_number = input("Enter account number: ")
        pin = input("Enter PIN: ")
        account = self.authenticate(account_number, pin)
        if account:
            print("Login successful!")
            self.account_menu(account)
        else:
            print("Invalid account number or PIN. Please try again.")

    def account_menu(self, account):
        while True:
            print("\nAccount Menu")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                print(f"Your balance is: ${account.check_balance():.2f}")
            elif choice == "2":
                amount = self.get_float_input("Enter amount to deposit: ")
                if account.deposit(amount):
                    print(f"${amount:.2f} deposited successfully!")
                else:
                    print("Invalid deposit amount. Please try again.")
            elif choice == "3":
                amount = self.get_float_input("Enter amount to withdraw: ")
                if account.withdraw(amount):
                    print(f"${amount:.2f} withdrawn successfully!")
                else:
                    print("Invalid withdrawal amount or insufficient funds. Please try again.")
            elif choice == "4":
                print("Logged out successfully!")
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def get_float_input(prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

if __name__ == "__main__":
    atm = ATM()
    atm.run()
