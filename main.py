import customtkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from database import get_connection
import matplotlib.pyplot as plt

# ---------------- Functions ---------------- #

def add_product():
    name = name_entry.get()
    qty = qty_entry.get()
    price = price_entry.get()
    category = category_var.get()
    unit = unit_var.get()

    if name and qty and price and category and unit:
        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute("INSERT INTO products (name, quantity, price, category, unit) VALUES (%s,%s,%s,%s,%s)",
                        (name, qty, price, category, unit))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "✅ Product added successfully!")
            clear_fields()
            show_products()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
    else:
        messagebox.showwarning("Input Error", "All fields are required!")

def show_products():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    con.close()

    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert("", "end", values=row)

def delete_product():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Item", "Please select a product to delete.")
        return
    item = tree.item(selected)
    pid = item["values"][0]
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (pid,))
    con.commit()
    con.close()
    messagebox.showinfo("Deleted", "🗑 Product deleted successfully.")
    show_products()

def modify_product():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Item", "Please select a product to modify.")
        return

    item = tree.item(selected)
    pid = item["values"][0]

    def save_changes():
        new_name = name_edit.get()
        new_qty = qty_edit.get()
        new_price = price_edit.get()
        new_category = category_edit.get()
        new_unit = unit_edit.get()

        if new_name and new_qty and new_price:
            con = get_connection()
            cur = con.cursor()
            cur.execute(
                "UPDATE products SET name=%s, quantity=%s, price=%s, category=%s, unit=%s WHERE id=%s",
                (new_name, new_qty, new_price, new_category, new_unit, pid)
            )
            con.commit()
            con.close()
            messagebox.showinfo("Updated", "✅ Product details updated successfully.")
            edit_window.destroy()
            show_products()
        else:
            messagebox.showwarning("Input Error", "All fields are required.")

    # Edit Window
    edit_window = tk.CTkToplevel(root)
    edit_window.title("Modify Product")
    edit_window.geometry("400x400")

    tk.CTkLabel(edit_window, text="Product Name").pack(pady=5)
    name_edit = tk.CTkEntry(edit_window)
    name_edit.insert(0, item["values"][1])
    name_edit.pack()

    tk.CTkLabel(edit_window, text="Quantity").pack(pady=5)
    qty_edit = tk.CTkEntry(edit_window)
    qty_edit.insert(0, item["values"][2])
    qty_edit.pack()

    tk.CTkLabel(edit_window, text="Price").pack(pady=5)
    price_edit = tk.CTkEntry(edit_window)
    price_edit.insert(0, item["values"][3])
    price_edit.pack()

    tk.CTkLabel(edit_window, text="Category").pack(pady=5)
    category_edit = tk.CTkEntry(edit_window)
    category_edit.insert(0, item["values"][4])
    category_edit.pack()

    tk.CTkLabel(edit_window, text="Unit").pack(pady=5)
    unit_edit = tk.CTkEntry(edit_window)
    unit_edit.insert(0, item["values"][5])
    unit_edit.pack()

    tk.CTkButton(edit_window, text="💾 Save Changes", command=save_changes).pack(pady=10)

def clear_fields():
    name_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

def show_category_analysis():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT category, SUM(quantity * price) AS total_value FROM products GROUP BY category")
    data = cur.fetchall()
    con.close()

    if not data:
        messagebox.showinfo("No Data", "No products available for analysis.")
        return

    categories = [row[0] for row in data]
    values = [float(row[1]) for row in data]

    chart_type = chart_type_var.get()

    plt.figure(figsize=(7, 5))
    if chart_type == "Bar Chart":
        plt.bar(categories, values)
        plt.ylabel("Total Value (₹)")
    else:
        plt.pie(values, labels=categories, autopct="%1.1f%%", startangle=90)
        plt.axis("equal")

    plt.title("Category-wise Inventory Value")
    plt.tight_layout()
    plt.show()

# ---------------- UI Setup ---------------- #

root = tk.CTk()
root.title("📦 Inventory Management System")
root.geometry("900x700")

tk.CTkLabel(root, text="Inventory Management System", font=("Arial", 22, "bold")).pack(pady=15)

frame = tk.CTkFrame(root)
frame.pack(pady=10)

# Product Input Fields
tk.CTkLabel(frame, text="Product Name").grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.CTkEntry(frame)
name_entry.grid(row=0, column=1, padx=10)

tk.CTkLabel(frame, text="Quantity").grid(row=1, column=0, padx=10, pady=5)
qty_entry = tk.CTkEntry(frame)
qty_entry.grid(row=1, column=1, padx=10)

tk.CTkLabel(frame, text="Unit").grid(row=1, column=2, padx=10, pady=5)
unit_var = tk.StringVar(value="pcs")
unit_dropdown = tk.CTkComboBox(frame, values=["pcs", "kg", "litre", "packet"], variable=unit_var)
unit_dropdown.grid(row=1, column=3, padx=10)

tk.CTkLabel(frame, text="Price (₹)").grid(row=2, column=0, padx=10, pady=5)
price_entry = tk.CTkEntry(frame)
price_entry.grid(row=2, column=1, padx=10)

tk.CTkLabel(frame, text="Category").grid(row=2, column=2, padx=10, pady=5)
category_var = tk.StringVar(value="Snacks")
category_dropdown = tk.CTkComboBox(frame, values=["Snacks", "Beverages", "Dairy", "Groceries", "Fruits", "Vegetables"], variable=category_var)
category_dropdown.grid(row=2, column=3, padx=10)

# Buttons
tk.CTkButton(root, text="➕ Add Product", command=add_product).pack(pady=5)
tk.CTkButton(root, text="📋 Show Products", command=show_products).pack(pady=5)
tk.CTkButton(root, text="🗑 Delete Product", command=delete_product).pack(pady=5)
tk.CTkButton(root, text="✏️ Modify Product", command=modify_product).pack(pady=5)

# Chart Type Selector
chart_type_var = tk.StringVar(value="Bar Chart")
tk.CTkLabel(root, text="Select Chart Type:").pack(pady=5)
chart_type_dropdown = tk.CTkComboBox(root, values=["Bar Chart", "Pie Chart"], variable=chart_type_var)
chart_type_dropdown.pack()

tk.CTkButton(root, text="📊 Category Analysis", command=show_category_analysis).pack(pady=5)

# Product List
columns = ("ID", "Name", "Quantity", "Price", "Category", "Unit")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)
tree.pack(pady=15, fill="x")

show_products()

root.mainloop()
