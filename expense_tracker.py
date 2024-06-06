import sqlite3
import datetime
import streamlit as st


conn = sqlite3.connect("expenses.db")
cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    date TEXT,
    description TEXT,
    category TEXT,
    price REAL
)
""")
conn.commit()


def get_categories():
    cur.execute("SELECT DISTINCT category FROM expenses")
    return [row[0] for row in cur.fetchall()]


def add_expense(date, description, category, price):
    cur.execute("INSERT INTO expenses (date, description, category, price) VALUES (?, ?, ?, ?)", (date, description, category, price))
    conn.commit()


def get_all_expenses():
    cur.execute("SELECT * FROM expenses")
    return cur.fetchall()


def get_monthly_expenses(month, year):
    cur.execute("SELECT category, SUM(price) FROM expenses WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ? GROUP BY category", (month, year))
    return cur.fetchall()


st.title("Expense Tracker")

menu = ["Enter a new expense", "View expenses summary"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Enter a new expense":
    st.subheader("Enter a new expense")

    date = st.date_input("Date of the expense", datetime.date.today())
    description = st.text_input("Description of the expense")
    categories = get_categories()

    category = st.selectbox("Category", categories + ["Create a new category"])

    if category == "Create a new category":
        category = st.text_input("Enter the new category name")

    price = st.number_input("Price of the expense", min_value=0.0, format="%.2f")

    if st.button("Add Expense"):
        add_expense(date, description, category, price)
        st.success("Expense added successfully!")

elif choice == "View expenses summary":
    st.subheader("View expenses summary")

    view_options = ["View all expenses", "View monthly expenses by category"]
    view_choice = st.selectbox("Options", view_options)

    if view_choice == "View all expenses":
        expenses = get_all_expenses()
        for exp in expenses:
            st.write(f"Date: {exp[1]}, Description: {exp[2]}, Category: {exp[3]}, Price: {exp[4]}")

    elif view_choice == "View monthly expenses by category":
        month = st.selectbox("Month", [str(i).zfill(2) for i in range(1, 13)])
        year = st.text_input("Year", datetime.date.today().year)

        if st.button("View Expenses"):
            expenses = get_monthly_expenses(month, year)
            for exp in expenses:
                st.write(f"Category: {exp[0]}, Total: {exp[1]}")

conn.close()
# import sqlite3
# import datetime

# conn = sqlite3.connect("expenses.db")
# cur = conn.cursor()

# while True:
#     print("Select an option: ")
#     print("1. Enter a new expenses")
#     print("2. View expenses summary")
    
#     choice = int(input())
    
#     if choice == 1:
#         date = input("Enter the date of the expense (YYYY-MM-DD): ")
#         descrption = input("Enter the descrption of the expense:")
        
#         cur.execute("SELECT DISTINCT category FROM expenses")
        
#         categories = cur.fetchall()
        
#         print("Select a category by number: ")
#         for i, category in enumerate (categories):
#             print(f"{i+1}. {category[0]}")
#         print(f"{len(categories)+1}. Create a new category")
        
#         category_choice = int(input())
#         if category_choice == len(categories)+1:
#             category = input("Enter the new category name: ")
#         else:
#             category = categories[category_choice - 1][0]
            
#         price = input("Enter the price of the expense")
#         cur.execute("INSERT INTO expenses (Date, description, category, price)VALUES(?,?,?,?)", (date, descrption, category, price))

#         conn. commit()
        
        
#     elif choice == 2:
#         print("Select an option:")
#         print("1. View all expenses")
#         print("2. View monthly expenses by category")
        
#         view_choice = int(input())
        
#         if view_choice == 1:
#             cur.execute("SELECT * FROM expenses")
#             expenses = cur.fetchall()
#             for exp in (expenses):
#                 print(exp)
#         elif view_choice == 2:
#             month = input("Enter the month (MM): ")
#             year = input("Enter the year (YYYY): ")
#             cur.execute("SELECT category, SUM(price) FROM expenses WHERE strftime('%m', Date)=? AND strftime('%Y', Date)=? GROUP BY category",(month,year))
#             expenses = cur.fetchall()
#             for expense in expenses:
#                 print(f"Category: {expense[0]}, Total:{expense[1]}")
#         else:
#             exit()
            
    
#     else:
#         exit()
#     repeat = input("Would you like to do something else (y/n)? \n")
#     if repeat.lower()!='y':
#         break
# conn.close()