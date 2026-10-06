import sqlite3

DB="inventory.db"

def db():
    c=sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 0,
        price REAL NOT NULL,
        reorder_level INTEGER NOT NULL DEFAULT 5
    )""")
    return c

def add():
    name=input("Product: ").strip()
    try:q=int(input("Starting quantity: ")); p=float(input("Unit price (£): ")); r=int(input("Low-stock level: "))
    except ValueError:print("Invalid number.");return
    c=db()
    try:c.execute("INSERT INTO products(name,quantity,price,reorder_level) VALUES(?,?,?,?)",(name,q,p,r));c.commit();print("Product added.")
    except sqlite3.IntegrityError:print("Product already exists.")
    c.close()

def list_products(where="", params=()):
    c=db(); rows=c.execute("SELECT id,name,quantity,price,reorder_level FROM products "+where,params).fetchall(); c.close()
    if not rows: print("No matching products."); return
    print(f"\n{'ID':<4}{'Product':<25}{'Qty':>6}{'Price':>10}{'Value':>12}{'Status':>12}")
    for i,n,q,p,r in rows:
        status="LOW" if q<=r else "OK"
        print(f"{i:<4}{n[:24]:<25}{q:>6}{'£'+format(p,'.2f'):>10}{'£'+format(q*p,'.2f'):>12}{status:>12}")

def change_stock():
    try:i=int(input("Product ID: ")); delta=int(input("Quantity change (+/-): "))
    except ValueError:return
    c=db(); c.execute("UPDATE products SET quantity=quantity+? WHERE id=? AND quantity+? >= 0",(delta,i,delta))
    c.commit(); print("Stock updated." if c.total_changes else "Invalid ID or insufficient stock."); c.close()

def search():
    term=input("Search: ").strip()
    list_products("WHERE name LIKE ?",("%"+term+"%",))

def value():
    c=db(); total=c.execute("SELECT COALESCE(SUM(quantity*price),0) FROM products").fetchone()[0]; c.close()
    print(f"Inventory value: £{total:.2f}")

def main():
    while True:
        print("\nINVENTORY MANAGER\n1 Add product\n2 List\n3 Change stock\n4 Search\n5 Total value\n6 Low-stock\n0 Exit")
        x=input("> ")
        if x=="1":add()
        elif x=="2":list_products()
        elif x=="3":change_stock()
        elif x=="4":search()
        elif x=="5":value()
        elif x=="6":list_products("WHERE quantity<=reorder_level")
        elif x=="0":break

if __name__=="__main__":main()