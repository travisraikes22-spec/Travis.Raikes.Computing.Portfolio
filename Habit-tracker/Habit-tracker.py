import sqlite3
from datetime import date, timedelta

DB="habits.db"

def db():
    c=sqlite3.connect(DB)
    c.execute("CREATE TABLE IF NOT EXISTS habits(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT UNIQUE NOT NULL)")
    c.execute("""CREATE TABLE IF NOT EXISTS completions(
        habit_id INTEGER, completed_on TEXT, PRIMARY KEY(habit_id,completed_on),
        FOREIGN KEY(habit_id) REFERENCES habits(id))""")
    return c

def habits():
    c=db(); rows=c.execute("SELECT id,name FROM habits ORDER BY name").fetchall(); c.close()
    return rows

def add():
    name=input("Habit name: ").strip()
    if not name:return
    c=db()
    try:c.execute("INSERT INTO habits(name) VALUES(?)",(name,)); c.commit(); print("Added.")
    except sqlite3.IntegrityError:print("That habit already exists.")
    c.close()

def complete():
    rows=habits()
    if not rows: print("Create a habit first."); return
    for i,n in rows: print(i,n)
    try:i=int(input("Habit ID: "))
    except ValueError:return
    c=db()
    try:c.execute("INSERT INTO completions VALUES(?,?)",(i,str(date.today()))); c.commit(); print("Completed for today.")
    except sqlite3.IntegrityError:print("Already completed today.")
    c.close()

def streak(hid):
    c=db(); days={r[0] for r in c.execute("SELECT completed_on FROM completions WHERE habit_id=?",(hid,))}
    c.close()
    today=date.today(); current=0; d=today
    while str(d) in days:
        current+=1; d-=timedelta(days=1)
    best=0; run=0; d=today
    # Count consecutive runs over all recorded dates.
    for s in sorted(days):
        cur=date.fromisoformat(s)
        if run==0: run=1
        elif cur-prev==timedelta(days=1): run+=1
        else: run=1
        best=max(best,run); prev=cur
    return current,best

def show():
    rows=habits()
    if not rows: print("No habits."); return
    for i,n in rows:
        cur,best=streak(i); print(f"{i}. {n} â current: {cur} days | best: {best} days")

def remove():
    rows=habits()
    for i,n in rows:print(i,n)
    try:i=int(input("Habit ID to remove: "))
    except ValueError:return
    c=db(); c.execute("DELETE FROM completions WHERE habit_id=?",(i,)); c.execute("DELETE FROM habits WHERE id=?",(i,)); c.commit(); c.close(); print("Removed.")

def main():
    while True:
        print("\nHABIT TRACKER\n1 Add habit\n2 Complete today\n3 View streaks\n4 Remove\n0 Exit")
        x=input("> ")
        if x=="1":add()
        elif x=="2":complete()
        elif x=="3":show()
        elif x=="4":remove()
        elif x=="0":break

if __name__=="__main__":main()