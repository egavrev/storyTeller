import streamlit as st
from db_func import load_storeis, fetch_topics_settings, save_story
from openai_requests import generate_story, image_generation
from utils import update_image   

def app():
    st.title('Story Generator for Kids  - open or generate new story')
    topics, settings = fetch_topics_settings()        
        
    story_name,title_image,story_body = None, None, None
        #load all stories from history / for future maybe to load on topics or last 20-30
    saved_stories=load_storeis()
    with st.sidebar:
        with st.expander("Open Stories"):
            form = st.form(key='my_form')
            selected_topic = form.selectbox('Story name:', [(t[0], t[5]) for t in saved_stories], format_func=lambda x: x[1], placeholder='Select a story')
            button_form = form.form_submit_button(label='Open story')        
       
       

        with st.expander("Generate Stories"):
            topic = st.selectbox('Choose a topic:', [t[0] for t in topics])
            setting = st.selectbox('Choose a setting:', [s[0] for s in settings])
            backstory = st.text_area('Enter a backstory for your story:', value="""The story is about how a little boy named Maxim and his dad help their friends. 
                                    They have a fun and adventurous transformer robot friend named Bumblebee, a strict but kind Optimus, 
                                    and a garbage truck named Albert who loves to work and clean up everything.""", height=150)
            lang = st.selectbox('Choose a language:', ['English', 'Romanian', 'Russian'])
            kid_name = st.text_input('Enter a name for your kid:', value='Maxim', max_chars=20)
            kid_age = st.number_input('Enter an age for your kid:', value=5, min_value=1, max_value=12, step=1)
            image_type = st.selectbox('Choose an image type:', ['photorealistic', 'illustration', 'cartoon'])
            if st.button('Generate Story'):
                story_name,title_image,story_body = generate_story(topic, setting, backstory, kid_name, kid_age, lang)
                
                image_url= image_generation(title_image,image_type,kid_age)
                img = update_image(image_url,story_name, f"for {kid_name}")
                save_story(topic,setting,backstory,story_name,story_body,img)
    container = st.container(border=True)
    if (story_name != None) and (title_image != None) and (story_body != None):
        
        container.image( img,caption=f"Generated image for story",use_column_width=True)
        container.text_area('Your Story:', story_body, height=550,key="story_content")


        

    if button_form:
            story_id, topic = selected_topic
            for story in saved_stories:
                if story[0] == story_id:
                    container.image(story[6],caption=f"Generated image for story",use_column_width=True)
                    container.text_area('Your Story:', story[4], height=550,key="story_content")
                    break

                
if __name__ == '__main__':
    app()