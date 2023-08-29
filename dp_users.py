import sqlite3
import os

con = sqlite3.connect("users.db")
cursor = con.cursor()

try:
    cursor.execute("""CREATE TABLE users
                   (№ INTEGER PRIMARY KEY AUTOINCREMENT,
                   id INTEGER,
                   num TEXT,
                   true INTEGER)
               """)
except:
    pass