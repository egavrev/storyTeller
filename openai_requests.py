import requests
from openai import OpenAI
import os
import json



API_KEY= os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=API_KEY)

if 'OPENAI_API_KEY' not in os.environ:
        st.error('OpenAI API key not found. Please set it as an environment variable.')
        st.stop()

def generate_story(topic, setting,backstory, kid_name, kid_age, lang):
    messages = [{"role": "user", "content": f"""You are great story teller, write a story for for kids of {kid_age} age and name {kid_name}, story and title should be in {lang} language, given that the topic is {topic} and the setting is {setting}, here's a backstory: {backstory}. Following strict JSON format to be used: 
              {{"Story_name" : "Story Name - in 1-2 words maximum", "Title_image" : "Description of tile image in 2-3 phrases maximum", "Story_body": "The story itself in 2-5 paragraphs"}}."""}]
    response = client.chat.completions.create(model="gpt-4", messages=messages)
    data_dict = json.loads(response.choices[0].message.content,strict=False)
    story_name = data_dict['Story_name']
    title_image = data_dict['Title_image']
    story_body = data_dict['Story_body']
    
    
    return story_name,title_image,story_body


def image_generation(story, image_type,kid_age):
    response = client.images.generate(
            model="dall-e-3",
            quality="hd",
            prompt = f"generate title image for the story {story}, draw it as {image_type} for kids of {kid_age} age ",
            n = 1,
            size="1024x1024")
    print (response.data[0].url)
    return response.data[0].url