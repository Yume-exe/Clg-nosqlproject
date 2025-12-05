import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient

# --- MongoDB Setup ---
client = MongoClient(*your connection string)


db = client["finance_db"]
finance_col = db["records"]

root = tk.Tk()
root.title("Finance Tracker")
root.geometry("600x500")
root.configure(bg="#1e1e2f")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("Treeview", background="#2e2e3f", fieldbackground="#2e2e3f", foreground="white")
style.map("Treeview", background=[('selected', '#5a5ad1')])

# --- Frames ---
frame = tk.Frame(root, bg="#1e1e2f")
frame.pack(pady=10)

tk.Label(frame, text="Description", bg="#1e1e2f", fg="white").grid(row=0, column=0)
entry_desc = tk.Entry(frame, width=30)
entry_desc.grid(row=0, column=1)

tk.Label(frame, text="Amount", bg="#1e1e2f", fg="white").grid(row=1, column=0)
entry_amt = tk.Entry(frame, width=30)
entry_amt.grid(row=1, column=1)

type_var = tk.StringVar(value="Expense")
tk.Radiobutton(frame, text="Expense", variable=type_var, value="Expense", bg="#1e1e2f", fg="white").grid(row=2, column=0)
tk.Radiobutton(frame, text="Income", variable=type_var, value="Income", bg="#1e1e2f", fg="white").grid(row=2, column=1)

table = ttk.Treeview(root, columns=("desc", "amt", "type"), show='headings', height=10)
table.heading("desc", text="Description")
table.heading("amt", text="Amount")
table.heading("type", text="Type")
table.pack(pady=10)

def add_record():
    desc = entry_desc.get().strip()
    amt = entry_amt.get().strip()
    typ = type_var.get()
    if not desc or not amt or not amt.isdigit():
        messagebox.showerror("Error", "Invalid input")
        return
    finance_col.insert_one({"desc": desc, "amount": int(amt), "type": typ})
    load_records()
    entry_desc.delete(0, tk.END)
    entry_amt.delete(0, tk.END)

def load_records():
    for row in table.get_children():
        table.delete(row)
    for rec in finance_col.find():
        table.insert("", tk.END, values=(rec['desc'], rec['amount'], rec['type']))

ttk.Button(root, text="Add Record", command=add_record).pack(pady=5)
ttk.Button(root, text="Refresh", command=load_records).pack(pady=5)

load_records()
root.mainloop()
