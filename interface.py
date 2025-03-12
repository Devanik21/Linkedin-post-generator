import streamlit as st
import google.generativeai as genai

# Configure the Streamlit page
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="💼",
    layout="wide",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background-color: #6b0f87;
        }
        .stTextInput>div>div>input, .stSelectbox>div>div {
            background-color: #600e78;
            border-radius: 10px;
            padding: 8px;
            font-weight: bold;
        }
        .stButton>button {
            background: linear-gradient(to right, #12c2e9, #e7e6e8, #3000b3);
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for API Key
with st.sidebar:
    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input("Enter Google Gemini API Key:", type="password")

# Page Header
st.title("🚀 LinkedIn Post Generator")
st.write("Generate engaging LinkedIn posts effortlessly with AI!")

# Input fields
title = st.selectbox("📌 Select a Topic:", ["Career", "Networking", "Leadership", "Productivity"])
length = st.selectbox("📏 Select Length:", ["Short", "Medium", "Long"])
language = st.selectbox("🌍 Select Language:", ["English", "Hinglish", "Hindi", "Spanish"])

# Generate button
if st.button("🎯 Generate Post"):
    if not api_key:
        st.warning("⚠️ Please enter a valid Google Gemini API Key in the sidebar.")
    else:
        try:
            # Configure API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash")

            # Create a prompt for AI
            prompt = f"Generate a {length.lower()} LinkedIn post in {language} about {title} with a professional and engaging tone."

            # Generate response
            with st.spinner("🔄 Generating your LinkedIn post..."):
                response = model.generate_content(prompt)

            # Display result
            st.success("✅ Generated LinkedIn Post:")
            st.write(response.text)

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("If you're having issues, try using a different model like 'gemini-1.5-pro'.")

