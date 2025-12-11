import streamlit as st
import requests
from PIL import Image
import io
import base64
import os
from datetime import datetime

# Try to import audio recorder, provide fallback if not available
try:
    from audio_recorder_streamlit import audio_recorder
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="CBRE Blueprint Analyzer",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS for Professional CBRE Look
st.markdown("""
<style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove all white backgrounds */
    .main, .block-container, .stApp, [data-testid="stAppViewContainer"],
    [data-testid="stHeader"], section[data-testid="stSidebar"] {
        background: #1a1a1a !important;
    }
    
    /* Main Container */
    .main {
        background: #1a1a1a !important;
        padding: 0 !important;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
        background: #1a1a1a !important;
    }
    
    /* Remove default Streamlit padding/margins that cause white space */
    .css-1d391kg, .css-12oz5g7, .css-1dp5vir {
        background: #1a1a1a !important;
    }
    
    /* Top Header Bar */
    .top-header {
        background: linear-gradient(90deg, #004D40 0%, #00695C 100%);
        padding: 20px 40px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: -5rem -5rem 2rem -5rem;
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .logo-text {
        color: white;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    .logo-subtitle {
        color: #B2DFDB;
        font-size: 14px;
        font-weight: 400;
    }
    
    /* Chat Container */
    .chat-container {
        max-width: 1400px;
        margin: 20px auto;
        padding: 30px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        min-height: 70vh;
    }
    
    /* Ensure no white overflow */
    .element-container, .stMarkdown, .stButton {
        background: transparent !important;
    }
    
    /* Upload Section */
    .upload-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
    
    .upload-title {
        color: white;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .upload-subtitle {
        color: #E8EAF6;
        font-size: 14px;
        margin-bottom: 20px;
    }
    
    /* Message Bubbles */
    .message-container {
        display: flex;
        margin: 20px 0;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message {
        justify-content: flex-end;
    }
    
    .ai-message {
        justify-content: flex-start;
    }
    
    .message-bubble {
        max-width: 70%;
        padding: 18px 24px;
        border-radius: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        line-height: 1.6;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .ai-bubble {
        background: #F5F5F5;
        color: #333;
        border-bottom-left-radius: 4px;
        border-left: 4px solid #00695C;
    }
    
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        margin: 0 12px;
        flex-shrink: 0;
    }
    
    .user-avatar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .ai-avatar {
        background: linear-gradient(135deg, #00695C 0%, #004D40 100%);
    }
    
    /* Input Section */
    .input-section {
        position: sticky;
        bottom: 20px;
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
        margin-top: 30px;
    }
    
    /* Quick Questions */
    .quick-questions {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }
    
    .quick-question-btn {
        background: white;
        border: 2px solid #00695C;
        color: #00695C;
        padding: 10px 20px;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s;
        font-size: 14px;
        font-weight: 500;
    }
    
    .quick-question-btn:hover {
        background: #00695C;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,105,92,0.3);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00695C 0%, #004D40 100%);
        color: white;
        border: none;
        padding: 12px 40px;
        border-radius: 25px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0,105,92,0.3);
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,105,92,0.4);
    }
    
    /* Loading Animation */
    .loading-dots {
        display: inline-flex;
        gap: 6px;
        padding: 20px;
    }
    
    .loading-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #00695C;
        animation: bounce 1.4s infinite ease-in-out both;
    }
    
    .loading-dot:nth-child(1) { animation-delay: -0.32s; }
    .loading-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    
    /* Blueprint Preview */
    .blueprint-preview {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        margin: 20px 0;
    }
    
    /* Stats Cards */
    .stats-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .stats-number {
        font-size: 32px;
        font-weight: 700;
        color: #00695C;
    }
    
    .stats-label {
        font-size: 14px;
        color: #666;
        margin-top: 5px;
    }
    
    /* Info Box */
    .info-box {
        background: #E8F5E9;
        border-left: 4px solid #4CAF50;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
    
    /* Text Input */
    .stTextInput>div>div>input {
        border-radius: 25px;
        border: 2px solid #E0E0E0;
        padding: 12px 20px;
        font-size: 15px;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #00695C;
        box-shadow: 0 0 0 2px rgba(0,105,92,0.1);
    }
    
    /* File Uploader */
    .stFileUploader>div>div {
        border-radius: 15px;
        border: 2px dashed #00695C;
        background: #F5F5F5;
    }
    
    /* Success Message */
    .success-message {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        margin: 15px 0;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(76,175,80,0.3);
    }
</style>
""", unsafe_allow_html=True)

# API endpoint
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'blueprint_uploaded' not in st.session_state:
    st.session_state.blueprint_uploaded = False
if 'blueprint_id' not in st.session_state:
    st.session_state.blueprint_id = None
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None


def analyze_blueprint_api(file_bytes, filename, question=None, audio_bytes=None):
    """Call FastAPI backend for blueprint analysis"""
    try:
        files = {"file": (filename, file_bytes, "image/jpeg")}
        data = {}
        
        if question:
            data["question"] = question
        
        if audio_bytes:
            files["audio"] = ("audio.wav", audio_bytes, "audio/wav")
        
        response = requests.post(
            f"{API_URL}/api/analyze-blueprint",
            files=files,
            data=data,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": response.text}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def ask_followup_api(blueprint_id, question=None, audio_bytes=None):
    """Ask follow-up question about blueprint"""
    try:
        files = {}
        data = {"blueprint_id": blueprint_id}
        
        if question:
            data["question"] = question
        
        if audio_bytes:
            files["audio"] = ("audio.wav", audio_bytes, "audio/wav")
        
        response = requests.post(
            f"{API_URL}/api/ask-followup",
            files=files if files else None,
            data=data,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": response.text}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def display_message(role, content, avatar="👤"):
    """Display a chat message"""
    if role == "user":
        st.markdown(f"""
        <div class="message-container user-message">
            <div class="message-bubble user-bubble">{content}</div>
            <div class="message-avatar user-avatar">👤</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message-container ai-message">
            <div class="message-avatar ai-avatar">🏢</div>
            <div class="message-bubble ai-bubble">{content}</div>
        </div>
        """, unsafe_allow_html=True)


def main():
    # Header
    st.markdown("""
    <div class="top-header">
        <div class="logo-section">
            <div>
                <div class="logo-text">🏢 CBRE BLUEPRINT ANALYZER</div>
                <div class="logo-subtitle">AI-Powered Architectural Intelligence</div>
            </div>
        </div>
        <div style="color: white; font-size: 14px;">
            <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px;">
                Powered by GPT-4o Vision
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Chat Container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Add extra CSS to override Streamlit defaults
    st.markdown("""
    <style>
        /* Additional override for white backgrounds */
        div[data-testid="stVerticalBlock"] > div {
            background: transparent !important;
        }
        div[data-testid="column"] {
            background: transparent !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Upload Section (if no blueprint uploaded)
    if not st.session_state.blueprint_uploaded:
        st.markdown("""
        <div class="upload-section">
            <div class="upload-title">📐 Upload Your Blueprint</div>
            <div class="upload-subtitle">Start analyzing architectural plans with AI intelligence</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            uploaded_file = st.file_uploader(
                "Drop your blueprint here",
                type=['png', 'jpg', 'jpeg', 'pdf', 'gif', 'bmp', 'tiff'],
                label_visibility="collapsed"
            )
            
            if uploaded_file:
                st.session_state.uploaded_file = uploaded_file
                st.session_state.blueprint_uploaded = True
                st.session_state.blueprint_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Display preview
                if uploaded_file.type.startswith('image'):
                    image = Image.open(uploaded_file)
                    st.markdown('<div class="blueprint-preview">', unsafe_allow_html=True)
                    st.image(image, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("""
                <div class="success-message">
                    ✅ Blueprint uploaded successfully! Ask me anything about it.
                </div>
                """, unsafe_allow_html=True)
                st.rerun()
    
    else:
        # Display uploaded blueprint info
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.session_state.uploaded_file and st.session_state.uploaded_file.type.startswith('image'):
                with st.expander("📋 View Blueprint", expanded=False):
                    image = Image.open(st.session_state.uploaded_file)
                    st.image(image, use_container_width=True)
        
        # Display chat history
        for msg in st.session_state.messages:
            display_message(msg["role"], msg["content"])
        
        # Quick Questions Section
        if len(st.session_state.messages) == 0:
            st.markdown("""
            <div style="margin: 30px 0;">
                <h3 style="color: #00695C; margin-bottom: 15px;">💡 Quick Questions</h3>
            </div>
            """, unsafe_allow_html=True)
            
            quick_questions = [
                "📏 What are the dimensions and total square footage?",
                "🏠 How many rooms are there and what types?",
                "🚪 Tell me about doors, windows, and entry points",
                "♿ What accessibility features are included?",
                "🔧 Describe the HVAC and electrical systems",
                "📐 Provide a comprehensive analysis of this blueprint"
            ]
            
            cols = st.columns(2)
            for idx, question in enumerate(quick_questions):
                with cols[idx % 2]:
                    if st.button(question, key=f"quick_{idx}", use_container_width=True):
                        process_question(question.split(" ", 1)[1] if " " in question else question)
        
        # Input Section
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Ask anything about your blueprint...",
                placeholder="e.g., How many bedrooms are there? What is the total area?",
                label_visibility="collapsed",
                key="user_input"
            )
        
        with col2:
            send_button = st.button("Send 📤", use_container_width=True)
        
        if send_button and user_input:
            process_question(user_input)
        
        # Voice input option
        if AUDIO_AVAILABLE:
            st.markdown("<br>", unsafe_allow_html=True)
            audio_bytes = audio_recorder(
                text="🎤 Or click to ask via voice",
                recording_color="#00695C",
                neutral_color="#666",
                icon_size="1x"
            )
            if audio_bytes:
                with st.spinner("Transcribing audio..."):
                    # Here you would call transcription API
                    st.info("Voice transcription in progress...")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Clear chat button
        if len(st.session_state.messages) > 0:
            if st.button("🔄 New Analysis", key="clear"):
                st.session_state.messages = []
                st.session_state.blueprint_uploaded = False
                st.session_state.blueprint_id = None
                st.session_state.uploaded_file = None
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer Stats
    if st.session_state.blueprint_uploaded:
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="stats-card">
                <div class="stats-number">🎯</div>
                <div class="stats-label">High Accuracy</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{len(st.session_state.messages)//2}</div>
                <div class="stats-label">Questions Asked</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="stats-card">
                <div class="stats-number">⚡</div>
                <div class="stats-label">Fast Analysis</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="stats-card">
                <div class="stats-number">🏢</div>
                <div class="stats-label">CBRE Powered</div>
            </div>
            """, unsafe_allow_html=True)


def process_question(question):
    """Process user question and get AI response"""
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Show loading
    with st.spinner("🤔 Analyzing blueprint..."):
        # Always use the full analysis with image for best results
        st.session_state.uploaded_file.seek(0)
        file_bytes = st.session_state.uploaded_file.read()
        
        # Build context from previous messages for follow-ups
        if len(st.session_state.messages) > 2:
            context = "Previous conversation:\n"
            for msg in st.session_state.messages[:-1]:
                if msg["role"] == "user":
                    context += f"User asked: {msg['content']}\n"
                else:
                    context += f"AI responded: {msg['content'][:200]}...\n"
            full_question = f"{context}\nNew question: {question}"
        else:
            full_question = question
        
        # Always call analyze_blueprint_api with the image
        result = analyze_blueprint_api(
            file_bytes,
            st.session_state.uploaded_file.name,
            full_question
        )
        
        if result and result.get('success'):
            response = result['analysis']
        else:
            response = f"❌ Error: {result.get('error', 'Unknown error occurred')}"
        
        # Add AI response
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()


if __name__ == "__main__":
    main()