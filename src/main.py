#import customtkinter
import customtkinter as Tk
from CustomTkinterMessagebox import CTkMessagebox

from datetime import date

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pylab as plt

import numpy as np

import pandas as pd
from PIL import Image

from tkcalendar import Calendar, DateEntry
from tkinter import ttk

#import from database
from database import *

################# colors ###############
co0 = "#d82600"  # red
co1 = "#feffff"  # white
co2 = "#4fa882"  # green
co3 = "#038cfc"  # blue
co4 = "#2b2b2b"  # gray
co5 = "black"    # black

# Create data tables
create_categories()
create_income()
create_expenses()

# open screen -----------------------------------------------------
window = Tk.CTk()
window.title()
window.geometry("1200x800")
window.configure(background=co1)
window.resizable(width=False, height=False)

frame_width = 1180


################ function #####################
global tree

# function to show expenses  -----------------------------------------------------
def show_expenses():
    global tree

    table_head = ["id", "categories", "Date", "amount"]
    list_items = table()

    hd = ["center","center","center","center"]
    h = [30, 210, 165 ,100]
    n = 0

    # create the tree view -----------------------------------------------------
    
    tree = ttk.Treeview(frame_income,columns=table_head ,selectmode="extended", show="headings")
    vsb = Tk.CTkScrollbar(frame_income, orientation="vertical", command=tree.yview)
    hsb = Tk.CTkScrollbar(frame_income, orientation="horizontal", command=tree.xview)

    tree.grid(row=0,column=0, sticky="nsew")
    vsb.grid(row=0,column=1, sticky="ns")
    hsb.grid(row=1,column=0, sticky="ew")

    
    for col in table_head:
        tree.heading(col, text=col.title(), anchor="center")
        tree.column(col, width=h[n], anchor=hd[n])

        n+=1

    for items in list_items:
        tree.insert("", "end", values=items)

# Progressbar -----------------------------------------------------
def percentage():
    value = percentage_left()

    # text
    label_name = Tk.CTkLabel(framemiddle,
                             text="percentage of cash left to used",
                             height=1,
                             anchor="nw",
                             font=("verdana",12),
                             )
    label_name.place(x=80,y=50)
    
    # bar
    progressbar = Tk.CTkProgressBar(framemiddle,
                                    orientation="horizontal",
                                    height=25,
                                    width=300.
                                    )
    progressbar.place(x=5,y=5)
    progressbar.set(value/100)

    label_percentage = Tk.CTkLabel(framemiddle,
                             text="{:,.2f}%".format(value),
                             height=1,
                             anchor="nw",
                             font=("verdana",12),
                             )
    label_percentage.place(x=140,y=35)

# bar function -----------------------------------------------------
def bar_function():
    list_categories = ["Income", "Expenses", "Balance"]
    list_values =  bar_table()

    plt.style.use("bmh")
    bar_color = [co2,co0,co3]

    figure= plt.Figure(figsize=(5,4),dpi=60, facecolor=co4)
    ax = figure.add_subplot(111)
    ax.bar(list_categories, list_values, color=bar_color)

    text_color = 'white'
    ax.set_title("Income vs Expenses", color=text_color)

    # change colors of axis
    ax.tick_params(axis="x", colors=text_color)
    ax.tick_params(axis="y", colors=text_color)

    canvas = FigureCanvasTkAgg(figure, master=framemiddle)
    canvas.get_tk_widget().place(x=30,y=80)

# summary -----------------------------------------------------
def summary():
    values = bar_table()
    
    # line one Monthly Income 
    line = Tk.CTkLabel(framemiddle, 
                       text="", 
                       width=200, 
                       height=2, 
                       anchor="nw", 
                       font=("Arial", 1), 
                       bg_color="white"
                       )
    line.place(x=330,y=60)

    line_text = Tk.CTkLabel(framemiddle,
                            text="Monthly Income",
                            font=("Arial", 25)
                            )
    line_text.place(x=340,y=30)
    
    line_summary = Tk.CTkLabel(framemiddle,
                               text="¥ {:}".format(values[0]), 
                               anchor="nw",
                               font=("Arial", 20)
                               )
    line_summary.place(x=405, y=70)
    
    # line two 
    line = Tk.CTkLabel(framemiddle, 
                       text="", 
                       width=200, 
                       height=2, 
                       anchor="nw", 
                       font=("Arial", 1), 
                       bg_color="white"
                       )
    line.place(x=330,y=150)

    line_text = Tk.CTkLabel(framemiddle,
                            text="Expenses",
                            font=("Arial", 25)
                            )
    line_text.place(x=380,y=120)
    
    line_summary = Tk.CTkLabel(framemiddle,
                               text="¥ {:}".format(values[1]), 
                               anchor="nw",
                               font=("Arial", 20)
                               )
    line_summary.place(x=405, y=160)

    # line three
    line = Tk.CTkLabel(framemiddle, 
                       text="", 
                       width=200, 
                       height=2, 
                       anchor="nw", 
                       font=("Arial", 1), 
                       bg_color="white"
                       )
    line.place(x=330,y=240)

    line_text = Tk.CTkLabel(framemiddle,
                            text="Balance",
                            font=("Arial", 25)
                            )
    line_text.place(x=390,y=210)
    
    line_summary = Tk.CTkLabel(framemiddle,
                               text="¥ {:}".format(values[2]), 
                               anchor="nw",
                               font=("Arial", 20)
                               )
    line_summary.place(x=405, y=250)

# pie chart -----------------------------------------------------
def pie_chart():
    values = pie_values()
    list_categories = values[0]
    list_values = values[1]

    explode = []
    for i in list_categories:
        explode.append(0.05)
    #calculate persantages
    total= sum(list_values)
    percentages = [f"{(value/total)*100:.1f}%" for value in list_values]
    # plot
    figure = plt.Figure(figsize=(5,5), dpi=60, facecolor=co4)
    ax = figure.add_subplot(111)
    ax.pie(list_values,
           labels=percentages,
           explode=explode,
           startangle=90,
           textprops={"color":"white"}
           )
    ax.legend(list_categories)
    
    canvas = FigureCanvasTkAgg(figure, master=framemiddle)
    canvas.get_tk_widget().place(x=800,y=50)

    text_color = 'white'
    # change colors of axis
    ax.tick_params(colors=text_color)

######################################### INSERT FUNCTIONS ##########################################

# insert category function -----------------------------------------------------
def insert_category_function():
    name = value_textbox2.get()
    
    if not name.strip():
        CTkMessagebox(title="ERROR", message="Category name cannot be empty")
        return
    
    # passing the list to the data    
    insert_categories(name)  

    CTkMessagebox.messagebox(title="Sucess", text="category inserted with success")

    value_textbox2.delete(0,"end")

    categories_optionbox.configure(values=see_categories())

# insert income function -----------------------------------------------------
def insert_income_function():
    name = "income"
    date = e_cal_income.get()
    amount = value_textbox3.get()

    
    if not all ([name, date, amount]):
        CTkMessagebox(title="ERROR", message="Category name cannot be empty")
        return
    
    insert_income(name,date,amount)

    CTkMessagebox.messagebox(title="Sucess", text="Income inserted with success")

    value_textbox3.delete(0,"end")

    # update all data
    show_expenses()
    percentage()
    bar_function()
    summary()
    pie_chart()

#insert expenses -------------------------------------------------------------------
def insert_expenses_function():
    name = categories_optionbox.get()
    date = e_cal_expenses.get()
    price = value_textbox.get()

    if not all ([name,date,price]):
        CTkMessagebox(title="ERROR", message="Category name cannot be empty")
        return
    
    insert_expenses(name, date, price)

    CTkMessagebox.messagebox(title="Sucess", text="Income inserted with success")

    value_textbox.delete(0,"end")

    show_expenses()
    percentage()
    bar_function()
    summary()
    pie_chart()

# table data function -------------------------------------------------------
def table():
    expenses = see_expenses()
    income = see_income()

    table_list = []

    for i in expenses:
        table_list.append(i)
    
    for i in income:
        table_list.append(i)

    return table_list

def bar_table():
    # income total -------------------------------------------------------
    income = see_income()
    income_list = []

    for i in income:
        income_list.append(i[3])

    total_income = sum(income_list)

    # expenses total -------------------------------------------------------
    expenses = see_expenses()
    expenses_list = []

    for i in expenses:
        expenses_list.append(i[3])

    total_expenses = sum(expenses_list)

    balance = total_income - total_expenses

    value_list = [total_income, total_expenses, balance]
    return value_list
    
def percentage_left():
    # income total -------------------------------------------------------
    total_expenses = 0

    income = see_income()
    income_list = []

    for i in income:
        income_list.append(i[3])

    total_income = sum(income_list)

    # expenses total -------------------------------------------------------
    expenses = see_expenses()
    expenses_list = []

    for i in expenses:
        expenses_list.append(i[3])

    total_expenses = sum(expenses_list)

    if total_income == 0:
        return 1
    
    value_list = ((total_income - total_expenses) / total_income)*100
    return value_list

def pie_values():
    expenses = see_expenses()
    table_list = []

    for i in expenses:
        table_list.append(i)

    dataframe = pd.DataFrame(table_list, columns= ['id', 'categories', 'Date', 'price'])
    dataframe = dataframe.groupby('categories')['price'].sum()

    list_quantities = dataframe.values.tolist()
    list_categories = []

    for i in dataframe.index:
        list_categories.append(i)

    return([list_categories, list_quantities])

######################################### DELETE FUNCTIONS  ##########################################

# delete function -----------------------------------------------------
def delete_data():
    try:
        treeview_data = tree.focus()
        treeview_dictionary = tree.item(treeview_data)
        treeview_list = treeview_dictionary["values"]
        id_values = treeview_list[0]
        category = treeview_list[1]

        if category == "income":
            delete_income([id_values])
            CTkMessagebox.messagebox(title="Sucess", text="Income deleted success")

            show_expenses()
            percentage()
            bar_function()
            summary()
            pie_chart()

        else:
            delete_expenses([id_values])
            CTkMessagebox.messagebox(title="Sucess", text="Expense deleted success")
    
            show_expenses()
            percentage()
            bar_function()
            summary()
            pie_chart()

    except IndexError:
        CTkMessagebox.messagebox(text="There was an error we couldn't delete the data")

######################################### SCREEN SETTINGS ##########################################

# screen frame division -----------------------------------------------------
frametop = Tk.CTkFrame(window,width=frame_width ,height=50, border_color=co1)
frametop.grid(row=0,column=0,padx=10,pady=5)

framemiddle = Tk.CTkFrame(window,width=frame_width ,height=360, border_color=co1)
framemiddle.grid(row=1,column=0,padx=10,pady=0, sticky="nsew")

framebottom = Tk.CTkFrame(window,width=frame_width ,height=370, border_color=co1)
framebottom.grid(row=2,column=0,padx=10,pady=5, sticky="nsew")

# Bottom frame division -----------------------------------------------------
frame_income = Tk.CTkFrame(framebottom, width=590, height=370)
frame_income.grid(row=0,column=0)

frame_operations = Tk.CTkFrame(framebottom, width=295, height=370)
frame_operations.grid(row=0,column=1,padx=3)

frame_insert = Tk.CTkFrame(framebottom, width=295, height=370)
frame_insert.grid(row=0,column=2)


# Opening Image for light and dark mode -----------------------------------------------------
app_image_light = Image.open("images/piggybank.png")
app_image_dark = Image.open("images/piggy_white.png")
app_image = Tk.CTkImage(
    light_image=app_image_light,
    dark_image=app_image_dark,
    size=(45,45))

# text below loading bar -----------------------------------------------------
app_logo = Tk.CTkLabel(frametop, 
                       image=app_image,
                       text="Personal Finance Tracker",
                       text_color="white",
                       compound="left",
                       anchor="nw",
                       padx=10,
                       pady=3,
                       font=("Minion Pro Med",16)
                       )
app_logo.place(x=0,y=0)

#text above income frame -----------------------------------------------------------
income_logo = Tk.CTkLabel(framemiddle, 
                       text="Expenses table",
                       text_color="white",
                       compound="left",
                       anchor="nw",
                       padx=10,
                       pady=3,
                       font=("Minion Pro Med",16)
                       )
income_logo.place(x=50,y=330)

# Expenses HEADER -----------------------------------------------------------------------
line_info = Tk.CTkLabel(frame_operations, 
                               text="Insert new expenses", 
                               height=1,
                               anchor="nw",
                               font=("Arial", 15)
                               )
line_info.place(x=85,y=10)

# ComboBox box  --------------------------------------------------------------------------------
line_categories = Tk.CTkLabel(frame_operations, 
                               text="Categories", 
                               height=1,
                               anchor="nw",
                               font=("Arial", 15)
                               )
line_categories.place(x=10,y=40)

categories_optionbox = Tk.CTkComboBox(frame_operations,
                                        values=see_categories(),
                                        width=100,
                                        height=20
                                        )
categories_optionbox.place(x=110, y=40)

# calender -----------------------------------------------------------------------------------
line_cal_expenses = Tk.CTkLabel(frame_operations, text="Date", height=1, anchor="nw", font=("Arial", 15))
line_cal_expenses.place(x=10, y=70)

e_cal_expenses = DateEntry(frame_operations, width=12, background="darkblue", foreground="black", borderwidth=2, year=2024)
e_cal_expenses.place(x=110,y=70)

# calender 2 -----------------------------------------------------------------------------------
line_cal_income = Tk.CTkLabel(frame_insert, text="Date", height=1, anchor="nw", font=("Arial", 15))
line_cal_income.place(x=10, y=40)

e_cal_income = DateEntry(frame_insert, width=12, background="darkblue", foreground="black", borderwidth=2, year=2024)
e_cal_income.place(x=110,y=40)

# Inser Values --------------------------------------------------------------------------------
line_value = Tk.CTkLabel(frame_operations, text="Price ¥", height=1, anchor="nw", font=("Arial", 15))
line_value.place(x=10, y=100)

value_textbox = Tk.CTkEntry(frame_operations,placeholder_text="Price", height=20, width=100)
value_textbox.place(x=110, y=100)

# Inser Values 2 --------------------------------------------------------------------------------
line_value2 = Tk.CTkLabel(frame_insert, text="categories", height=1, anchor="nw", font=("Arial", 15))
line_value2.place(x=10, y=230)

value_textbox2 = Tk.CTkEntry(frame_insert ,placeholder_text="Categories", height=20, width=100)
value_textbox2.place(x=110, y=230)

# Inser Values 3 --------------------------------------------------------------------------------
line_value3 = Tk.CTkLabel(frame_insert, text="Income", height=1, anchor="nw", font=("Arial", 15))
line_value3.place(x=10, y=70)

value_textbox3 = Tk.CTkEntry(frame_insert,placeholder_text="Price", height=20, width=100)
value_textbox3.place(x=110, y=70)

# Add button and delete button --------------------------------------------------------------
button_add_right = Tk.CTkButton(frame_operations, text="add", height=30, width=100, fg_color="green",command=insert_expenses_function)
button_add_right.place(x=110, y=160)

button_delete_right = Tk.CTkButton(frame_operations,command=delete_data, text="remove", height=30, width=100,fg_color="red")
button_delete_right.place(x=110, y=240)
# Add button more of them --------------------------------------------------------------

button_add_left_top = Tk.CTkButton(frame_insert, text="add", height=30, width=100, fg_color="green", 
                                   command=insert_income_function)
button_add_left_top.place(x=110, y=160)

button_add_left_bot = Tk.CTkButton(frame_insert, text="add", height=30, width=100, fg_color="green",
                               command=insert_category_function)
button_add_left_bot.place(x=110, y=320)




# run functions -----------------------------------------------------
insert_category_function
bar_function()
summary()
percentage()
pie_chart()
show_expenses()

window.mainloop()

        