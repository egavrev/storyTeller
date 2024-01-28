import streamlit as st
import sqlite3
import requests
from openai import OpenAI
from PIL import Image,ImageDraw, ImageFont
from io import BytesIO
import os
import json
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
    

def update_image(image_data, text_upper, text_lower):
  
    image = Image.open(BytesIO(save_image_from_url(image_data)))
    border = 50  # Thickness of the border/frame
    new_width = image.width + border * 2
    new_height = image.height + border * 2

    # Create a new image with the increased dimensions.
    # The frame color will fill this new image.
    frame_color = (255, 255, 255)  # Using white as the frame color for the example.
    new_image = Image.new("RGB", (new_width, new_height), frame_color)

    # Paste the original image onto the center of the new image.
    new_image.paste(image, (border, border))

    # Prepare to write text on the image.
    draw = ImageDraw.Draw(new_image)
    # Define the text properties.
    font = ImageFont.truetype("Chalkduster.ttf", 85)   # Adjust the font size as needed.
    # Calculate the position for the text to be centered on the border.
    text_x = 55
    text_y = 20
    # Choose a text color that contrasts the frame color.
    text_color = (0, 0, 255)  # Black color for the text.
    # Write the text onto the image.
    draw.text((text_x, text_y), text_upper, fill=text_color, font=font)


    font = ImageFont.truetype("Chalkduster.ttf", 75)   # Adjust the font size as needed.
    # Calculate the position for the text to be centered on the border.
    text_x = image.width - image.width/2
    text_y = image.height - 25
    # Choose a text color that contrasts the frame color.
    text_color = (255, 0, 0)  # Black color for the text.
    # Write the text onto the image.
    draw.text((text_x, text_y), text_lower, fill=text_color, font=font)

    img_byte_arr = BytesIO()
    new_image.save(img_byte_arr, format='JPEG')  # Save the image as JPEG into the BytesIO object
    # Get the binary representation of the image
    img_binary = img_byte_arr.getvalue()

    return  img_binary
    
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
    messages = [{"role": "user", "content": f"""Given that the topic is {topic} and the setting is {setting}, here's a backstory: {backstory}. Following strict JSON format to be used: 
              {{"Sotry_name" : "Story Name - in 2-5 words maximum", "Title_image" : "Description of tile image in 2-3 phrases maximum", "Story_body": "The story itself in 2-5 paragraphs"}}."""}]
    response = client.chat.completions.create(model="gpt-4", messages=messages)
    data_dict = json.loads(response.choices[0].message.content,strict=False)
    # Extract the parts you want
    story_name = data_dict['Story_name']
    title_image = data_dict['Title_image']
    story_body = data_dict['Story_body']
    
    
    return story_name,title_image,story_body


def image_generation(story):
    response = client.images.generate(
            model="dall-e-3",
            quality="hd",
            prompt = f"generate title image for the sotry {story}, draw it as cartoon for little kids - 3 years",
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
    backstory = st.text_area('Enter a backstory for your story:', value="""The story is about how a little boy named Maxim and his dad help their friends. 
                             They have a fun and adventurous transformer robot friend named Bumblebee, a strict but kind Optimus, 
                             and a garbage truck named Albert who loves to work and clean up everything.""", height=150)

    if st.button('Generate Story'):
        story_name,title_image,story_body = generate_story(topic, setting, backstory)
        
        image_url= image_generation(title_image)
        st.markdown(f"# {story_name}")
        

        st.image(update_image(image_url,story_name, "for Maxim"), caption=f"Generated image for sotry",
                         use_column_width=True)
        st.text_area('Your Story:', story_body, height=550)

    """ with st.sidebar:
        st.header('Generated Stories')
        for story_id, story_topic, story_setting, story_content, story_date in saved_stories:
            st.subheader(f"Story ID: {story_id}")
            st.write(f"Topic: {story_topic}")
            st.write(f"Setting: {story_setting}")
            st.write(f"Created at: {story_date}")
            if st.button(f"Show Story {story_id}"):
                st.text_area(f"Story {story_id}:", story_content, height=250)
    """


    

    #if st.button('Generate Image'):
    #    story = generate_story(topic, setting, backstory)
    #    st.text_area('Your Story:', story, height=250)

if __name__ == '__main__':
    app()