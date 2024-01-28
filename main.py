import streamlit as st
import sqlite3
import requests
from openai import OpenAI
from PIL import Image
import os
# Retrieve the OpenAI API key from environment variable
API_KEY= os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=API_KEY)


# Your OpenAI API key (Replace 'your_api_key_here' with your actual OpenAI API key)

def save_image_from_url(url):
    # Fetch the image from the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Return the binary content of the image
        return response.content
    else:
        raise Exception("Failed to fetch image from URL")

def save_story(topic, setting, backstory, story_name, story, image_url):
    # Generate the image and get the URL
    image_data = save_image_from_url(image_url)
    
    # Establish a connection to the SQLite database
    connection = sqlite3.connect('story_database.db')
    cursor = connection.cursor()
    
    # SQL query to insert the new story and image data into the stories table
    cursor.execute('INSERT INTO stories (topic, setting, backstory, story_name, story, image_data) VALUES (?, ?, ?, ?, ?, ?)',
                   (topic, setting, backstory, story_name, story, sqlite3.Binary(image_data)))
    
    # Commit the changes to the database
    connection.commit()
    
    # Close the database connection
    connection.close()

def fetch_topics_settings():
    connection = sqlite3.connect('story_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT name FROM topics')
    topics = cursor.fetchall()

    cursor.execute('SELECT name FROM settings')
    settings = cursor.fetchall()

    connection.close()

    return topics, settings

def generate_story(topic, setting,backstory):
    messages = [{"role": "user", "content": f"Given that the topic is {topic} and the setting is {setting}, here's a backstory: {backstory}. Now, based on that, generate a story."}]
    response = client.chat.completions.create(model="gpt-4", messages=messages)
    return response.choices[0].message.content


def image_generation(story):
    response = client.images.generate(
            model="dall-e-3",
            quality="hd",
            prompt = f"generate title image for the sotry {story}",
            n = 1,
            size="1024x1024")
    return response.data[0].url
          
                

def app():
    st.title('Story Generator for Kids')

    if 'OPENAI_API_KEY' not in os.environ:
        st.error('OpenAI API key not found. Please set it as an environment variable.')
        st.stop()
    

    topics, settings = fetch_topics_settings()

    topic = st.selectbox('Choose a topic:', [t[0] for t in topics])
    setting = st.selectbox('Choose a setting:', [s[0] for s in settings])
    backstory = st.text_area('Enter a backstory for your story:', value="""type here""", height=150)

    if st.button('Generate Story'):
        story = generate_story(topic, setting, backstory)
        st.text_area('Your Story:', story, height=250)
        image_url= image_generation(story)
        print(image_url)
        st.image(image_url, caption=f"Generated image for sotry",
                         use_column_width=True)
    with st.sidebar:
        st.header('Generated Stories')
        saved_stories = get_saved_stories()
        for story_id, story_topic, story_setting, story_content, story_date in saved_stories:
            st.subheader(f"Story ID: {story_id}")
            st.write(f"Topic: {story_topic}")
            st.write(f"Setting: {story_setting}")
            st.write(f"Created at: {story_date}")
            if st.button(f"Show Story {story_id}"):
                st.text_area(f"Story {story_id}:", story_content, height=250)



    

    #if st.button('Generate Image'):
    #    story = generate_story(topic, setting, backstory)
    #    st.text_area('Your Story:', story, height=250)

if __name__ == '__main__':
    app()