import streamlit as st
import sqlite3
from openai import OpenAI
from PIL import Image
import os
# Retrieve the OpenAI API key from environment variable
API_KEY= os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=API_KEY)


# Your OpenAI API key (Replace 'your_api_key_here' with your actual OpenAI API key)

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


    #if st.button('Generate Image'):
    #    story = generate_story(topic, setting, backstory)
    #    st.text_area('Your Story:', story, height=250)

if __name__ == '__main__':
    app()