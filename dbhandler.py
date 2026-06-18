import sqlite3
conobj=sqlite3.connect(database='bank.sqlite')
curobj=conobj.cursor()
query='''create table if not exists users(
acn integer primary key autoincrement,
name text,
pass text,
email text,
mob text,
adhar text,
age int,
bal float,
gender text,
opendate text
)
'''

curobj.execute(query)
conobj.close()
print("Table managed")