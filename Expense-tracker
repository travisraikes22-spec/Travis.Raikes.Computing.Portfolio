import sqlite3
import csv
from datetime import date

DB = "expenses.db"

def connect():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        spent_on TEXT NOT NULL
    )""")
    return conn

def add_expense():
    try:
        amount = float(input("Amount (£): "))
        if amount <= 0: raise ValueError
    except ValueError:
        print("Enter a valid positive amount."); return
    category = input("Category: ").strip() or "Other"
    description = input("Description: ").strip()
    spent_on = input(f"Date [{date.today()}]: ").strip() or str(date.today())
    conn = connect()
    conn.execute("INSERT INTO expenses(amount,category,description,spent_on) VALUES(?,?,?,?)",
                 (amount, category, description, spent_on))
    conn.commit(); conn.close()
    print("Expense added.")

def list_expenses():
    conn = connect()
    rows = conn.execute("SELECT id,amount,category,description,spent_on FROM expenses ORDER BY spent_on DESC,id DESC").fetchall()
    conn.close()
    if not rows: print("No expenses yet."); return
    print(f"\n{'ID':<4}{'Amount':>10}  {'Category':<15}{'Date':<12}Description")
    print("-"*70)
    for i,a,c,d,dt in rows:
        print(f"{i:<4}£{a:>8.2f}  {c:<15}{dt:<12}{d or ''}")

def summary():
    month = input("Month (YYYY-MM, blank for all): ").strip()
    conn = connect()
    if month:
        rows = conn.execute("""SELECT category,SUM(amount) FROM expenses
                               WHERE substr(spent_on,1,7)=? GROUP BY category ORDER BY SUM(amount) DESC""",(month,)).fetchall()
    else:
        rows = conn.execute("SELECT category,SUM(amount) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC").fetchall()
    conn.close()
    print("\nSpending summary")
    print("-"*30)
    total = 0
    for category, amount in rows:
        print(f"{category:<18} £{amount:>8.2f}")
        total += amount
    print("-"*30); print(f"{'TOTAL':<18} £{total:>8.2f}")

def delete_expense():
    try: i = int(input("Expense ID: "))
    except ValueError: print("Invalid ID."); return
    conn = connect()
    cur = conn.execute("DELETE FROM expenses WHERE id=?", (i,))
    conn.commit(); conn.close()
    print("Deleted." if cur.rowcount else "ID not found.")

def export_csv():
    conn = connect()
    rows = conn.execute("SELECT id,amount,category,description,spent_on FROM expenses").fetchall()
    conn.close()
    with open("expenses_export.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["id","amount","category","description","spent_on"]); w.writerows(rows)
    print("Exported to expenses_export.csv")

def main():
    while True:
        print("\nEXPENSE TRACKER\n1 Add\n2 List\n3 Summary\n4 Delete\n5 Export CSV\n0 Exit")
        choice=input("> ").strip()
        if choice=="1": add_expense()
        elif choice=="2": list_expenses()
        elif choice=="3": summary()
        elif choice=="4": delete_expense()
        elif choice=="5": export_csv()
        elif choice=="0": break
        else: print("Choose a menu option.")

if __name__=="__main__": main()
