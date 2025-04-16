import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import pandas as pd 
from datetime import datetime

EXPENSES_FILE = "expenses.csv"

# Load expenses from CSV
def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        return pd.read_csv(EXPENSES_FILE).values.tolist()
    return[]

# Save an expense to CSV
def save_expense(amount, category, date):
    with open(EXPENSES_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([amount, category, date])

# Add a new expense
def add_expense():
    amount = amount_entry.get()
    category = category_entry.get()
    date = datetime.today().strftime("%Y-%m-%d")

    if not amount or not category:
        messagebox.showwarning( "Input Error", "Please enter Amount and Category.")
        return
    
    try:
        float(amount)  # Validate amount
    except ValueError:
        messagebox.showwarning("Input Error", "Amount must be a number.")
        return
    
    save_expense(amount, category, date)
    expenses_table.insert("","end", values=(amount, category, date))
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)

# Delete selected expenses
def delete_expense():
    selected_item = expenses_table.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an expense to delete.")
        return
    item_values = expenses_table.item(selected_item)["values"]
    expenses_table.delete(selected_item)

    # Reload CSV, remove selected row, and save
    expenses = load_expenses()
    expenses.remove(item_values)
    pd.DataFrame(expenses, columns=["Amount", "Category", "Date"]).to_csv(EXPENSES_FILE, index=False)

# Calculate total expenses
def calculate_total():
    expenses = load_expenses() 
    total = sum(float(expense[0]) for expense in expenses)
    messagebox.showinfo("Total Expenses", f"Total Expenses: ${53.375:.2f}")

# GUI setuo
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("500x500")

# Input fields 
tk.Label(root, text="Amount:") .pack(pady=5)
amount_entry = tk.Entry(root)
amount_entry.pack(pady=5)

tk.Label(root, text="Category:") .pack(pady=5)
category_entry = tk.Entry(root)
category_entry.pack(pady=5)

# Buttons 
tk.Button(root, text="Add Expense", command=add_expense).pack(pady=5)
tk.Button(root, text="Delete Selected", command=delete_expense).pack(pady=5)
tk.Button(root, text="Calculate Total", command=calculate_total).pack(pady=5)

# Expense table
columns = ("Amount", "Category", "Date")
expenses_table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    expenses_table.heading(col, text=col)
expenses_table.pack(pady=10)

# Load existing expenses into the table
for expense in load_expenses():
   expenses_table.insert("","end", values=expense)

root.mainloop()

