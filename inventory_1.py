import sqlite3
import hashlib
import tkinter as tk
from tkinter import messagebox

# Setup the database
def setup_database():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Create products table
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 quantity INTEGER NOT NULL,
                 price REAL NOT NULL)''')

    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL UNIQUE,
                 password TEXT NOT NULL)''')

    # Create sales table
    c.execute('''CREATE TABLE IF NOT EXISTS sales (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 product_id INTEGER,
                 quantity INTEGER,
                 total_price REAL,
                 date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                 FOREIGN KEY (product_id) REFERENCES products (id))''')

    conn.commit()
    conn.close()

setup_database()

# User authentication functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  (username, hash_password(password)))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # Username already exists
    finally:
        conn.close()
    return True

def authenticate_user(username, password):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        return True
    return False

# GUI class
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.current_user = None
        
        self.login_screen()
    
    def login_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Username").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1)
        
        tk.Label(self.root, text="Password").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.grid(row=1, column=1)
        
        tk.Button(self.root, text="Login", command=self.login).grid(row=2, column=0)
        tk.Button(self.root, text="Register", command=self.register).grid(row=2, column=1)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if authenticate_user(username, password):
            self.current_user = username
            self.main_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if register_user(username, password):
            messagebox.showinfo("Success", "User registered successfully")
        else:
            messagebox.showerror("Error", "Username already exists")
    
    def main_screen(self):
        self.clear_screen()
        
        tk.Button(self.root, text="Add Product", command=self.add_product_screen).grid(row=0, column=0)
        tk.Button(self.root, text="Edit Product", command=self.edit_product_screen).grid(row=0, column=1)
        tk.Button(self.root, text="Delete Product", command=self.delete_product_screen).grid(row=0, column=2)
        tk.Button(self.root, text="View Inventory", command=self.view_inventory_screen).grid(row=0, column=3)
        tk.Button(self.root, text="Record Sale", command=self.record_sale_screen).grid(row=1, column=0)
        tk.Button(self.root, text="Low Stock Report", command=self.low_stock_report).grid(row=1, column=1)
        tk.Button(self.root, text="Sales Summary", command=self.sales_summary).grid(row=1, column=2)
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def add_product_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Product Name").grid(row=0, column=0)
        self.product_name_entry = tk.Entry(self.root)
        self.product_name_entry.grid(row=0, column=1)
        
        tk.Label(self.root, text="Quantity").grid(row=1, column=0)
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=1, column=1)
        
        tk.Label(self.root, text="Price").grid(row=2, column=0)
        self.price_entry = tk.Entry(self.root)
        self.price_entry.grid(row=2, column=1)
        
        tk.Button(self.root, text="Add", command=self.add_product).grid(row=3, column=0, columnspan=2)
    
    def add_product(self):
        name = self.product_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        
        if not name or not quantity or not price:
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price")
            return
        
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Product added successfully")
        self.main_screen()
    
    def edit_product_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Product ID").grid(row=0, column=0)
        self.product_id_entry = tk.Entry(self.root)
        self.product_id_entry.grid(row=0, column=1)
        
        tk.Label(self.root, text="New Quantity").grid(row=1, column=0)
        self.new_quantity_entry = tk.Entry(self.root)
        self.new_quantity_entry.grid(row=1, column=1)
        
        tk.Label(self.root, text="New Price").grid(row=2, column=0)
        self.new_price_entry = tk.Entry(self.root)
        self.new_price_entry.grid(row=2, column=1)
        
        tk.Button(self.root, text="Update", command=self.update_product).grid(row=3, column=0, columnspan=2)
    
    def update_product(self):
        product_id = self.product_id_entry.get()
        new_quantity = self.new_quantity_entry.get()
        new_price = self.new_price_entry.get()
        
        if not product_id or not new_quantity or not new_price:
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            product_id = int(product_id)
            new_quantity = int(new_quantity)
            new_price = float(new_price)
        except ValueError:
            messagebox.showerror("Error", "Invalid ID, quantity or price")
            return
        
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("UPDATE products SET quantity=?, price=? WHERE id=?", (new_quantity, new_price, product_id))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Product updated successfully")
        self.main_screen()
    
    def delete_product_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Product ID").grid(row=0, column=0)
        self.product_id_entry = tk.Entry(self.root)
        self.product_id_entry.grid(row=0, column=1)
        
        tk.Button(self.root, text="Delete", command=self.delete_product).grid(row=1, column=0, columnspan=2)
    
    def delete_product(self):
        product_id = self.product_id_entry.get()
        
        if not product_id:
            messagebox.showerror("Error", "Product ID is required")
            return
        
        try:
            product_id = int(product_id)
        except ValueError:
            messagebox.showerror("Error", "Invalid Product ID")
            return
        
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Product deleted successfully")
        self.main_screen()
    
    def view_inventory_screen(self):
        self.clear_screen()
        
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        products = c.fetchall()
        conn.close()
        
        row = 0
        for product in products:
            tk.Label(self.root, text=f"ID: {product[0]}, Name: {product[1]}, Quantity: {product[2]}, Price: {product[3]}").grid(row=row, column=0, columnspan=4)
            row += 1
        
        tk.Button(self.root, text="Back", command=self.main_screen).grid(row=row, column=0, columnspan=4)

    def record_sale_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Product ID").grid(row=0, column=0)
        self.sale_product_id_entry = tk.Entry(self.root)
        self.sale_product_id_entry.grid(row=0, column=1)
        
        tk.Label(self.root, text="Quantity Sold").grid(row=1, column=0)
        self.sale_quantity_entry = tk.Entry(self.root)
        self.sale_quantity_entry.grid(row=1, column=1)
        
        tk.Button(self.root, text="Record Sale", command=self.record_sale).grid(row=2, column=0, columnspan=2)
    
    def record_sale(self):
        product_id = self.sale_product_id_entry.get()
        quantity_sold = self.sale_quantity_entry.get()
        
        if not product_id or not quantity_sold:
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            product_id = int(product_id)
            quantity_sold = int(quantity_sold)
        except ValueError:
            messagebox.showerror("Error", "Invalid ID or quantity")
            return
        
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        
        # Check if product exists and has sufficient stock
        c.execute("SELECT quantity, price FROM products WHERE id=?", (product_id,))
        product = c.fetchone()
        if not product:
            messagebox.showerror("Error", "Product not found")
            conn.close()
            return
        
        current_quantity, price = product
        if current_quantity < quantity_sold:
            messagebox.showerror("Error", "Insufficient stock")
            conn.close()
            return
        
        total_price = quantity_sold * price
        new_quantity = current_quantity - quantity_sold
        
        # Update product quantity
        c.execute("UPDATE products SET quantity=? WHERE id=?", (new_quantity, product_id))
        
        # Record the sale
        c.execute("INSERT INTO sales (product_id, quantity, total_price) VALUES (?, ?, ?)",
                  (product_id, quantity_sold, total_price))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Sale recorded successfully")
        self.main_screen()
    
    def low_stock_report(self):
        self.clear_screen()
        
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products WHERE quantity < 5")  # Assuming low stock threshold is 5
        products = c.fetchall()
        conn.close()
        
        row = 0
        for product in products:
            tk.Label(self.root, text=f"ID: {product[0]}, Name: {product[1]}, Quantity: {product[2]}, Price: {product[3]}").grid(row=row, column=0, columnspan=4)
            row += 1
        
        tk.Button(self.root, text="Back", command=self.main_screen).grid(row=row, column=0, columnspan=4)
    
    def sales_summary(self):
        self.clear_screen()
        
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT p.name, s.quantity, s.total_price, s.date FROM sales s JOIN products p ON s.product_id = p.id")
        sales = c.fetchall()
        conn.close()
        
        row = 0
        for sale in sales:
            tk.Label(self.root, text=f"Product: {sale[0]}, Quantity Sold: {sale[1]}, Total Price: {sale[2]}, Date: {sale[3]}").grid(row=row, column=0, columnspan=4)
            row += 1
        
        tk.Button(self.root, text="Back", command=self.main_screen).grid(row=row, column=0, columnspan=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
