import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd
import numpy as np
import sqlite3 
root = tk.Tk()
root.title("Calico Management Application")
root.geometry("1024x768")

'''
Functions for the program
'''
#include the function to refresh each tree after an update
def add_item():
    #Placeholder please edit
    print("meow")

def add_sale():
    #Placeholder please edit
    print("meow sale")

def update():
    #Placeholder please edit
    print("meow update")

def delete():
    #Placehold please edit
    print("meow delete")

def summary():
    #Summary report
    def summary():
    import sqlite3

    conn = sqlite3.connect("calico.db")

    query = """
    SELECT 
        inventory.name,
        inventory.category,
        inventory.price,
        sales.quantity,
        sales.date
    FROM sales
    JOIN inventory ON sales.parent_id = inventory.id
    """

    df = pd.read_sql(query, conn)
    print("meow summary")

'''
Main gui set up for the program
'''
notebookTab = ttk.Notebook(root)

tab1 = ttk.Frame(notebookTab)
tab2 = ttk.Frame(notebookTab)
tab3 = ttk.Frame(notebookTab)
tab4 = ttk.Frame(notebookTab)
tab5 = ttk.Frame(notebookTab)
tab6 = ttk.Frame(notebookTab)


notebookTab.add(tab1, text = "View =ᗢ=")
notebookTab.add(tab2, text="Add Item=ᗢ=")
notebookTab.add(tab3, text="Add Sale=ᗢ=")
notebookTab.add(tab4, text="Update Item =ᗢ=")
notebookTab.add(tab5, text="Delete Item =ᗢ=")
notebookTab.add(tab6, text="Generate Report =ᗢ=")
notebookTab.pack(expand = 1, fill = "both")

'''
Content for the View tab
'''

introductionLabel = ttk.Label(tab1, text="Coldbrew Calico Coffeehouse  ₊˚⊹♡ ᓚ₍ ^. .^₎", font=("Arial", 15))
introductionLabel.pack(padx=20,pady=20)
viewLabel_item = ttk.Label(tab1, text="Inventory", font=("Arial", 12))
viewLabel_item.pack(padx=20,pady=20)
#Setting up the treeview
inventoryView1 = ttk.Treeview(tab1, columns=("id","name","category","price","active"), show="headings")

inventoryView1.heading("id", text="ID")
inventoryView1.heading("name", text="Name")
inventoryView1.heading("category", text="Category")
inventoryView1.heading("price", text="Price")
inventoryView1.heading("active", text="Active")

inventoryView1.pack()

viewLabel_sales = ttk.Label(tab1, text="Sales", font=("Arial", 12))
viewLabel_sales.pack(padx=20,pady=20)

salesLabel1 = ttk.Label(tab1, text="Coffee Shop Sales")
salesView1 = ttk.Treeview(tab1, columns=("id","parent_id","date","quantity","total"), show="headings")

salesView1.heading("id", text="ID")
salesView1.heading("parent_id", text="Parent ID")
salesView1.heading("date", text="Date")
salesView1.heading("quantity", text="Quantity")
salesView1.heading("total",text="Total")

salesView1.pack()

#Implement a panda to loop through the 
#template: for index, row in (panda group name).iterrows():
    #treeView.insert("",tk.END, values=['id'],......))

#-------------------------------------------------------------------------------------
'''
Content for the Add tab for inventory
'''

options = ["Drinks", "Food", "Products"]

name_label2=tk.Label(tab2,text='Item name',font=('Arial', 12))
name_label2.pack(pady=2)
name_entry2=tk.Entry(tab2, width=30, font=('Arial',12))
name_entry2.pack(pady=2)

option_men2= tk.StringVar(tab2)
option_men2.set("Select a Category")

client_label2=tk.Label(tab2,text='Category',font=('Arial', 12))
client_label2.pack(pady=2)
client_menu2 = tk.OptionMenu(tab2,option_men2,*options).pack(pady=10)

price_label2=tk.Label(tab2,text='Price',font=('Arial', 12))
price_label2.pack(pady=5)
price_entry2=tk.Entry(tab2, width=30, font=('Arial',12))
price_entry2.pack(pady=5)

add_btn2 = tk.Button(tab2, text='Add Item',command=add_item,font=('Arial',12), bg="#E2A263",fg='white')
add_btn2.pack(pady=2)

#The active setting will be a default addition in the creation of the database so when creating it will auto be 1 which means active (0 is inactive)

viewLabel2 = ttk.Label(tab2, text="Inventory", font=("Arial", 12))
viewLabel2.pack(padx=20,pady=20)

#Setting up the treeview for inventory adding
inventoryView2 = ttk.Treeview(tab2, columns=("id","name","category","price","active"), show="headings")

inventoryView2.heading("id", text="ID")
inventoryView2.heading("name", text="Name")
inventoryView2.heading("category", text="Category")
inventoryView2.heading("price", text="Price")
inventoryView2.heading("active", text="Active")

inventoryView2.pack()

#-------------------------------------------------------------------------------------
'''
Content for the add tab for sales
'''


'''
Option menu needs to be implemented through the following code below:

cursor.execute('SELECT name FROM inventory')
#collecting the list of clients from the database
    rows = cursor.fetchall()
    flat = [r[0] for r in rows]
    names = np.array(flat)

    change the "*options" to *names when this is implemented
'''
names = ["meow"]
option_men3= tk.StringVar(tab3)
option_men3.set("Select an Item")

parent_label3=tk.Label(tab3,text='Parent Item',font=('Arial', 12))
parent_label3.pack(pady=3)
parent_menu = tk.OptionMenu(tab3,option_men3,*names).pack(pady=10)

date_label=tk.Label(tab3,text='Date (ex.2026-04-22 or 20260422)',font=('Arial', 12))
date_label.pack(pady=2)
date_entry=tk.Entry(tab3, width=30, font=('Arial',12))
date_entry.pack(pady=2)


quantity_label3=tk.Label(tab3,text='Quantity',font=('Arial', 12))
quantity_label3.pack(pady=5)
quantity_entry3=tk.Entry(tab3, width=30, font=('Arial',12))
quantity_entry3.pack(pady=5)

add_btn3 = tk.Button(tab3, text='Add Sale',command=add_sale,font=('Arial',12), bg="#E2A263",fg='white')
add_btn3.pack(pady=5)

#Note: Total will be calculated with numpy and appended to the database Quantity x Price from the parent item so this will need to be included

salesView3 = ttk.Treeview(tab3, columns=("id","parent_id","date","quantity","total"), show="headings")

salesView3.heading("id", text="ID")
salesView3.heading("parent_id", text="Parent ID")
salesView3.heading("date", text="Date")
salesView3.heading("quantity", text="Quantity")
salesView3.heading("total",text="Total")

salesView3.pack()
#-------------------------------------------------------------------------------------
'''
Content for the Update Item feature
'''
#options were already defined in function 2 so no need to redefine them

name_label4=tk.Label(tab4,text='Item name',font=('Arial', 12))
name_label4.pack(pady=2)
name_entry4=tk.Entry(tab4, width=30, font=('Arial',12))
name_entry4.pack(pady=2)

option_men4= tk.StringVar(tab4)
option_men4.set("Select a Category")

client_label4=tk.Label(tab4,text='Category',font=('Arial', 12))
client_label4.pack(pady=2)
client_menu4 = tk.OptionMenu(tab4,option_men4,*options).pack(pady=10)

price_label4=tk.Label(tab4,text='Price',font=('Arial', 12))
price_label4.pack(pady=5)
price_entry4=tk.Entry(tab4, width=30, font=('Arial',12))
price_entry4.pack(pady=5)

update_btn4 = tk.Button(tab4, text='Add Item',command=update,font=('Arial',12), bg="#E2A263",fg='white')
update_btn4.pack(pady=2)

#The active setting will be a default addition in the creation of the database so when creating it will auto be 1 which means active (0 is inactive)

viewLabel4 = ttk.Label(tab4, text="Inventory", font=("Arial", 12))
viewLabel4.pack(padx=20,pady=20)

#Setting up the treeview for inventory adding
inventoryView4 = ttk.Treeview(tab4, columns=("id","name","category","price","active"), show="headings")

inventoryView4.heading("id", text="ID")
inventoryView4.heading("name", text="Name")
inventoryView4.heading("category", text="Category")
inventoryView4.heading("price", text="Price")
inventoryView4.heading("active", text="Active")

inventoryView4.pack()
#-------------------------------------------------------------------------------------
'''
Content for Deleting Item Feature
'''
#Delete by selecting which item is focused on you can do this through item = treename.focus()
viewLabel5 = ttk.Label(tab5, text="Select an item by clicking and Click the delete button", font=("Arial", 12))
viewLabel5.pack(padx=20,pady=20)

#Setting up the treeview for inventory adding
inventoryView5 = ttk.Treeview(tab5, columns=("id","name","category","price","active"), show="headings")

inventoryView5.heading("id", text="ID")
inventoryView5.heading("name", text="Name")
inventoryView5.heading("category", text="Category")
inventoryView5.heading("price", text="Price")
inventoryView5.heading("active", text="Active")

inventoryView5.pack()

delete_btn5 = tk.Button(tab5, text='Delete Item',command=delete,font=('Arial',12), bg="#FF3C3C",fg='white')
delete_btn5.pack(pady=2)

#-------------------------------------------------------------------------------------
'''
Content for Deleting Item Feature
'''


root.mainloop()
