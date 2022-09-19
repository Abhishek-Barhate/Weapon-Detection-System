import sqlite3
conn = sqlite3.connect('wds_db')
curs = conn.cursor()
curs.execute('create table uid (username char(50), email char(50), password char(50))')
