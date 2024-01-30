import sqlite3

def load_storeis():
    connection = sqlite3.connect('story_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM stories')
    stories = cursor.fetchall()

    connection.close()

    return stories

def fetch_topics_settings():
    connection = sqlite3.connect('story_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT name FROM topics')
    topics = cursor.fetchall()

    cursor.execute('SELECT name FROM settings')
    settings = cursor.fetchall()

    connection.close()

    return topics, settings


def save_story(topic, setting, backstory, story_name, story, image_data):
    # Generate the image and get the URL
    # Establish a connection to the SQLite database
    connection = sqlite3.connect('story_database.db')
    cursor = connection.cursor()    
    # SQL query to insert the new story and image data into the stories table
    cursor.execute('INSERT INTO stories (topic, setting, backstory, story_name, story_body, image) VALUES (?, ?, ?, ?, ?, ?)',
                   (topic, setting, backstory, story_name, story, sqlite3.Binary(image_data)))
    
    # Commit the changes to the database
    connection.commit()
    
    # Close the database connection
    connection.close()