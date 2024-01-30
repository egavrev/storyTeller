import sqlite3

def create_database():
    connection = sqlite3.connect('story_database.db')
    cursor = connection.cursor()

    # Creating the 'topics' table
    cursor.execute('''DROP TABLE IF EXISTS topics''')
    cursor.execute('''CREATE TABLE topics (
                      id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL)''')

    # Creating the 'settings' table
    cursor.execute('''DROP TABLE IF EXISTS settings''')
    cursor.execute('''CREATE TABLE settings (
                      id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL)''')
  
    cursor.execute('''CREATE TABLE IF NOT EXISTS stories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        topic TEXT NOT NULL,
                        setting TEXT NOT NULL,
                        backstory TEXT NOT NULL,
                        story_body TEXT NOT NULL,
                        story_name TEXT NOT NULL,
                        image mage BLOB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')

    # Inserting some predefined topics and settings
    """
    add elements to the topics and settings tables
    1. Custom
    2. Honesty & Integrity
    3. Good Behavior & Respect
    4. Patience & Tolerance
    5. Healthy Lifestyle
    6. Care for Environment
    7. Diversity & Inclusion
    8. Internet Safety
    9. Peer Pressure
    10. Financial Literacy
    11. Entrepreneurship
    """
    topics = [('Honesty & Integrity',), ('Good Behavior & Respect',), ('Patience & Tolerance',), ('Healthy Lifestyle',), ('Care for Environment',), ('Diversity & Inclusion',), ('Internet Safety',), ('Peer Pressure',), ('Financial Literacy',), ('Entrepreneurship',)]
    
    """
    add elements to the settings table
    Custom
    School of Magic
    Cubic Game Universe
    Space Tales
    Magic Kingdom
    Superhero Metropolis
    Time Travel Adventures
    Robot City
    Pirate Seas
    Alive Toys
    Gamer Universe
    """
    settings = [('School of Magic',), ('Cubic Game Universe',), ('Space Tales',), ('Magic Kingdom',), ('Superhero Metropolis',), ('Time Travel Adventures',), ('Robot City',), ('Pirate Seas',), ('Alive Toys',), ('Gamer Universe',)]
    


    cursor.executemany('INSERT INTO topics (name) VALUES (?)', topics)
    cursor.executemany('INSERT INTO settings (name) VALUES (?)', settings)

    connection.commit()
    connection.close()
    

if __name__ == '__main__':
    create_database()