import streamlit as st
import google.generativeai as genai

# Configure the Streamlit page
st.set_page_config(
    page_title="Advanced LinkedIn Post Generator",
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
            border: 2px solid #ff4b4b !important;
            color: white;
        }
        .stButton>button {
            background: linear-gradient(to right, #12c2e9, #141414, #3000b3);
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
            border: none;
        }
        .stTextArea>div>textarea {
            background-color: #07494f;
            border: 2px solid #ff4b4b !important;
            border-radius: 10px;
            padding: 8px;
            font-weight: bold;
            color: white;
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
st.title("🚀 Advanced LinkedIn Post Generator")
st.write("Customize your LinkedIn posts with advanced options!")

# Advanced Options (20+ Options) Split into two columns for clarity
col1, col2 = st.columns(2)

with col1:
    topic = st.selectbox("📌 Topic:", ["Career", "Networking", "Leadership", "Productivity"])
    tone = st.selectbox("🎤 Post Tone:", ["Professional", "Casual", "Inspirational", "Humorous", "Empowering"])
    target_audience = st.selectbox("👥 Target Audience:", ["Job Seekers", "Industry Professionals", "Students", "Entrepreneurs"])
    industry = st.selectbox("🏭 Industry:", ["Technology", "Finance", "Healthcare", "Education", "Marketing"])
    style = st.selectbox("📝 Post Style:", ["Narrative", "Bullet Points", "Listicle", "Storytelling"])
    hashtags = st.checkbox("🔖 Include Hashtags")
    emoji = st.checkbox("😊 Include Emoji")
    call_to_action = st.checkbox("👉 Include Call-to-Action")
    quote_inclusion = st.checkbox("💬 Include a Quote")
    post_complexity = st.selectbox("⚙️ Post Complexity:", ["Simple", "Detailed", "Analytical"])

with col2:
    brand_voice = st.selectbox("🗣️ Brand Voice:", ["Friendly", "Authoritative", "Innovative", "Trusted", "Casual"])
    keywords = st.text_input("🔑 Keywords (comma separated):")
    image_suggestions = st.checkbox("📸 Suggest Image Ideas")
    video_suggestions = st.checkbox("🎥 Suggest Video Ideas")
    post_format = st.selectbox("🖼️ Post Format:", ["Text Only", "Image and Text", "Video and Text"])
    personalization = st.selectbox("💡 Personalization:", ["Include Personal Experience", "Highlight Professional Achievements", "None"])
    sentence_style = st.selectbox("✏️ Sentence Style:", ["Short", "Complex", "Mixed"])
    engagement_optimization = st.checkbox("📈 Optimize for Engagement")
    language = st.selectbox("🌍 Language:", ["English", "Hinglish", "Hindi", "Spanish"])
    length = st.selectbox("📏 Post Length:", ["Short", "Medium", "Long"])
    additional_instructions = st.text_area("📝 Additional Instructions:")

# Generate button for Advanced Post
if st.button("🎯 Generate Advanced Post"):
    if not api_key:
        st.warning("⚠️ Please enter a valid Google Gemini API Key in the sidebar.")
    else:
        try:
            # Configure API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash")

            # Build a detailed prompt based on all the provided options
            prompt = f"Generate a {length.lower()} LinkedIn post in {language} about {topic}. "
            prompt += f"Tone: {tone}. Audience: {target_audience}. Industry: {industry}. Style: {style}. "
            if hashtags:
                prompt += "Include relevant hashtags. "
            if emoji:
                prompt += "Incorporate suitable emojis. "
            if call_to_action:
                prompt += "Include a compelling call-to-action. "
            if quote_inclusion:
                prompt += "Include an inspiring quote. "
            prompt += f"Complexity: {post_complexity}. Brand Voice: {brand_voice}. "
            if keywords:
                prompt += f"Use these keywords: {keywords}. "
            if image_suggestions:
                prompt += "Suggest ideas for images. "
            if video_suggestions:
                prompt += "Suggest ideas for videos. "
            prompt += f"Post Format: {post_format}. Personalization: {personalization}. "
            prompt += f"Sentence Style: {sentence_style}. "
            if engagement_optimization:
                prompt += "Optimize the post for high engagement. "
            if additional_instructions:
                prompt += f"Additional Instructions: {additional_instructions}. "

            # Generate the LinkedIn post
            with st.spinner("🔄 Generating your advanced LinkedIn post..."):
                response = model.generate_content(prompt)

            st.success("✅ Generated Advanced LinkedIn Post:")
            st.write(response.text)

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("If you're having issues, try using a different model like 'gemini-1.5-pro'.")
