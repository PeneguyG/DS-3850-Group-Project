import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd
import numpy as np
import sqlite3


#database & tables
def init_db():
    conn = sqlite3.connect("calico_coffee.db")
    cursor = conn.cursor()
    # TBL1 Main Menu_Options
    cursor.execute('''CREATE TABLE IF NOT EXISTS Menu_Options (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT NOT NULL,
                        price REAL NOT NULL,
                        active INTEGER DEFAULT 1)''')
    # TBL2 
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        parent_id INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        total REAL NOT NULL,
                        FOREIGN KEY (parent_id) REFERENCES Menu_Options (id))''')
    
    # Menu Options; food items, drinks, products- feel free to add whatever you guys want!
    cursor.execute("SELECT COUNT(*) FROM Menu_Options")
    if cursor.fetchone()[0] == 0:
        products = [
    ('Iced Matcha Latte', 'Drinks', 6.50, 1),
    ('Vanilla Cold Brew', 'Drinks', 5.25, 1),
    ('Caramel Latte', 'Drinks', 5.75, 1),
    ('Strawberry Refresher', 'Drinks', 4.75, 1),

    ('Ham & Cheese Croissant', 'Food', 4.25, 1),
    ('Blueberry Muffin', 'Food', 3.75, 1),
    ('Avocado Toast', 'Food', 7.00, 1),
    ('Grilled Chicken Panini', 'Food', 8.50, 1),

    ('Calico Coffee Mug', 'Products', 14.99, 1),
    ('Reusable Straw Set', 'Products', 6.00, 1),
    ('Coffee Bean Bag (Medium Roast)', 'Products', 16.50, 1)
]
        cursor.executemany("INSERT INTO Menu_Options (name, category, price, active) VALUES (?,?,?,?)", products)
    conn.commit()
    conn.close()
def reset_to_startup():
    # Message box- I wanted the app to ask for confirmation before it deleted anything
    if messagebox.askyesno("Reset", "This will delete all new sales and items. Reset to original products?"):
        conn = sqlite3.connect("calico_coffee.db")
        cursor = conn.cursor()
        # Wipe everything
        cursor.execute("DROP TABLE IF EXISTS Menu_Options")
        cursor.execute("DROP TABLE IF EXISTS sales")
        conn.commit()
        conn.close()
        
        # Re-initialize with products
        init_db()
        refresh_data()
        messagebox.showinfo("Reset Complete", "App returned to original startup state.")

def create_cute_cat_reset(parent):
    # custom cat button!
    canv = tk.Canvas(parent, width=120, height=100, highlightthickness=0)
    canv.pack(pady=10)

    # Colors
    calico_orange = "#E2A263"
    ear_pink = "#FFC0CB"

    # Left Ear
    canv.create_polygon(20, 40, 40, 10, 50, 40, fill=calico_orange, outline="black", width=2)
    canv.create_polygon(25, 38, 40, 15, 45, 38, fill=ear_pink) # Inner ear
    
    # Right Ear
    canv.create_polygon(70, 40, 80, 10, 100, 40, fill=calico_orange, outline="black", width=2)
    canv.create_polygon(75, 38, 80, 15, 95, 38, fill=ear_pink) # Inner ear

    # Head- It's just an oval
    canv.create_oval(15, 30, 105, 90, fill=calico_orange, outline="black", width=2)

    # --- Face Details ---
    # Eyes (Small dots)
    canv.create_oval(40, 55, 45, 60, fill="black")
    canv.create_oval(75, 55, 80, 60, fill="black")
    
    # Nose/Mouth (A little 'v' shape)
    canv.create_line(55, 65, 60, 70, 65, 65,  smooth=True) 

    # Whiskers
    canv.create_line(10, 60, 30, 63, fill="black") # Left
    canv.create_line(10, 70, 30, 67, fill="black")
    canv.create_line(90, 63, 110, 60, fill="black") # Right
    canv.create_line(90, 67, 110, 70, fill="black")

    # --- The Button Text ---
    canv.create_text(60, 78, text="RESET", font=("Arial", 9, "bold"), fill="white")

 
    canv.tag_bind("all", "<Button-1>", lambda e: reset_to_startup())
    
    # Hover effect for the button, trying to make it fancy 
    canv.tag_bind("all", "<Enter>", lambda e: canv.configure(cursor="hand2"))
    
    return canv

def refresh_data():
    """Updates all Treeviews and dropdowns across all tabs"""
    for tree in [Menu_OptionsView1, Menu_OptionsView2, Menu_OptionsView4, Menu_OptionsView5]:
        tree.delete(*tree.get_children())
    salesView1.delete(*salesView1.get_children())
    salesView3.delete(*salesView3.get_children())
    

    conn = sqlite3.connect("calico_coffee.db")
    # Load Menu_Options
    inv_df = pd.read_sql("SELECT * FROM Menu_Options WHERE active = 1", conn)
    for _, row in inv_df.iterrows():
        vals = (row['id'], row['name'], row['category'], row['price'], row['active'])
        for tree in [Menu_OptionsView1, Menu_OptionsView2, Menu_OptionsView4, Menu_OptionsView5]:
            tree.insert("", tk.END, values=vals)
    
    # Laod Sales
    sales_df = pd.read_sql("SELECT * FROM sales", conn)
    for _, row in sales_df.iterrows():
        s_vals = (row['id'], row['parent_id'], row['date'], row['quantity'], row['total'])
        salesView1.insert("", tk.END, values=s_vals)
        salesView3.insert("", tk.END, values=s_vals)
    conn.close()

#CRUD FUNCTIONS
def add_item():
    name = name_entry2.get()
    cat = option_men2.get()
    price = price_entry2.get()
    if name and price and cat != "Select a Category":
        conn = sqlite3.connect("calico_coffee.db")
        conn.execute("INSERT INTO Menu_Options (name, category, price) VALUES (?, ?, ?)", (name, cat, float(price)))
        conn.commit()
        conn.close()
        refresh_data()
        messagebox.showinfo("Success", "Item added to Menu_Options!")
    else:
        messagebox.showwarning("Error", "Please fill all fields")

def update():
    selected = Menu_OptionsView4.focus()
    if not selected:
        messagebox.showwarning("Selection", "Select an item in the list below first")
        return
    item_id = Menu_OptionsView4.item(selected)['values'][0]
    name, price, cat = name_entry4.get(), price_entry4.get(), option_men4.get()
    
    if name and price:
        conn = sqlite3.connect("calico_coffee.db")
        conn.execute("UPDATE Menu_Options SET name=?, category=?, price=? WHERE id=?", (name, cat, float(price), item_id))
        conn.commit()
        conn.close()
        refresh_data()
        messagebox.showinfo("Success", "Item updated!")

def delete():
    selected = Menu_OptionsView5.focus()
    if selected:
        item_id = Menu_OptionsView5.item(selected)['values'][0]
        conn = sqlite3.connect("calico_coffee.db")
        conn.execute("UPDATE Menu_Options SET active = 0 WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()
        refresh_data()
        messagebox.showinfo("Deleted", "Item is now inactive")

# --- REPORTING & SALES (Member 3) ---
def add_sale():
    item_name = option_men3.get() 
    qty = quantity_entry3.get()
    date = date_entry.get()
    
    if qty and date:
        conn = sqlite3.connect("calico_coffee.db")
        cur = conn.cursor()
        cur.execute("SELECT id, price FROM Menu_Options WHERE name = ?", (item_name,))
        res = cur.fetchone()
        if res:
            p_id, price = res
            # NumPy calculation for total
            total = np.multiply(int(qty), price)
            cur.execute("INSERT INTO sales (parent_id, date, quantity, total) VALUES (?,?,?,?)", (p_id, date, int(qty), float(total)))
            conn.commit()
        conn.close()
        refresh_data()
        messagebox.showinfo("Success", "Sale recorded!")

def generate_report():
    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT i.category, s.quantity, s.total
    FROM sales s
    JOIN Menu_Options i ON s.parent_id = i.id
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        messagebox.showinfo("Report", "No sales yet — go make some coffee sales")
        return

    # calculations
    avg_sale = np.mean(df['total'])
    max_sale = np.max(df['total'])

    grouped = df.groupby('category')[['quantity', 'total']].sum()

    report_display.delete('1.0', tk.END)

    # Calico daily header 
    report_display.insert(tk.END, "📊 Calico Coffee Daily Summary\n")
    report_display.insert(tk.END, "-----------------------------------\n")

    report_display.insert(tk.END, f"Average Sale: ${avg_sale:.2f}\n")
    report_display.insert(tk.END, f"Highest Sale: ${max_sale:.2f}\n\n")

    report_display.insert(tk.END, "Sales by Category:\n")
    report_display.insert(tk.END, grouped.to_string())

    # save CSV
    df.to_csv("calico_sales_report.csv", index=False)

    messagebox.showinfo("Report Ready", "Report generated and saved!")

    # NumPy stats
    mean_val = np.mean(df['total'])
    max_val = np.max(df['total'])
    
    # Pandas Groupby
    grouped = df.groupby('category')[['quantity', 'total']].sum()
    
    # Display in Tab 6
    report_display.delete('1.0', tk.END)
    report_display.insert(tk.END, f"--- Statistics ---\nAvg Sale: ${mean_val:.2f}\nLargest Sale: ${max_val:.2f}\n\n")
    report_display.insert(tk.END, "--- Grouped by Category ---\n")
    report_display.insert(tk.END, grouped.to_string())
    
    # CSV Export
    df.to_csv("calico_business_report.csv", index=False)
    messagebox.showinfo("CSV", "Report exported to calico_business_report.csv")

# --- UI INITIALIZATION ---
init_db()
root = tk.Tk()
root.title("Calico Management Application")
root.geometry("1024x768")

notebookTab = ttk.Notebook(root)
tab1, tab2, tab3, tab4, tab5, tab6 = [ttk.Frame(notebookTab) for _ in range(6)]


notebookTab.add(tab1, text="View =ᗢ=")
notebookTab.add(tab2, text="Add Item=ᗢ=")
notebookTab.add(tab3, text="Add Sale=ᗢ=")
notebookTab.add(tab4, text="Update Item =ᗢ=")
notebookTab.add(tab5, text="Delete Item =ᗢ=")
notebookTab.add(tab6, text="Generate Report =ᗢ=")
notebookTab.pack(expand=1, fill="both")

# --- Tab 1 Content ---
introductionLabel = ttk.Label(tab1, text="Coldbrew Calico Coffeehouse  ₊˚⊹♡ ᓚ₍ ^. .^₎", font=("Arial", 15)).pack(pady=10)
Menu_OptionsView1 = ttk.Treeview(tab1, columns=("id","name","category","price","active"), show="headings")
for c in ("id","name","category","price","active"): Menu_OptionsView1.heading(c, text=c.title())
Menu_OptionsView1.pack()
salesView1 = ttk.Treeview(tab1, columns=("id","parent_id","date","quantity","total"), show="headings")
for c in ("id","parent_id","date","quantity","total"): salesView1.heading(c, text=c.title())
salesView1.pack()


reset_btn = tk.Button(tab1, text="Reset to Startup State", 
                      command=reset_to_startup, 
                      bg="#FF3C3C", fg="white", font=("Arial", 10))
# Instead of the standard button, use the custom cat head
create_cute_cat_reset(tab1)



# --- Tab 2 Content (Add) ---
options = ["Drinks", "Food", "Products"]
tk.Label(tab2, text="Item Name").pack()
name_entry2 = tk.Entry(tab2); name_entry2.pack()
option_men2 = tk.StringVar(value="Drinks")
tk.OptionMenu(tab2, option_men2, *options).pack()
tk.Label(tab2, text="Price").pack()
price_entry2 = tk.Entry(tab2); price_entry2.pack()
tk.Button(tab2, text="Add Item", command=add_item, bg="#E2A263").pack(pady=10)
Menu_OptionsView2 = ttk.Treeview(tab2, columns=("id","name","category","price","active"), show="headings")
for c in ("id","name","category","price","active"): Menu_OptionsView2.heading(c, text=c.title())
Menu_OptionsView2.pack()

# --- Tab 3 Content (Sales) ---
option_men3 = tk.StringVar(value="Espresso") # Ideally populated from names list
tk.OptionMenu(tab3, option_men3, "Espresso", "Latte", "Mocha", "Croissant").pack()
date_entry = tk.Entry(tab3); date_entry.insert(0, "2026-04-30"); date_entry.pack()
quantity_entry3 = tk.Entry(tab3); quantity_entry3.pack()
tk.Button(tab3, text="Add Sale", command=add_sale, bg="#E2A263").pack(pady=5)
salesView3 = ttk.Treeview(tab3, columns=("id","parent_id","date","quantity","total"), show="headings")
for c in ("id","parent_id","date","quantity","total"): salesView3.heading(c, text=c.title())
salesView3.pack()

# Update Tab, (4)
tk.Label(tab4, text="New Name").pack()
name_entry4 = tk.Entry(tab4); name_entry4.pack()
option_men4 = tk.StringVar(value="Drinks")
tk.OptionMenu(tab4, option_men4, *options).pack()
tk.Label(tab4, text="New Price").pack()
price_entry4 = tk.Entry(tab4); price_entry4.pack()
tk.Button(tab4, text="Update Selected", command=update).pack()
Menu_OptionsView4 = ttk.Treeview(tab4, columns=("id","name","category","price","active"), show="headings")
for c in ("id","name","category","price","active"): Menu_OptionsView4.heading(c, text=c.title())
Menu_OptionsView4.pack()

# Deletion Tab,(5)
tk.Button(tab5, text="Delete Selected Item", command=delete, bg="red", fg="white").pack(pady=20)
Menu_OptionsView5 = ttk.Treeview(tab5, columns=("id","name","category","price","active"), show="headings")
for c in ("id","name","category","price","active"): Menu_OptionsView5.heading(c, text=c.title())
Menu_OptionsView5.pack()

# Reports Tab (6); ui set up 
tk.Button(tab6, text="Generate Business Report", command=summary).pack(pady=10)
report_display = scrolledtext.ScrolledText(tab6, width=70, height=20)
report_display.pack()

refresh_data()
root.mainloop()
