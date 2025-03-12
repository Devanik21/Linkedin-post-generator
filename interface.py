import streamlit as st
import google.generativeai as genai
import time
import re
from datetime import datetime

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
        .main {
            background-color: #f3f2ef;
            border-radius: 15px;
            padding: 20px;
        }
        .stTextInput>div>div>input, .stSelectbox>div>div, .stMultiselect>div>div {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 8px;
            border: 1px solid #0a66c2;
        }
        .stButton>button {
            background: linear-gradient(to right, #0a66c2, #0077b5);
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
        }
        .post-preview {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.1);
        }
        .linkedin-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        .profile-pic {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            margin-right: 15px;
        }
        .user-info h4, .user-info p {
            margin: 0;
        }
        .post-metrics {
            display: flex;
            justify-content: space-between;
            border-top: 1px solid #e0e0e0;
            padding-top: 10px;
            margin-top: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar for API Key and settings
with st.sidebar:
    st.image("https://brandlogos.net/wp-content/uploads/2016/06/linkedin-logo-512x512.png", width=100)
    st.markdown("### 🔑 API Configuration")
    
    # API key input with validation
    api_key = st.text_input("Enter Google Gemini API Key:", type="password")
    st.caption("Your API key is never stored and only used for generating posts.")
    
    # Model selection
    model_version = st.selectbox(
        "Select Gemini Model:",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"],
        index=0
    )
    
    # Advanced settings
    st.markdown("### ⚙️ Advanced Settings")
    temperature = st.slider("Creativity Level (Temperature):", 0.0, 1.0, 0.7, 0.1)
    
    # History
    st.markdown("### 📜 Generation History")
    if st.session_state.history:
        if st.button("Clear History"):
            st.session_state.history = []
            st.experimental_rerun()
        
        for i, item in enumerate(st.session_state.history[-5:]):
            with st.expander(f"Post {len(st.session_state.history) - i}: {item['topic']}"):
                st.write(item['content'])
    else:
        st.write("No posts generated yet.")

# Main content area
st.title("🚀 LinkedIn Post Generator")
st.write("Create engaging LinkedIn posts tailored to your professional brand.")

# Two-column layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📝 Post Configuration")
    
    # Input fields with more options
    topics = {
        "Career Development": ["Job Search", "Career Change", "Promotion", "Skills Development", "Resume Tips"],
        "Leadership": ["Team Management", "Decision Making", "Vision Setting", "Mentoring", "Crisis Management"],
        "Industry Insights": ["Market Trends", "Technology", "Innovation", "Competitor Analysis", "Industry News"],
        "Personal Branding": ["Personal Achievement", "Work Anniversary", "New Role", "Learning Journey", "Thought Leadership"],
        "Networking": ["Event Highlights", "Connection Requests", "Recommendations", "Endorsements", "Community Building"]
    }
    
    # Topic selection
    main_topic = st.selectbox("📌 Main Category:", list(topics.keys()))
    sub_topic = st.selectbox("🔍 Specific Topic:", topics[main_topic])
    
    # Tone and style
    tone_options = ["Professional", "Inspirational", "Informative", "Conversational", "Storytelling", "Humorous"]
    tone = st.selectbox("🎭 Tone:", tone_options)
    
    # Include elements
    elements = st.multiselect(
        "🧩 Include Elements:",
        ["Personal story", "Statistics", "Question for engagement", "Call to action", "Hashtags", "Emoji"],
        default=["Call to action", "Hashtags"]
    )
    
    # Length and language
    length = st.select_slider(
        "📏 Post Length:",
        options=["Very Short (1-2 paragraphs)", "Short (3-4 paragraphs)", "Medium (5-6 paragraphs)", "Long (7+ paragraphs)"],
        value="Short (3-4 paragraphs)"
    )
    
    language = st.selectbox(
        "🌍 Language:",
        ["English", "Hinglish", "Hindi", "Spanish", "French", "German", "Chinese", "Japanese", "Arabic"]
    )
    
    # Additional customization
    custom_instructions = st.text_area("✨ Additional Instructions (Optional):", placeholder="E.g., mention my 5 years of experience in digital marketing")

# Generate button and preview
if col1.button("🎯 Generate LinkedIn Post"):
    if not api_key:
        st.warning("⚠️ Please enter a valid Google Gemini API Key in the sidebar.")
    else:
        try:
            # Configure API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_version,
                generation_config={"temperature": temperature}
            )
            
            # Create a detailed prompt for AI
            elements_str = ", ".join(elements)
            prompt = f"""Generate a {length.lower()} LinkedIn post about {sub_topic} within the broader category of {main_topic}.
            
            Tone: {tone}
            Language: {language}
            Elements to include: {elements_str}
            
            Additional instructions: {custom_instructions}
            
            The post should be professional, engaging, and optimized for LinkedIn's algorithm. Format it properly with paragraphs, line breaks, and relevant hashtags if requested.
            """
            
            # Generate response
            with st.spinner("🔄 Crafting your LinkedIn post..."):
                response = model.generate_content(prompt)
                
                # Simulate slight delay for better UX
                time.sleep(1.5)
                
                # Clean up the response text
                post_text = response.text.strip()
                
                # Add to history
                st.session_state.history.append({
                    'topic': sub_topic,
                    'content': post_text,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
            # Display success message
            st.success("✅ Your LinkedIn post has been generated successfully!")
            
            # Show in preview pane
            with col2:
                st.markdown("### 👁️ LinkedIn Post Preview")
                
                # Create LinkedIn-style preview
                preview_html = f"""
                <div class="post-preview">
                    <div class="linkedin-header">
                        <img src="https://randomuser.me/api/portraits/women/65.jpg" class="profile-pic">
                        <div class="user-info">
                            <h4>Your Name</h4>
                            <p>Your Professional Title</p>
                            <small style="color: #666;">Just now • 🌎</small>
                        </div>
                    </div>
                    <div class="post-content">
                        {post_text.replace('\n', '<br>')}
                    </div>
                    <div class="post-metrics">
                        <span>👍 0</span>
                        <span>💬 0</span>
                        <span>🔁 0</span>
                    </div>
                </div>
                """
                st.markdown(preview_html, unsafe_allow_html=True)
                
                # Copy to clipboard button
                if st.button("📋 Copy to Clipboard"):
                    st.code(post_text)
                    st.info("Post text copied! You can now paste it directly to LinkedIn.")
                
        except Exception as e:
            error_message = str(e)
            st.error(f"❌ Error: {error_message}")
            
            # Provide helpful troubleshooting based on error type
            if "API key" in error_message.lower():
                st.info("Please check if your API key is valid and has permissions for the Gemini models.")
            elif "model" in error_message.lower():
                st.info("The selected model might be unavailable. Try a different model version from the sidebar.")
            else:
                st.info("If issues persist, please check your internet connection or try again later.")

# Initially show placeholder in preview pane when no post is generated
if 'history' not in st.session_state or not st.session_state.history:
    with col2:
        st.markdown("### 👁️ LinkedIn Post Preview")
        st.info("Your generated post will appear here. Configure your post settings and click 'Generate LinkedIn Post' to create content.")
        
        # Example placeholder
        st.markdown("""
        <div class="post-preview" style="opacity: 0.7;">
            <div class="linkedin-header">
                <img src="https://randomuser.me/api/portraits/women/65.jpg" class="profile-pic">
                <div class="user-info">
                    <h4>Your Name</h4>
                    <p>Your Professional Title</p>
                    <small style="color: #666;">Just now • 🌎</small>
                </div>
            </div>
            <div class="post-content" style="color: #888;">
                Your professional LinkedIn post will appear here...<br><br>
                Configure the options and click generate to see your post!<br><br>
                #LinkedInContent #ProfessionalBranding
            </div>
            <div class="post-metrics">
                <span>👍 0</span>
                <span>💬 0</span>
                <span>🔁 0</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666;">
        <small>This tool uses Google's Gemini AI to generate content. Always review and personalize AI-generated content before posting.</small>
    </div>
    """, 
    unsafe_allow_html=True
)
