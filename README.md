# Story Generator for Kids
This is a Streamlit web application that generates stories for kids. 

## Prerequisites
Before you begin, ensure you have met the following requirements:
* You have installed Python 3.6 or later.
* You have installed Streamlit. If not, install it using pip:
    pip install streamlit
* You have set the `OPENAI_API_KEY` environment variable with your OpenAI API key.

## Configuring Story Generator for Kids
To configure Story Generator for Kids, follow these steps:
1. Clone the repository:
2. Navigate to the project directory:

## Running Story Generator for Kids

To run Story Generator for Kids, follow these steps:
1. Run the Streamlit application: streamlit run main.py
2. Open your web browser and go to `http://localhost:8501` to view the application.



# Versions 
## v.0.1
- [X] generate title of story - 2 3 words, image_prompt and story itself. 
- [X] parse story data to get story name, prompt and story
- [X] generate request data to DALL_E for image
- [X] save all information to database 
- [X] function to get a story information from data base
## v.0.2
- [X] save personalized image file with frame title name and signature for Max. 
- [X] make an form with dropdown list and button to click to show data. 
- [X] display story content in specific area. 
## v.0.3
- [X] provide generic setting: type of image - cartoon, realistic; name and age of kid, add setting and backstory.
- [ ] option to select an langue to which story might be translated
- [X] rebuild project structure add util.py and request.py for utility and working with sqldb functions 
### v.0.4
- [ ] add different language support
- [ ] when story title it is the same name as existing add index.
- [ ] split main file in two - side bar and main content