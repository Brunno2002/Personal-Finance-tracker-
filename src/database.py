import sqlite3

# make connection -------------------------------------------------------------
con = sqlite3.connect("data/finance.db")


# create category functions -------------------------------------------------------------
def create_categories():
    with con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT
                    )""")
        
def insert_categories(name):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO categories (name) VALUES (?)",(name,))


def see_categories():
    with con:
        cur = con.cursor()
        cur.execute("SELECT name FROM categories")
        categories = [item[0] for item in cur.fetchall()]
        return categories


# create income functions -------------------------------------------------------------
def create_income():
    with con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS income (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    categories TEXT,
                    added_date DATE,
                    income_value DECIMAL
                    )""")

def insert_income(added_categories, added_date, added_income):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO income(categories, added_date, income_value) VALUES (?, ?, ?)",(added_categories, added_date, added_income))
        
def see_income():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM income")
        income_record = cur.fetchall()
        return income_record
        
def delete_income(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM income WHERE id=?"
        cur.execute(query, i)

# create expenses functions --------------------------------------------------------------------------
def create_expenses():
    with con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    categories TEXT,
                    added_date DATE,
                    price DECIMAL
                    )""")

def insert_expenses(added_categories, added_date, added_price):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO expenses (categories, added_date, price) VALUES (?, ?, ?)",(added_categories, added_date, added_price))

def see_expenses():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM expenses")
        income_record = cur.fetchall()
        return income_record

def delete_expenses(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM expenses WHERE id=?"
        cur.execute(query, i)





    

