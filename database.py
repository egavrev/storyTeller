import sqlite3

def create_database():
    connection = sqlite3.connect('story_database.db')
    cursor = connection.cursor()

    # Creating the 'topics' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS topics (
                      id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL)''')

    # Creating the 'settings' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                      id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL)''')

    # Inserting some predefined topics and settings
    topics = [('honesty',), ('bravery',), ('friendship',)]
    settings = [('robo-city',), ('jungle',), ('ancient temple',)]

    cursor.executemany('INSERT INTO topics (name) VALUES (?)', topics)
    cursor.executemany('INSERT INTO settings (name) VALUES (?)', settings)

    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_database()