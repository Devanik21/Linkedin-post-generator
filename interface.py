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
topics = ["Career", "Networking", "Leadership", "Productivity", "Innovation", "Technology", "AI", "Marketing", "Sales", "Personal Development", "Finance", "Health & Wellness", "Education", "Startups", "Remote Work", "Diversity & Inclusion", "Sustainability", "Women in Tech", "Data Science", "Public Speaking", "Work-Life Balance", "Growth Hacking", "Cybersecurity", "Mental Health"]
lengths = ["Short", "Medium", "Long", "Very Short", "Very Long", "Concise", "Elaborate", "Brief", "Extended", "Detailed", "Twitter-Style", "Engaging", "In-Depth", "Compact", "Summarized", "Expanded", "Micro", "Mini", "Maxi", "Verbose", "Comprehensive", "To-the-Point", "Rich", "Layered"]
languages = ["English", "Hinglish", "Hindi", "Spanish", "French", "German", "Mandarin", "Portuguese", "Italian", "Russian", "Arabic", "Korean", "Japanese", "Dutch", "Swedish", "Turkish", "Hebrew", "Bengali", "Tamil", "Urdu", "Indonesian", "Greek", "Polish", "Thai"]
tones = ["Professional", "Casual", "Inspirational", "Motivational", "Humorous", "Empathetic", "Bold", "Encouraging", "Analytical", "Optimistic", "Confident", "Direct", "Persuasive", "Engaging", "Friendly", "Warm", "Serious", "Critical", "Thoughtful", "Visionary", "Pragmatic", "Respectful", "Conversational", "Exciting"]
audiences = ["Students", "Job Seekers", "Entrepreneurs", "Managers", "Developers", "Freelancers", "Marketers", "CXOs", "Consultants", "Researchers", "Startups", "HR Professionals", "Sales Executives", "Creatives", "Public Speakers", "Investors", "Educators", "Healthcare Professionals", "Government Officials", "Corporate Employees", "Product Managers", "UX Designers", "Finance Experts", "Influencers"]
purposes = ["Informative", "Promotional", "Storytelling", "Personal Experience", "Industry Trends", "Educational", "Community Building", "Customer Engagement", "Motivational", "Brand Awareness", "Recruitment", "Networking", "Awareness", "Case Study", "How-To", "Tips & Tricks", "Behind-the-Scenes", "Event Promotion", "News & Updates", "Product Launch", "Market Analysis", "Opinion Piece", "Experience Sharing", "CSR Initiatives"]
styles = ["None", "Hashtags", "Emojis", "Both Hashtags & Emojis", "Custom Formatting", "Bullet Points", "Lists", "Story Format", "Quotes", "Engagement Hooks", "Q&A Style", "Conversational", "Narrative", "Infographic-Oriented", "Tweet-Like", "Mini-Thread", "News Headline", "Interactive", "Slang-Friendly", "Puns & Wordplay", "Clickbait-Free", "Educational-Focused", "Professional Journal", "SEO-Friendly"]

# Create select boxes
topic = st.selectbox("📌 Select a Topic:", topics)
length = st.selectbox("📏 Select Length:", lengths)
language = st.selectbox("🌍 Select Language:", languages)
tone = st.selectbox("💭 Select Tone:", tones)
audience = st.selectbox("👤 Target Audience:", audiences)
purpose = st.selectbox("🎯 Purpose of the Post:", purposes)
style = st.selectbox("🎨 Include Extras:", styles)

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
