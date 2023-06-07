import sqlite3

conn = sqlite3.connect('chattest.db')
c = conn.cursor()
c.execute("delete from chatmess")
c.execute("delete from chat")
c.execute("delete from user where name='あなた'")
conn.commit()
conn.close()
