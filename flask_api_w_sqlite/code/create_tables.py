import sqlite3

def init_db():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    create_table = 'CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username TEXT, password TEXT)'
    cursor.execute(create_table)

    connection.commit()
    connection.close()
