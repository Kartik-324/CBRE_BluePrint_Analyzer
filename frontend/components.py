# frontend/components.py
import streamlit as st
from PIL import Image
from datetime import datetime
from utils import process_question, reset_application


def render_header():
    """Render the CBRE header"""
    st.markdown("""
    <div class="cbre-header">
        <div class="logo-area">
            <div class="logo-icon">🏢</div>
            <div class="logo-text">
                <h1>CBRE BLUEPRINT ANALYZER</h1>
                <p>AI-Powered Architectural Intelligence</p>
            </div>
        </div>
        <div class="header-badge">Powered by GPT-4o Vision</div>
    </div>
    """, unsafe_allow_html=True)


def render_welcome_screen():
    """Render the welcome screen with file uploader"""
    st.markdown("""
    <div class="welcome-screen">
        <div class="welcome-icon">📐</div>
        <h1 class="welcome-title">Welcome to CBRE Blueprint Analyzer</h1>
        <p class="welcome-subtitle">
            Upload your architectural blueprint to start analyzing with AI.<br>
            Get instant comprehensive insights on rooms, dimensions, features, and more.
        </p>
        <div class="upload-box">
            <div class="upload-title">📤 Upload Your Blueprint</div>
            <div class="upload-desc">Supports JPG, PNG, PDF, and more<br>Automatic analysis will begin immediately</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_file = st.file_uploader(
            "Choose file",
            type=['png', 'jpg', 'jpeg', 'pdf', 'gif', 'bmp', 'tiff'],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file
            st.session_state.blueprint_uploaded = True
            st.session_state.blueprint_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.session_state.show_welcome = False
            st.session_state.auto_analyzed = False
            st.rerun()


def render_blueprint_panel():
    """Render the left panel with blueprint viewer"""
    st.markdown('<div class="left-panel">', unsafe_allow_html=True)
    st.markdown("""
        <div class="blueprint-header">
            <h3>📋 Blueprint View</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="blueprint-viewer">', unsafe_allow_html=True)
    
    if st.session_state.uploaded_file:
        try:
            image = Image.open(st.session_state.uploaded_file)
            st.image(image, width='stretch', output_format="PNG")
        except:
            st.error("Could not display image")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 New Analysis", key="new_analysis", use_container_width=True):
        reset_application()
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_loading_screen():
    """Render beautiful loading animation during analysis"""
    st.markdown("""
    <div class="loading-container">
        <div class="loading-content">
            <div class="loading-spinner">
                <div class="spinner-ring"></div>
                <div class="spinner-ring"></div>
                <div class="spinner-ring"></div>
                <div class="blueprint-icon">📐</div>
            </div>
            <h2 class="loading-title">Analyzing Your Blueprint</h2>
            <p class="loading-subtitle">AI is examining rooms, dimensions, and architectural features...</p>
            <div class="loading-steps">
                <div class="step active">
                    <div class="step-icon">🔍</div>
                    <div class="step-text">Scanning Blueprint</div>
                </div>
                <div class="step active">
                    <div class="step-icon">📏</div>
                    <div class="step-text">Measuring Dimensions</div>
                </div>
                <div class="step active">
                    <div class="step-icon">🏠</div>
                    <div class="step-text">Identifying Rooms</div>
                </div>
                <div class="step active">
                    <div class="step-icon">✨</div>
                    <div class="step-text">Generating Report</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_chat_panel():
    """Render the right panel with chat interface"""
    st.markdown('<div class="right-panel">', unsafe_allow_html=True)
    
    # Show beautiful loading screen during analysis
    if st.session_state.analyzing:
        render_loading_screen()
    
    # Chat messages area
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        render_message(msg)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick questions
    if st.session_state.auto_analyzed and len(st.session_state.messages) == 1:
        render_quick_questions()
    
    # Input area
    if st.session_state.auto_analyzed:
        render_input_area()
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_message(msg):
    """Render a single message bubble"""
    role_class = "user" if msg["role"] == "user" else "assistant"
    avatar_emoji = "👤" if msg["role"] == "user" else "🏢"
    
    st.markdown(f"""
    <div class="message {role_class}">
        <div class="message-content">
            <div class="avatar {role_class}">{avatar_emoji}</div>
            <div class="bubble {role_class}">{msg["content"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_quick_questions():
    """Render quick question buttons"""
    st.markdown("""
    <div class="quick-questions">
        <div class="quick-questions-title">💡 Quick Follow-up Questions</div>
    """, unsafe_allow_html=True)
    
    quick_questions = [
        "Tell me more about bedroom dimensions",
        "Details on bathroom fixtures",
        "Kitchen layout and appliances",
        "What about storage spaces?",
        "HVAC and electrical details",
        "Accessibility features"
    ]
    
    cols = st.columns(3)
    for idx, q in enumerate(quick_questions):
        with cols[idx % 3]:
            if st.button(q, key=f"q_{idx}", use_container_width=True):
                process_question(q)
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_input_area():
    """Render the chat input area"""
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    
    with st.form(key='chat_form', clear_on_submit=True):
        input_col, button_col = st.columns([5, 1])
        
        with input_col:
            user_input = st.text_input(
                "user_message",
                placeholder="Ask follow-up questions about the blueprint...",
                label_visibility="collapsed",
                key="user_input_form"
            )
        
        with button_col:
            send = st.form_submit_button("Send 📤")
        
        if send and user_input:
            process_question(user_input)
    
    st.markdown('</div>', unsafe_allow_html=True)