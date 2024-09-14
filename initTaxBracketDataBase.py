import sqlite3
import sys
import json


TAX_BRACKET_DATABASE = './tax_brackets.db'
def create_database():
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tax_brackets (state INTEGER, status INTEGER, lower INTEGER, upper INTEGER, rate INTEGER)''')

    conn.commit()
    conn.close()
    return True

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
    return True

def create_file_status_table():
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS file_status (id INTEGER PRIMARY KEY AUTOINCREMENT, status TEXT)''')

    conn.commit()
    conn.close()
    return True

def populate_file_status():
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    c = conn.cursor()
    file_statuses = ['single', 'married_separate', 'married_joint', 'head_of_household']
    
    for a in file_statuses:
        c.execute("INSERT INTO file_status(status) VALUES (?)", (a,))

    conn.commit()
    conn.close()

def insert_tax_bracket(state, status, lower, upper, rate):
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO tax_brackets (state, status, lower, upper, rate) VALUES (?, ?, ?, ?, ?)", (state, status, lower, upper, rate))

    conn.commit()
    conn.close()

def list_tax_brackets():
    
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    c = conn.cursor()

    for row in c.execute("SELECT * FROM tax_brackets"):
        print(row)
    conn.close()

# populate the states table
def populate_states_table(json_data):
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    c = conn.cursor()

    with open(json_data, 'r') as data:
        states = json.load(data)
    
    # Insert the json data Of each state into the states table
    for state in states['states']:
        c.execute('''INSERT INTO states 
            (name) VALUES (?)''', 
            (state,))

    conn.commit()
    conn.close()

def get_state_id(state_name):
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM states WHERE name =?', (state_name,))
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    if result:
        return result[0]
    else:
        raise ValueError(f"State '{state_name}' not found in the database")
    
def get_status_id(status_name):
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM file_status WHERE status =?', (status_name,))
    result = cursor.fetchone()
    # print("Result: ", result)
    conn.commit()
    conn.close()
    if result:
        return result[0]
    else:
        raise ValueError(f"State '{status_name}' not found in the database")

# populate the db with state tax rates
def populate_tax_brackets_table(json_data, status):
    conn = sqlite3.connect(TAX_BRACKET_DATABASE)
    cursor = conn.cursor()


    s = get_status_id(status)
    with open(json_data, 'r') as data:
        state_brackets = json.load(data)

    # Loop the Json Data inserting a record for each bracket
    for state_name, brackets in state_brackets.items():

        state_id = get_state_id(state_name)
        for bracket in brackets:
            cursor.execute(''' 
            INSERT INTO tax_brackets (state, status, lower, upper, rate)
            VALUES(?,?,?,?,?)
            ''', (state_id, s, bracket['lower'], bracket['upper'], bracket['rate']))
            #insert_tax_bracket(state_id, bracket['lower'], bracket['upper'], bracket['rate'])
    
    conn.commit()
    conn.close()

def init_database():
    print("Creating Database\n")
    if create_database():

        print("Creating States Table")
        if create_states_table():
            populate_states_table('states.json')
        if create_file_status_table():
            populate_file_status()

        print("populating Data")
        
        populate_tax_brackets_table('state_taxes.json', 'single')


# populate the db with federal tax rates


def main():
    init_database()


if __name__ == '__main__':
    main()