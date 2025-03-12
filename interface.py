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
            background-color: #07494f;
        }
        .stTextInput>div>div>input, .stSelectbox>div>div {
            background-color: #07494f;
            border-radius: 10px;
            padding: 8px;
            font-weight: bold;
        }
        .stButton>button {
            background: linear-gradient(to right, #12c2e9, #141414, #3000b3);
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
topic = st.selectbox("📌 Select a Topic:", ["Career", "Networking", "Leadership", "Productivity", "Innovation"])
length = st.selectbox("📏 Select Length:", ["Short", "Medium", "Long", "Very Short", "Very Long"])
language = st.selectbox("🌍 Select Language:", ["English", "Hinglish", "Hindi", "Spanish", "French"])
tone = st.selectbox("💭 Select Tone:", ["Professional", "Casual", "Inspirational", "Motivational", "Humorous"])
audience = st.selectbox("👤 Target Audience:", ["Students", "Job Seekers", "Entrepreneurs", "Managers", "Developers"])
purpose = st.selectbox("🎯 Purpose of the Post:", ["Informative", "Promotional", "Storytelling", "Personal Experience", "Industry Trends"])
style = st.selectbox("🎨 Include Extras:", ["None", "Hashtags", "Emojis", "Both Hashtags & Emojis", "Custom Formatting"])

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
            prompt = (f"Generate a {length.lower()} LinkedIn post in {language} about {topic} with a {tone.lower()} tone, "
                      f"targeted at {audience}. The post should be {purpose.lower()} and engaging. "
                      f"Include {style.lower()} if applicable.")

            # Generate response
            with st.spinner("🔄 Generating your LinkedIn post..."):
                response = model.generate_content(prompt)

            # Display result
            st.success("✅ Generated LinkedIn Post:")
            st.write(response.text)

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("If you're having issues, try using a different model like 'gemini-1.5-pro'.")
