import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient

#connection
client = MongoClient(*atlas string here)
db = client["finance_db"]
finance_col = db["records"]

#gui
root = tk.Tk()
root.title("Finance Tracker")
root.geometry("800x640")
root.configure(bg="#1d1b26")

#style
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 11), padding=8, background="#4b4dbd", foreground="white")
style.map("TButton", background=[('active', '#363899')])
style.configure("Treeview", background="#2a2836", fieldbackground="#2a2836", foreground="white", rowheight=28)
style.map("Treeview", background=[('selected', '#4b4dbd')])

header = tk.Label(root, text="Finance Tracker", font=("Segoe UI", 20, "bold"), fg="white", bg="#1d1b26")
header.pack(pady=10)

frame = tk.Frame(root, bg="#1d1b26")
frame.pack(pady=5)

tk.Label(frame, text="Description", bg="#1d1b26", fg="white", font=("Segoe UI", 11)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
entry_desc = tk.Entry(frame, width=35)
entry_desc.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Amount", bg="#1d1b26", fg="white", font=("Segoe UI", 11)).grid(row=1, column=0, padx=10, pady=5, sticky='e')
entry_amt = tk.Entry(frame, width=35)
entry_amt.grid(row=1, column=1, pady=5)

type_var = tk.StringVar(value="Expense")
radio_frame = tk.Frame(frame, bg="#1d1b26")
radio_frame.grid(row=2, column=1, pady=5, sticky='w')

tk.Radiobutton(radio_frame, text="Expense", variable=type_var, value="Expense", bg="#1d1b26", fg="white", selectcolor="#2a2836").pack(side="left", padx=6)
tk.Radiobutton(radio_frame, text="Income", variable=type_var, value="Income", bg="#1d1b26", fg="white", selectcolor="#2a2836").pack(side="left", padx=6)

balance_label = tk.Label(root, text="Total Balance: ₹0", font=("Segoe UI", 14, "bold"), bg="#1d1b26", fg="#76ff76")
balance_label.pack(pady=10)

#table
table = ttk.Treeview(root, columns=("desc", "amt", "type"), show='headings', height=10)
table.heading("desc", text="Description")
table.heading("amt", text="Amount")
table.heading("type", text="Type")
table.pack(pady=10, fill='x', padx=15)

# fucntions
def update_balance():
    total = 0
    for rec in finance_col.find():
        if rec.get('type') == "Income":
            total += rec.get('amount', 0)
        else:
            total -= rec.get('amount', 0)
    balance_label.config(text=f"Total Balance: ₹{total}")


def add_record():
    desc = entry_desc.get().strip()
    amt = entry_amt.get().strip()
    typ = type_var.get()

    if not desc:
        messagebox.showerror("Error", "Please enter a description.")
        return
    try:
        amount_val = int(float(amt))
    except Exception:
        messagebox.showerror("Error", "Please enter a valid numeric amount.")
        return

    finance_col.insert_one({"desc": desc, "amount": amount_val, "type": typ})
    load_records()
    entry_desc.delete(0, tk.END)
    entry_amt.delete(0, tk.END)


def load_records():
    for row in table.get_children():
        table.delete(row)
    for rec in finance_col.find():
        table.insert("", tk.END, values=(rec.get('desc',''), rec.get('amount',0), rec.get('type','')))
    update_balance()

def reset_all():
    finance_col.delete_many({})
    load_records()
    messagebox.showinfo("Reset", "All records have been cleared.")


# buttons
btn_frame = tk.Frame(root, bg="#1d1b26")
btn_frame.pack(pady=8)

add_btn = ttk.Button(btn_frame, text="Add Record", command=add_record)
add_btn.grid(row=0, column=0, padx=8)

refresh_btn = ttk.Button(btn_frame, text="Refresh", command=load_records)
refresh_btn.grid(row=0, column=1, padx=8)

ttk.Button(btn_frame, text="Reset All", command=reset_all).grid(row=0, column=2, padx=8)


root.bind('<Return>', lambda event: add_record())

load_records()
root.mainloop()
