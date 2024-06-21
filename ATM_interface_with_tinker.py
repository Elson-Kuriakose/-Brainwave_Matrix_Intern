import tkinter as tk
from tkinter import messagebox

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
    def __init__(self, root):
        self.accounts = {}
        self.current_account = None
        self.root = root
        self.root.title("ATM Interface")
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="ATM", font=('Helvetica', 16)).pack(pady=10)
        
        tk.Label(self.root, text="Account Number:").pack(pady=5)
        self.account_number_entry = tk.Entry(self.root)
        self.account_number_entry.pack(pady=5)
        
        tk.Label(self.root, text="PIN:").pack(pady=5)
        self.pin_entry = tk.Entry(self.root, show='*')
        self.pin_entry.pack(pady=5)
        
        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Create Account", command=self.create_account_screen).pack(pady=5)

    def create_account_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Create Account", font=('Helvetica', 16)).pack(pady=10)
        
        tk.Label(self.root, text="Account Number:").pack(pady=5)
        self.new_account_number_entry = tk.Entry(self.root)
        self.new_account_number_entry.pack(pady=5)
        
        tk.Label(self.root, text="PIN:").pack(pady=5)
        self.new_pin_entry = tk.Entry(self.root, show='*')
        self.new_pin_entry.pack(pady=5)
        
        tk.Label(self.root, text="Initial Deposit:").pack(pady=5)
        self.initial_deposit_entry = tk.Entry(self.root)
        self.initial_deposit_entry.pack(pady=5)
        
        tk.Button(self.root, text="Create Account", command=self.create_account).pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.create_login_screen).pack(pady=5)

    def create_account(self):
        account_number = self.new_account_number_entry.get()
        pin = self.new_pin_entry.get()
        initial_deposit = self.get_float_input(self.initial_deposit_entry.get())
        if account_number and pin and initial_deposit is not None:
            if self.create_account_logic(account_number, pin, initial_deposit):
                messagebox.showinfo("Success", "Account created successfully!")
                self.create_login_screen()
            else:
                messagebox.showerror("Error", "Account number already exists.")
        else:
            messagebox.showerror("Error", "Please fill in all fields correctly.")

    def create_account_logic(self, account_number, pin, initial_balance=0):
        if account_number not in self.accounts:
            self.accounts[account_number] = Account(account_number, pin, initial_balance)
            return True
        return False

    def login(self):
        account_number = self.account_number_entry.get()
        pin = self.pin_entry.get()
        account = self.authenticate(account_number, pin)
        if account:
            self.current_account = account
            self.account_menu()
        else:
            messagebox.showerror("Error", "Invalid account number or PIN.")

    def authenticate(self, account_number, pin):
        account = self.accounts.get(account_number)
        if account and account.pin == pin:
            return account
        return None

    def account_menu(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Account Menu", font=('Helvetica', 16)).pack(pady=10)
        
        tk.Button(self.root, text="Check Balance", command=self.check_balance).pack(pady=5)
        tk.Button(self.root, text="Deposit Money", command=self.deposit_screen).pack(pady=5)
        tk.Button(self.root, text="Withdraw Money", command=self.withdraw_screen).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def check_balance(self):
        balance = self.current_account.check_balance()
        messagebox.showinfo("Balance", f"Your balance is: ${balance:.2f}")

    def deposit_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Deposit Money", font=('Helvetica', 16)).pack(pady=10)
        
        tk.Label(self.root, text="Amount to Deposit:").pack(pady=5)
        self.deposit_amount_entry = tk.Entry(self.root)
        self.deposit_amount_entry.pack(pady=5)
        
        tk.Button(self.root, text="Deposit", command=self.deposit).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.account_menu).pack(pady=5)

    def deposit(self):
        amount = self.get_float_input(self.deposit_amount_entry.get())
        if amount is not None:
            if self.current_account.deposit(amount):
                messagebox.showinfo("Success", f"${amount:.2f} deposited successfully!")
                self.account_menu()
            else:
                messagebox.showerror("Error", "Invalid deposit amount.")
        else:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def withdraw_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Withdraw Money", font=('Helvetica', 16)).pack(pady=10)
        
        tk.Label(self.root, text="Amount to Withdraw:").pack(pady=5)
        self.withdraw_amount_entry = tk.Entry(self.root)
        self.withdraw_amount_entry.pack(pady=5)
        
        tk.Button(self.root, text="Withdraw", command=self.withdraw).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.account_menu).pack(pady=5)

    def withdraw(self):
        amount = self.get_float_input(self.withdraw_amount_entry.get())
        if amount is not None:
            if self.current_account.withdraw(amount):
                messagebox.showinfo("Success", f"${amount:.2f} withdrawn successfully!")
                self.account_menu()
            else:
                messagebox.showerror("Error", "Invalid withdrawal amount or insufficient funds.")
        else:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def logout(self):
        self.current_account = None
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    @staticmethod
    def get_float_input(value):
        try:
            return float(value)
        except ValueError:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    atm = ATM(root)
    root.mainloop()
