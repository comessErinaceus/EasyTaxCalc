import sqlite3
import sys
import json


TAX_BRACKET_DATABASE = './tax_brackets.db'
def create_database():
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tax_brackets (state INTEGER, lower REAL, upper REAL, rate REAL)''')

    conn.commit()
    conn.close()

def insert_tax_bracket(state, status, lower, upper, rate):
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO tax_brackets (state, status, lower, uppoer, rate) VALUES (?, ?, ?, ?, ?)", (state, status, lower, upper, rate))

    conn.commit()
    conn.close()

def list_tax_brackets():
    
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    c = conn.cursor()

    for row in c.execute("SELECT * FROM tax_brackets"):
        print(row)
    conn.close()


# create States table
def create_states_table():
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS states (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

# populate the states table
def populate_states_table(json_data):
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    c = conn.cursor()


    states = json.loads(json_data)
    
    # Insert the json data Of each state into the states table
    for state in states['states']:
        c.execute('''INSERT INTO states 
            (name) VALUES (?)''', 
            (state,))

    conn.commit()
    conn.close()

def get_satate_id(state_name):
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM state WHERE name =?', (state_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        raise ValueError(f"State '{state_name}' not found in the database")

# populate the db with state tax rates
def populate_states_table(json_data, status):
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    c = conn.cursor()

    state_brackets = json.loads(json_data)

    # Loop the Json Data inserting a record for each bracket
    for state_name, brackets in state_brackets.items():

        state_id = get_satate_id(state_name)
        for bracket in brackets:
            c.exectue(''' 
            INSERT INTO tax_brackets (state, status, lower, upper, rate)
            VALUES(?,?,?,?)
            ''', (state_id, status, bracket['lower'], bracket['upper'], bracket['rate']))
            #insert_tax_bracket(state_id, bracket['lower'], bracket['upper'], bracket['rate'])
    
    conn.commit()
    conn.close()



# populate the db with federal tax rates