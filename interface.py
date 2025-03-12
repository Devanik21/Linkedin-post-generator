import streamlit as st
from google import genai

# Define options
titles = ["Career", "Technology", "Business", "Leadership", "Marketing"]
lengths = ["Short", "Medium", "Long"]
languages = ["English", "Hinglish", "Spanish"]

length_dict = {
    "Short": "less than 100 words",
    "Medium": "between 100 and 200 words",
    "Long": "more than 200 words"
}

language_dict = {
    "English": "English",
    "Hinglish": "a mix of Hindi and English",
    "Spanish": "Spanish"
}

# Set up client
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# UI
st.title("LinkedIn Post Generator")

title = st.selectbox("Title", titles)
length = st.selectbox("Length", lengths)
language = st.selectbox("Language", languages)

if st.button("Generate"):
    try:
        prompt = f"Generate a LinkedIn post about {title} in {language_dict[language]}. The post should be {length} in length, which is {length_dict[length]}. Ensure that the post is professional, insightful, and suitable for a LinkedIn audience."
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        st.write(response.text)
    except Exception as e:
        st.error(f"An error occurred: {e}")
