import sqlite3

def init_db():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    create_user_table = 'CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username TEXT, password TEXT)'
    cursor.execute(create_user_table)
    create_item_table = 'CREATE TABLE IF NOT EXISTS item (id INTEGER PRIMARY KEY, name TEXT, price FLOAT)'
    cursor.execute(create_item_table)
    connection.commit()
    connection.close()
