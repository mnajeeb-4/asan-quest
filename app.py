import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# -----------------------------------------
# 1. PAGE CONFIGURATION & iPHONE THEME CSS
# -----------------------------------------
st.set_page_config(page_title="EduGlass - Student AI", page_icon="📱", layout="centered")

# Dark Glassmorphism (iPhone Style) CSS
st.markdown("""
<style>
    /* Background Gradient (iOS Dark Mode Feel) */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        color: white;
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Glassmorphism Title */
    .glass-title {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .glass-title h1 {
        font-weight: 700;
        letter-spacing: 1px;
        background: -webkit-linear-gradient(#fff, #a1c4fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    /* Glassmorphism Containers */
    div[data-testid="stFileUploader"], .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }

    /* iOS Style Buttons */
    div.stButton > button:first-child {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 25px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    div.stButton > button:first-child:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateY(-2px);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }

    /* Output Text Box Glass Effect */
    .glass-output {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 25px;
        margin-top: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        color: #e0e0e0;
        font-size: 16px;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# 2. DEVELOPER API KEY SETUP (Free & Hidden)
# -----------------------------------------
# Bhai yahan apni FREE Google Gemini API key dalein. 
# Students ko ye nahi dikhegi aur unke liye app free hogi.
GEMINI_API_KEY = "AIzaSyA3GCv2lKeOSan-PcBcoSqJh-0DfNh5fjo" 

genai.configure(api_key=GEMINI_API_KEY)
# Using Gemini 1.5 Flash for fast and accurate image reading
model = genai.GenerativeModel('gemini-1.5-flash')

# -----------------------------------------
# 3. APP UI & LOGIC
# -----------------------------------------
st.markdown("""
<div class="glass-title">
    <h1>📱 EduGlass AI</h1>
    <p style='color: #ccc; margin-top: 5px; font-size: 14px;'>Upload any question pic. Get answers instantly. Stress Free Study!</p>
</div>
""", unsafe_allow_html=True)

# Image Uploader (Camera or Gallery)
uploaded_file = st.file_uploader("📸 Upload Question Picture (School/College/Uni)", type=["png", "jpg", "jpeg", "webp"])

# Language Selector
target_language = st.text_input("🌐 Answer Language (e.g., Roman Urdu, English, Hindi, Spanish):", placeholder="Roman Urdu")

# Submit Button
if st.button("🚀 Solve Question"):
    if not target_language:
        st.warning("⚠️ Please enter a language (e.g., Roman Urdu).")
    elif not uploaded_file:
        st.warning("⚠️ Please upload a picture of the question.")
    elif GEMINI_API_KEY == "YAHAN_APNI_FREE_GEMINI_API_KEY_DALEIN":
        st.error("⚠️ Developer Error: Please put your Free Gemini API Key in the code.")
    else:
        try:
            # Display processing spinner
            with st.spinner('AI is thinking... 🧠'):
                # Read Image
                image = Image.open(uploaded_file)
                st.image(image, caption="Your Question", use_container_width=True)

                # Custom Prompt for AI
                prompt = f"""
                You are a highly intelligent tutor for school, college, and university students.
                Analyze the provided image carefully. It contains a question or a problem (could be Math, Science, Programming, Literature, etc.).
                
                Task:
                1. Solve the problem or answer the question shown in the image step-by-step.
                2. Explain it in a very easy-to-understand way so the student feels tension-free.
                3. You MUST provide the final response strictly in this language: {target_language}.
                """

                # Get Response from AI
                response = model.generate_content([prompt, image])

                # Display Output in Glass Box
                st.markdown(f"""
                <div class="glass-output">
                    <h3 style="color: white; margin-top: 0;">✅ Answer:</h3>
                    {response.text}
                </div>
                """, unsafe_allow_html=True)
                
                st.balloons() # Happy animation for students

        except Exception as e:
            st.error(f"❌ Koi error aa gaya! Please try again. Details: {e}")
