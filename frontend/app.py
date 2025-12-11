# frontend/app.py
import streamlit as st
from styles import get_styles
from components import (
    render_header, 
    render_welcome_screen, 
    render_blueprint_panel, 
    render_chat_panel
)
from utils import (
    initialize_session_state, 
    perform_auto_analysis, 
    trigger_auto_analysis
)

# Page configuration
st.set_page_config(
    page_title="CBRE Blueprint Analyzer",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply styles
st.markdown(get_styles(), unsafe_allow_html=True)

# Initialize session state
initialize_session_state()


def main():
    """Main application logic"""
    # Render header
    render_header()
    
    # Main content
    if not st.session_state.blueprint_uploaded:
        # Show welcome screen
        render_welcome_screen()
    else:
        # Perform auto-analysis if needed
        if st.session_state.analyzing and not st.session_state.auto_analyzed:
            perform_auto_analysis()
        
        # Trigger auto-analysis on first load after upload
        if not st.session_state.auto_analyzed and not st.session_state.analyzing:
            trigger_auto_analysis()
        
        # Split screen layout
        left_col, right_col = st.columns([1, 2])
        
        with left_col:
            render_blueprint_panel()
        
        with right_col:
            render_chat_panel()


if __name__ == "__main__":
    main()