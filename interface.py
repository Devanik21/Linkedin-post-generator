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
lengths = ["Short", "Medium", "Long", "Very Short", "Very Long", "Concise", "Elaborate", "Brief", "Extended", "Detailed", "Twitter-Style", "Engaging", "In-Depth", "Compact", "Summarized", "Expanded", "Micro", "Mini", "Maxi", "Verbose", "Comprehensive", "To-the-Point", "Rich", "Layered"]
topics = [
    "Career", "Networking", "Leadership", "Productivity", "Innovation", "Technology", "AI", "Marketing", "Sales", "Personal Development", 
    "Finance", "Health & Wellness", "Education", "Startups", "Remote Work", "Diversity & Inclusion", "Sustainability", "Women in Tech", 
    "Data Science", "Public Speaking", "Work-Life Balance", "Growth Hacking", "Cybersecurity", "Mental Health", "Blockchain", "NFTs", 
    "Cryptocurrency", "Web3", "Metaverse", "Virtual Reality", "Augmented Reality", "Mixed Reality", "Cloud Computing", "DevOps", "Agile", 
    "Scrum", "Kanban", "Product Management", "UX Design", "UI Design", "Graphic Design", "Content Creation", "Copywriting", "SEO", "SEM", 
    "PPC", "Social Media Marketing", "Email Marketing", "Affiliate Marketing", "Influencer Marketing", "Video Marketing", "Content Marketing", 
    "Brand Building", "Personal Branding", "Corporate Branding", "Employer Branding", "Recruitment", "Talent Acquisition", "HR Tech", 
    "Employee Engagement", "Employee Experience", "Learning & Development", "Performance Management", "Compensation & Benefits", 
    "Workplace Culture", "Team Building", "Emotional Intelligence", "Soft Skills", "Hard Skills", "Technical Skills", "Digital Skills", 
    "Future of Work", "Future of Education", "Future of Healthcare", "Future of Finance", "Future of Transportation", "Future of Energy", 
    "Future of Food", "Future of Retail", "Future of Manufacturing", "Industry 4.0", "Smart Cities", "Smart Homes", "Internet of Things", 
    "Big Data", "Data Analytics", "Business Intelligence", "Artificial Intelligence", "Machine Learning", "Deep Learning", "Neural Networks", 
    "Computer Vision", "Natural Language Processing", "Robotics", "Automation", "RPA", "Digital Transformation", "Business Transformation", 
    "Organizational Change", "Change Management", "Project Management", "Program Management", "Portfolio Management", "Risk Management", 
    "Crisis Management", "Business Continuity", "Disaster Recovery", "Information Security", "Network Security", "Application Security", 
    "Cloud Security", "Mobile Security", "Data Privacy", "GDPR", "CCPA", "HIPAA", "Compliance", "Regulatory", "Legal Tech", "Contract Management", 
    "Intellectual Property", "Patents", "Trademarks", "Copyrights", "Trade Secrets", "Business Law", "Corporate Law", "Employment Law", 
    "Tax Law", "Real Estate Law", "Immigration Law", "Healthcare Law", "Environmental Law", "International Law", "Constitutional Law", 
    "Criminal Law", "Civil Law", "Family Law", "Estate Planning", "Wills & Trusts", "Probate", "Mergers & Acquisitions", "Venture Capital", 
    "Private Equity", "Angel Investing", "Crowdfunding", "Initial Public Offering", "Stock Market", "Bond Market", "Forex", "Commodities", 
    "Futures", "Options", "Derivatives", "Mutual Funds", "ETFs", "Index Funds", "Retirement Planning", "401k", "IRA", "Roth IRA", "Social Security", 
    "Medicare", "Medicaid", "Health Insurance", "Life Insurance", "Disability Insurance", "Long-Term Care Insurance", "Property Insurance", 
    "Casualty Insurance", "Auto Insurance", "Home Insurance", "Renters Insurance", "Budgeting", "Saving", "Investing", "Real Estate Investing", 
    "REITs", "Rental Properties", "Fix & Flip", "House Hacking", "Commercial Real Estate", "Residential Real Estate", "Industrial Real Estate", 
    "Retail Real Estate", "Office Real Estate", "Multifamily Real Estate", "Land Development", "Construction", "Architecture", "Interior Design", 
    "Exterior Design", "Landscape Design", "Urban Planning", "Rural Development", "Sustainable Development", "Green Building", "LEED Certification", 
    "Energy Efficiency", "Renewable Energy", "Solar Power", "Wind Power", "Hydropower", "Geothermal Power", "Biomass Energy", "Nuclear Energy", 
    "Fossil Fuels", "Oil & Gas", "Coal", "Natural Resources", "Water Conservation", "Wildlife Conservation", "Forest Conservation", 
    "Marine Conservation", "Climate Change", "Global Warming", "Carbon Footprint", "Carbon Offset", "Carbon Capture", "Circular Economy", 
    "Zero Waste", "Recycling", "Upcycling", "Ethical Consumption", "Fair Trade", "Organic", "Non-GMO", "Plant-Based", "Veganism", "Vegetarianism", 
    "Flexitarianism", "Keto Diet", "Paleo Diet", "Mediterranean Diet", "Intermittent Fasting", "Nutrition", "Fitness", "Strength Training", 
    "Cardio", "HIIT", "Yoga", "Pilates", "Meditation", "Mindfulness", "Stress Management", "Sleep Health", "Digital Wellbeing", "Digital Detox", 
    "Work Addiction", "Burnout Prevention", "Mental Health Awareness", "Depression", "Anxiety", "PTSD", "OCD", "ADHD", "Autism", "Neurodiversity", 
    "Disability Inclusion", "Accessibility", "Universal Design", "Assistive Technology", "Regenerative Agriculture", "Aquaponics", "Hydroponics", 
    "Vertical Farming", "Urban Farming", "Community Gardens", "Food Security", "Food Sovereignty", "Indigenous Knowledge", "Traditional Wisdom", 
    "Cultural Heritage", "Language Preservation", "Art & Culture", "Music", "Visual Arts", "Performing Arts", "Literature", "Poetry", "Film", 
    "Photography", "Fashion", "Design Thinking", "Human-Centered Design", "Service Design", "Experience Design", "Computational Design", 
    "Algorithmic Design", "Generative Design", "3D Printing", "Additive Manufacturing", "Subtractive Manufacturing", "CNC Machining", "Laser Cutting", 
    "Robotics Process Automation", "Quantum Computing", "Edge Computing", "Fog Computing", "Grid Computing", "High-Performance Computing", 
    "Supercomputing", "Microservices", "Serverless Architecture", "Containerization", "Docker", "Kubernetes", "Terraform", "Infrastructure as Code", 
    "GitOps", "MLOps", "AIOps", "DevSecOps", "SRE", "Observability", "Monitoring", "Logging", "Tracing", "API Development", "Frontend Development", 
    "Backend Development", "Full Stack Development", "Mobile Development", "Android Development", "iOS Development", "Cross-Platform Development", 
    "React", "Angular", "Vue", "Svelte", "Node.js", "Python", "JavaScript", "TypeScript", "Java", "C#", "C++", "Ruby", "PHP", "Swift", "Kotlin", 
    "Go", "Rust", "Haskell", "Elixir", "SQL", "NoSQL", "MongoDB", "MySQL", "PostgreSQL", "Oracle", "SQL Server", "Redis", "Elasticsearch", 
    "Cassandra", "Neo4j", "TensorFlow", "PyTorch", "Keras", "scikit-learn", "NLTK", "spaCy", "OpenCV", "SciPy", "NumPy", "Pandas", "Matplotlib", 
    "Seaborn", "Tableau", "Power BI", "Excel", "Google Sheets", "Google Analytics", "Adobe Analytics", "Mixpanel", "Amplitude", "Hotjar", 
    "Optimizely", "A/B Testing", "Multivariate Testing", "User Testing", "Usability Testing", "Accessibility Testing", "Security Testing", 
    "Performance Testing", "Load Testing", "Stress Testing", "Regression Testing", "Unit Testing", "Integration Testing", "System Testing", 
    "Acceptance Testing", "End-to-End Testing", "Test Automation", "Selenium", "Cypress", "Playwright", "Jest", "Mocha", "Chai", "JUnit", "NUnit"
]

lengths = ["Short", "Medium", "Long", "Very Short", "Very Long", "Concise", "Elaborate", "Brief", "Extended", "Detailed", "Twitter-Style", "Engaging", "In-Depth", "Compact", "Summarized", "Expanded", "Micro", "Mini", "Maxi", "Verbose", "Comprehensive", "To-the-Point", "Rich", "Layered"]

languages = [
    "English", "Hindi", "Bengali", "Spanish", "French", "German", "Mandarin", "Portuguese", "Italian", "Russian", "Arabic", "Korean", "Japanese", 
    "Dutch", "Swedish", "Turkish", "Hebrew", "Tamil", "Urdu", "Indonesian", "Greek", "Polish", "Thai", "Vietnamese", "Filipino", "Malay", "Czech", 
    "Hungarian", "Romanian", "Finnish", "Norwegian", "Danish", "Slovak", "Ukrainian", "Persian", "Hebrew", "Swahili", "Hausa", "Zulu", "Xhosa", 
    "Igbo", "Yoruba", "Burmese", "Khmer", "Lao", "Sinhala", "Pashto", "Kurdish", "Basque", "Catalan", "Galician", "Maltese", "Luxembourgish", 
    "Icelandic", "Welsh", "Scottish Gaelic", "Irish", "Maori", "Hawaiian", "Samoan", "Tongan", "Tahitian", "Chamorro", "Fijian", "Mongolian", 
    "Tibetan", "Quechua", "Aymara", "Guarani", "Haitian Creole", "Twi", "Amharic", "Tigrinya", "Oromo", "Shona", "Sesotho", "Tswana", "Sindhi", 
    "Nepali", "Kashmiri", "Assamese", "Marathi", "Gujarati", "Punjabi", "Kannada", "Malayalam", "Telugu", "Santali", "Meitei", "Bodo", "Dogri", 
    "Konkani", "Maithili", "Bhili", "Gondi", "Tulu", "Bishnupriya", "Manipuri", "Sylheti", "Afrikaans", "Albanian", "Amharic", "Armenian", 
    "Azerbaijani", "Belarusian", "Bosnian", "Bulgarian", "Burmese", "Cebuano", "Chichewa", "Corsican", "Croatian", "Esperanto", "Estonian", 
    "Frisian", "Gaelic", "Georgian", "Gujarati", "Haitian Creole", "Hausa", "Hawaiian", "Hmong", "Igbo", "Javanese", "Kannada", "Kazakh", 
    "Khmer", "Kinyarwanda", "Kurdish", "Kyrgyz", "Lao", "Latin", "Latvian", "Lithuanian", "Luxembourgish", "Macedonian", "Malagasy", "Malay", 
    "Malayalam", "Maltese", "Maori", "Marathi", "Mongolian", "Myanmar", "Nepali", "Odia", "Pashto", "Persian", "Punjabi", "Samoan", "Scots Gaelic", 
    "Serbian", "Sesotho", "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali", "Sundanese", "Swahili", "Tajik", "Tamil", "Tatar", 
    "Telugu", "Thai", "Turkish", "Turkmen", "Ukrainian", "Urdu", "Uyghur", "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish", "Yoruba", "Zulu",
    "Abkhazian", "Acehnese", "Acholi", "Adyghe", "Afar", "Afrihili", "Ainu", "Akan", "Akkadian", "Aleut", "Algonquin", "Alsatian", "Altai", 
    "Ancient Egyptian", "Ancient Greek", "Anglo-Saxon", "Angika", "Apache", "Aragonese", "Aramaic", "Arapaho", "Arawak", "Assamese", "Asturian", 
    "Avaric", "Avestan", "Awadhi", "Balinese", "Baluchi", "Bambara", "Bashkir", "Bassa", "Batak", "Bemba", "Bhojpuri", "Bikol", "Bini", 
    "Bislama", "Blackfoot", "Braj", "Brahui", "Breton", "Buginese", "Buhid", "Cakchiquel", "Californian", "Cantonese", "Carib", "Cayuga", 
    "Cebuano", "Chagatai", "Chamorro", "Chechen", "Cherokee", "Cheyenne", "Chibcha", "Chiga", "Chin", "Chipewyan", "Choctaw", "Church Slavic", 
    "Chuvash", "Comorian", "Coptic", "Cornish", "Corsican", "Cree", "Creek", "Crimean Tatar", "Croatian", "Dakota", "Dargwa", "Delaware", 
    "Dinka", "Divehi", "Dogri", "Douala", "Duala", "Dzongkha", "Efik", "Ekajuk", "Elamite", "Erzya", "Ewe", "Ewondo", "Fang", "Fanti", 
    "Faroese", "Fijian", "Filipino", "Finnish", "Fon", "Frafra", "Frisian", "Friulian", "Fulah", "Ga", "Gagauz", "Galician", "Ganda", 
    "Gayo", "Gbaya", "Geez", "Gilbertese", "Gondi", "Gorontalo", "Gothic", "Grebo", "Guarani", "Gujarati", "Gwich'in"
]

tones = [
    "Professional", "Casual", "Inspirational", "Motivational", "Humorous", "Empathetic", "Bold", "Encouraging", "Analytical", "Optimistic", 
    "Confident", "Direct", "Persuasive", "Engaging", "Friendly", "Warm", "Serious", "Critical", "Thoughtful", "Visionary", "Pragmatic", 
    "Respectful", "Conversational", "Exciting", "Academic", "Authoritative", "Balanced", "Candid", "Caring", "Cautious", "Challenging", 
    "Cheerful", "Clear", "Collaborative", "Commanding", "Compassionate", "Conciliatory", "Concerned", "Congratulatory", "Constructive", 
    "Contemplative", "Convincing", "Cooperative", "Creative", "Credible", "Curious", "Decisive", "Delightful", "Diplomatic", "Disarming", 
    "Dramatic", "Earnest", "Educational", "Eloquent", "Emotional", "Empowering", "Energetic", "Enlightening", "Enthusiastic", "Ethical", 
    "Evocative", "Excited", "Expert", "Explanatory", "Expressive", "Factual", "Fair", "Fascinating", "Fierce", "Firm", "Forward-Thinking", 
    "Genuine", "Gracious", "Grateful", "Guiding", "Helpful", "Honest", "Hopeful", "Humble", "Impartial", "Impassioned", "Inclusive", 
    "Informative", "Inquisitive", "Insightful", "Instructive", "Intellectual", "Intense", "Intimate", "Introspective", "Intuitive", 
    "Inviting", "Judicial", "Kind", "Knowledgeable", "Lighthearted", "Logical", "Loving", "Lyrical", "Matter-of-Fact", "Meditative", 
    "Methodical", "Mindful", "Modest", "Nurturing", "Objective", "Open-Minded", "Opinionated", "Passionate", "Patient", "Patriotic", 
    "Peaceful", "Personable", "Philosophical", "Pioneering", "Playful", "Poetic", "Polite", "Practical", "Proactive", "Problem-Solving", 
    "Progressive", "Provocative", "Questioning", "Quirky", "Rational", "Reassuring", "Reflective", "Reinforcing", "Relaxed", "Reliable", 
    "Resolute", "Resonant", "Resourceful", "Reverent", "Revolutionary", "Rigorous", "Robust", "Sarcastic", "Satirical", "Scholarly", 
    "Scientific", "Sensible", "Sensitive", "Sentimental", "Sincere", "Skeptical", "Smart", "Sobering", "Solemn", "Sophisticated", "Soulful", 
    "Spirited", "Spiritual", "Stimulating", "Strategic", "Straightforward", "Strong", "Supportive", "Surprised", "Sympathetic", "Tactical", 
    "Tactful", "Technical", "Tenacious", "Tender", "Thorough", "Thoughtful", "Thought-Provoking", "Tolerant", "Tough", "Transparent", 
    "Trendy", "Trustworthy", "Understanding", "Unexpected", "Unfiltered", "Upbeat", "Uplifting", "Urgent", "Vibrant", "Vigilant", 
    "Virtuous", "Visionary", "Vivid", "Vulnerable", "Welcoming", "Whimsical", "Wise", "Witty", "Wonder-Filled", "Worried", "Yearning", 
    "Zealous", "Adventurous", "Appreciative", "Articulate", "Astute", "Attentive", "Authentic", "Awe-Struck", "Breathtaking", "Calm", 
    "Captivating", "Celebratory", "Charismatic", "Civic-Minded", "Clever", "Committed", "Comforting", "Compelling", "Conscientious", 
    "Conservative", "Considerate", "Consistent", "Controversial", "Cool", "Courageous", "Cynical", "Daring", "Data-Driven", "Dazzling", 
    "Deliberate", "Devoted", "Dignified", "Diligent", "Dynamic", "Easy-Going", "Eclectic", "Economical", "Effervescent", "Efficient", 
    "Elegant", "Elevated", "Emotional", "Enchanting", "Encouraging", "Endearing", "Energetic", "Enigmatic", "Entertaining", "Entrepreneurial", 
    "Environmental", "Equitable", "Experimental", "Expository", "Extraordinary", "Fair-Minded", "Faithful", "Fearless", "Feminist", 
    "Fervent", "Festive", "Fiery", "Flamboyant", "Folksy", "Formal", "Fortifying", "Fresh", "Futuristic", "Gentle", "Gifted", "Gritty", 
    "Grounded", "Growth-Oriented", "Harmonious", "Hearty", "Heroic", "High-Energy", "Historical", "Holistic", "Idealistic", "Idiosyncratic", 
    "Illuminating", "Immersive", "Impactful", "Impeccable", "Impulsive", "Incisive", "Indignant", "Industrious", "Inimitable", "Innovative", 
    "Inquisitive", "Insistent", "Inspiring", "Instructional", "Intelligent", "Intentional", "Intimate", "Intriguing", "Judicial"
]

audiences = [
    "Students", "Job Seekers", "Entrepreneurs", "Managers", "Developers", "Freelancers", "Marketers", "CXOs", "Consultants", "Researchers", 
    "Startups", "HR Professionals", "Sales Executives", "Creatives", "Public Speakers", "Investors", "Educators", "Healthcare Professionals", 
    "Government Officials", "Corporate Employees", "Product Managers", "UX Designers", "Finance Experts", "Influencers", "Venture Capitalists", 
    "Policy Makers", "Tech Enthusiasts", "Non-Profit Leaders", "Customer Success Managers", "Academicians", "Small Business Owners", 
    "Legal Experts", "Content Creators", "Software Engineers", "Business Analysts", "Accountants", "Administrative Assistants", "Advertising Executives", 
    "Aerospace Engineers", "Agricultural Scientists", "AI Specialists", "Airport Managers", "Alumni Networks", "Animators", "Anthropologists", 
    "Antiquarians", "Archaeologists", "Architects", "Art Directors", "Art Historians", "Artists", "Astronomers", "Astrophysicists", "Athletes", 
    "Audiologists", "Auditors", "Authors", "Automotive Engineers", "Aviation Professionals", "Bakers", "Bankers", "Baristas", "Beauticians", 
    "Behavioral Economists", "Biochemists", "Bioinformaticians", "Biologists", "Biomedical Engineers", "Biotechnologists", "Blacksmiths", 
    "Blockchain Developers", "Bloggers", "Board Members", "Book Publishers", "Botanists", "Brand Managers", "Brewers", "Broadcast Journalists", 
    "Building Inspectors", "Business Coaches", "Business Development Professionals", "Business Intelligence Analysts", "Business Owners", 
    "Butchers", "Buyers", "Call Center Managers", "Camera Operators", "Career Counselors", "Carpenters", "Cartographers", "Caterers", 
    "Chefs", "Chemical Engineers", "Chemists", "Chief Data Officers", "Chief Digital Officers", "Chief Executive Officers", "Chief Financial Officers", 
    "Chief Information Officers", "Chief Marketing Officers", "Chief Operating Officers", "Chief People Officers", "Chief Product Officers", 
    "Chief Revenue Officers", "Chief Strategy Officers", "Chief Technology Officers", "Child Care Providers", "Chiropractors", "Choreographers", 
    "Civil Engineers", "Clinical Psychologists", "Cloud Architects", "Coaches", "College Administrators", "College Students", "Commercial Fishermen", 
    "Community Managers", "Community Organizers", "Composers", "Computer Network Architects", "Computer Programmers", "Computer Science Students", 
    "Computer Systems Analysts", "Construction Managers", "Construction Workers", "Consultants", "Consumer Researchers", "Content Strategists", 
    "Contractors", "Copywriters", "Corporate Trainers", "Cosmetologists", "Cost Estimators", "Counselors", "Court Reporters", "Craft Artists", 
    "Creative Directors", "Credit Analysts", "Credit Managers", "Criminologists", "Curators", "Customer Experience Managers", "Customer Service Representatives", 
    "Cybersecurity Analysts", "Dance Instructors", "Data Analysts", "Data Engineers", "Data Entry Clerks", "Data Scientists", "Database Administrators", 
    "Dental Assistants", "Dental Hygienists", "Dentists", "Dermatologists", "Design Engineers", "Desktop Publishers", "Detectives", "Dietitians", 
    "Digital Artists", "Digital Marketers", "Digital Nomads", "Digital Strategists", "Directors", "Dishwashers", "Dispatchers", "Doctors", 
    "Dog Trainers", "Drone Operators", "Early Career Professionals", "Ecologists", "E-commerce Managers", "Economists", "Editors", "Education Administrators", 
    "Electrical Engineers", "Electricians", "Electronic Engineers", "Elementary School Teachers", "Emergency Management Directors", "Emergency Medical Technicians", 
    "Employee Benefits Managers", "Endocrinologists", "Energy Analysts", "Energy Engineers", "Engineering Managers", "Engineering Students", 
    "English Teachers", "Entomologists", "Entrepreneurs", "Environmental Scientists", "Epidemiologists", "Equestrians", "Ergonomic Specialists", 
    "Escrow Officers", "Estheticians", "Ethical Hackers", "Event Coordinators", "Event Planners", "Exercise Physiologists", "Exporters", 
    "Facilities Managers", "Factory Workers", "Family Physicians", "Farmers", "Fashion Designers", "Fast Food Workers", "Field Service Technicians", 
    "Film Directors", "Film Editors", "Film Producers", "Financial Advisors", "Financial Analysts", "Financial Managers", "Financial Planners", 
    "Firefighters", "Fishery Managers", "Fitness Instructors", "Flight Attendants", "Floral Designers", "Food Critics", "Food Scientists", 
    "Food Service Managers", "Forensic Accountants", "Forensic Scientists", "Forest Rangers", "Foresters", "Founders", "Franchise Owners", 
    "Fraud Examiners", "Front-End Developers", "Full Stack Developers", "Fundraisers", "Furniture Designers", "Game Developers", "Game Wardens", 
    "Gaming Supervisors", "Gardeners", "Gemologists", "General Contractors", "General Managers", "Geneticists", "Geographers", "Geologists", 
    "Geophysicists", "Graphic Designers", "Green Building Consultants", "Groundskeepers", "Growth Hackers", "Guidance Counselors", "Hairdressers", 
    "Hardware Engineers", "Health Coaches", "Health Educators", "Healthcare Administrators", "Healthcare IT Specialists", "Heat, Air, Refrigeration Mechanics", 
    "High School Students", "High School Teachers", "Highway Maintenance Workers", "Historians", "Home Health Aides", "Hospice Workers", 
    "Hospitality Managers", "Hotel Managers", "Housekeepers", "Housing Specialists", "Human Resources Assistants", "Human Resources Managers", 
    "Human Rights Advocates", "HVAC Technicians", "Hydraulic Engineers", "Hydrologists", "Illustrators", "Immigration Officers", "Importers", 
    "Industrial Designers", "Industrial Engineers", "Industrial Maintenance Mechanics", "Industrial Production Managers", "Information Security Analysts", 
    "Information Technology Managers", "Insurance Agents", "Insurance Underwriters", "Interior Designers", "Internal Auditors", "International Aid Workers", 
    "International Business Professionals", "International Development Professionals", "International Relations Specialists", "International Students", 
    "Internet of Things Engineers", "Interpreters", "Inventors", "Investment Bankers", "Investment Fund Managers"
]

purposes = [
        "Informative", "Promotional", "Storytelling", "Personal Experience", "Industry Trends", "Educational", "Community Building",
        "Customer Engagement", "Motivational", "Brand Awareness", "Recruitment", "Networking", "Awareness", "Case Study", "How-To",
        "Tips & Tricks", "Behind-the-Scenes", "Event Promotion", "News & Updates", "Product Launch", "Market Analysis", "Opinion Piece",
        "Experience Sharing", "CSR Initiatives", "Webinar Promotion", "Podcast Announcement", "Survey Results", "Milestone Celebration",
        "Partnership Announcement", "Crowdfunding Campaign", "Social Advocacy", "Tech Innovation", "User Testimonials", "Thought Leadership",
        "Account Acquisition", "Advice Giving", "Alumni Connection", "Announcement", "Annual Report", "Appreciation", "Ask for Help",
        "Award Recognition", "Best Practices", "Blog Promotion", "Book Launch", "Book Recommendation", "Book Review", "Breaking News",
        "Business Update", "Call for Action", "Call for Collaboration", "Call for Speakers", "Career Advice", "Career Journey", "Career Milestone",
        "Career Transition", "Challenge Participation", "Challenging Assumptions", "Charity Fundraising", "Client Success Story", "Coaching Offering",
        "Company Anniversary", "Company Culture", "Company History", "Company Merger", "Company Pivot", "Company Rebrand", "Company Values",
        "Competitive Analysis", "Conference Highlights", "Conference Promotion", "Congratulating Others", "Contest Announcement", "Conversation Starter",
        "Course Launch", "Course Promotion", "Creative Process", "Crisis Communication", "Crisis Management", "Cross-Promotion", "Cultural Commentary",
        "Current Affairs", "Customer Appreciation", "Customer Feedback Request", "Customer Pain Points", "Customer Spotlight", "Customer Success",
        "Data Analysis", "Data Visualization", "Day in the Life", "Debate Initiation", "Decision Making Process", "Demystifying Concepts",
        "Diagram Explanation", "Disaster Relief", "Discounts & Deals", "Discussion Thread", "DIY Guide", "Documentary Promotion", "Economic Analysis",
        "Editorial", "Emotional Support", "Employee Appreciation", "Employee Highlight", "Employee Recognition", "Employee Spotlight",
        "Encouragement", "End of Year Review", "Environmental Awareness", "Equity & Inclusion", "Error Acknowledgment", "Ethics Discussion",
        "Expert Interview", "Expert Roundup", "Explainer", "Failure Analysis", "FAQ", "Feature Announcement", "Feature Comparison", "Feature Request",
        "Feedback Collection", "Feedback Response", "First Day Experience", "First Impressions", "Flash Sale", "Free Resource", "Free Tool",
        "Freelance Work Promotion", "Frequently Asked Questions", "Future Prediction", "Future Trends", "Giveaway", "Global Issue Awareness",
        "Goal Setting", "Grant Announcement", "Graphic Explanation", "Gratitude Expression", "Growth Metrics", "Guide", "Holiday Greeting",
        "Holiday Promotion", "Holiday Wishes", "Hot Take", "Humanitarian Effort", "Idea Generation", "Idea Sharing", "Identity Statement",
        "Image Gallery", "Impact Report", "Implementation Strategy", "Implications of Research", "Improvement Process", "In Memoriam",
        "Industry Analysis", "Industry Award", "Industry Challenge", "Industry Comparison", "Industry Disruption", "Industry Event",
        "Industry Forecast", "Industry Insight", "Industry News", "Industry Recognition", "Industry Report", "Industry Resource",
        "Industry Standard", "Industry Statistics", "Infographic Sharing", "Innovation Showcase", "Inspirational Quote",
        "Interview Preparation", "Investment Announcement", "Job Opening", "Job Promotion", "Job Search", "Job Sharing",
        "Knowledge Sharing", "Leadership Insight", "Leadership Philosophy", "Leadership Strategy", "Learning Experience",
        "Lesson Learned", "Life Update", "Limited Offer", "Link Roundup", "List Post", "Live Event", "Local Event",
        "Long-form Content", "Market Education", "Market Expansion", "Market Insight", "Market Opportunity", "Market Research",
        "Market Trend", "Media Coverage", "Media Feature", "Media Mention", "Meetup Invitation", "Mentoring Offer",
        "Mentorship Program", "Mission Statement", "Mistake Analysis", "Monthly Recap", "Motivational Message", "New Feature",
        "New Hire Announcement", "New Insight", "New Location", "New Office", "New Perspective", "New Position",
        "New Research", "New Service", "New Team Member", "Newsletter Promotion", "Niche Expertise", "Office Tour",
        "Office Update", "Online Course", "Opinion Poll", "Opportunity Sharing", "Pain Point Solution", "Panel Discussion",
        "Parent Experience", "Parenting Advice", "Participation Request", "Partner Appreciation", "Partner Highlight",
        "Partnership Benefit", "Patent Announcement", "People Profile", "Personal Achievement", "Personal Announcement",
        "Personal Challenge", "Personal Development", "Personal Growth", "Personal Journey", "Personal Milestone",
        "Personal Project", "Personal Reflection", "Personal Story", "Personal Update", "Perspective Shift",
        "PhD Journey", "Philanthropy Effort", "Photo Essay", "Podcast Episode", "Podcast Feature", "Podcast Guest",
        "Podcast Highlight", "Podcast Launch", "Podcast Recommendation", "Policy Change", "Policy Discussion",
        "Policy Impact", "Portfolio Update", "Positive Feedback", "Positive News", "Positive Review", "Press Release",
        "Pricing Change", "Pricing Strategy", "Problem Solution", "Process Documentation", "Process Improvement",
        "Product Announcement", "Product Comparison", "Product Demo", "Product Development", "Product Education",
        "Product Explainer", "Product Feature", "Product Highlight", "Product Improvement", "Product Knowledge",
        "Product Recommendation", "Product Review", "Product Teaser", "Product Tutorial", "Product Update",
        "Product Usage", "Professional Development", "Professional Milestone", "Professional Opinion",
        "Professional Update", "Profile Update", "Progress Report", "Project Announcement", "Project Completion",
        "Project Launch", "Project Milestone", "Project Update", "Promotion Announcement", "Public Speaking",
        "Publication Announcement", "Q&A Session", "Question Asking", "Quick Tip", "Quote Commentary", "R&D Update",
        "Reader Question", "Recognition", "Recommendation", "Recruitment Drive", "Redesign Announcement", "Relaunch",
        "Relocation Announcement", "Remote Work", "Report Findings", "Research Finding", "Research Publication",
        "Research Summary", "Research Update", "Resource List", "Resource Recommendation", "Resource Sharing",
        "Response to Criticism", "Response to Feedback", "Response to News", "Resume Tips", "Retirement Announcement",
        "Revenue Report", "Review", "Sales Announcement", "Sales Pitch", "Scholarship Announcement", "Season's Greetings",
        "Security Update", "Self-Improvement", "Self-Reflection", "Service Announcement", "Service Comparison",
        "Service Explanation", "Service Highlight", "Service Improvement", "Service Launch", "Service Offering",
        "Service Update", "Short Story", "Showcase", "Side Project", "Skill Development", "Skill Sharing",
        "Social Issue", "Social Proof", "Software Release", "Solution Proposal", "Special Offer", "Sponsorship Announcement",
        "Startup Journey", "Statistics Share", "Step-by-Step Guide", "Stock Update", "Strategy Explanation",
        "Student Experience", "Study Finding", "Success Story", "Summary", "Supply Chain Update", "Support Request",
        "Survey Invitation", "Survey Launch", "Survey Result", "System Update", "Team Achievement", "Team Announcement",
        "Team Building", "Team Highlight", "Team Introduction", "Team Member Highlight", "Team Recognition",
        "Team Update", "Technical Explanation", "Technical Guide", "Technical Issue", "Technical Solution",
        "Technology Comparison", "Technology Education", "Technology Explainer", "Technology Preview",
        "Technology Review", "Technology Trend", "Testimonial", "Text Post", "Thank You Note", "Thesis Defense",
        "Thought Experiment", "Thought Piece", "Throwback", "Time Management", "Tip Sharing", "Tool Recommendation",
        "Tool Review", "Tool Sharing", "Training Announcement", "Training Offer", "Training Program",
        "Transparency Report", "Travel Experience", "Travel Tip", "Trend Analysis", "Trend Report",
        "Trivia", "Tutorial", "Upcoming Event", "Update", "User Experience", "User Feedback", "User Guide",
        "User Interface", "User Research", "User Story", "Vacation Announcement", "Value Proposition",
        "Video Promotion", "Video Share", "Virtual Event", "Vision Statement", "Volunteer Experience",
        "Volunteer Opportunity", "Webinar Announcement", "Webinar Recap", "Website Launch", "Website Update",
        "Weekly Recap", "Welcome Message", "Wellness Tip", "White Paper Announcement", "White Paper Summary",
        "Work Anniversary", "Work Culture", "Work Experience", "Work Highlight", "Work Process", "Work Update",
        "Workshop Announcement", "Workshop Invitation", "Year in Review", "Your Take"
      ]
styles = ["None", "Hashtags", "Emojis", "Both Hashtags & Emojis", "Custom Formatting", "Bullet Points", "Lists", "Story Format", "Quotes", "Engagement Hooks", "Q&A Style", "Conversational", "Narrative", "Infographic-Oriented", "Tweet-Like", "Mini-Thread", "News Headline", "Interactive", "Slang-Friendly", "Puns & Wordplay", "Clickbait-Free", "Educational-Focused", "Professional Journal", "SEO-Friendly", "Visual Elements", "Data-Driven Insights", "Minimalist Style", "Call-to-Action Focused", "Humor-Infused", "Metaphor-Based", "Dialogue-Driven", "Question-Led", "Trend-Jacking"]

# Create select boxes
topic = st.selectbox("📌 Select a Topic:", topics)
length = st.selectbox("📏 Select Length:", lengths)
language = st.selectbox("🌍 Select Language:", languages, index=0, key="language_search")
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
