import sqlite3

CONN = sqlite3.connect("db/dogs.db")
CURSOR = CONN.cursor()
