# frontend/utils.py
import streamlit as st
import requests
import re
import os
from datetime import datetime

API_URL = os.getenv("API_URL", "http://localhost:8000")


def initialize_session_state():
    """Initialize all session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'blueprint_uploaded' not in st.session_state:
        st.session_state.blueprint_uploaded = False
    if 'blueprint_id' not in st.session_state:
        st.session_state.blueprint_id = None
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True
    if 'auto_analyzed' not in st.session_state:
        st.session_state.auto_analyzed = False
    if 'analyzing' not in st.session_state:
        st.session_state.analyzing = False


def analyze_blueprint_api(file_bytes, filename, question=None, auto_analyze=True):
    """Call API for blueprint analysis"""
    try:
        files = {"file": (filename, file_bytes, "image/jpeg")}
        data = {"auto_analyze": str(auto_analyze).lower()}
        if question:
            data["question"] = question
        
        response = requests.post(
            f"{API_URL}/api/analyze-blueprint",
            files=files,
            data=data,
            timeout=120
        )
        
        return response.json() if response.status_code == 200 else {"success": False, "error": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}


def clean_response(response):
    """Clean up AI response by removing unwanted headers"""
    response = re.sub(r'^#+\s*Executive Summary\s*', '', response, flags=re.IGNORECASE | re.MULTILINE)
    response = re.sub(r'^Executive Summary\s*:?\s*', '', response, flags=re.IGNORECASE)
    response = re.sub(r'^#+\s*Detailed Findings\s*', '', response, flags=re.IGNORECASE | re.MULTILINE)
    response = response.lstrip('\n').strip()
    return response


def perform_auto_analysis():
    """Perform automatic comprehensive analysis on blueprint upload"""
    if st.session_state.analyzing and not st.session_state.auto_analyzed:
        # Remove the analyzing message if present
        if len(st.session_state.messages) > 0 and "Analyzing your blueprint" in st.session_state.messages[-1].get("content", ""):
            st.session_state.messages.pop()
        
        st.session_state.uploaded_file.seek(0)
        file_bytes = st.session_state.uploaded_file.read()
        
        with st.spinner("🔍 Analyzing blueprint comprehensively..."):
            result = analyze_blueprint_api(
                file_bytes,
                st.session_state.uploaded_file.name,
                question=None,
                auto_analyze=True
            )
        
        if result.get('success'):
            raw_response = result.get('analysis', 'Analysis completed')
            response = clean_response(raw_response)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"{response}\n\n---\n\n💬 **You can now ask me follow-up questions about any specific details!**"
            })
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"❌ Error analyzing blueprint: {result.get('error', 'Unknown error')}"
            })
        
        st.session_state.auto_analyzed = True
        st.session_state.analyzing = False
        st.rerun()


def trigger_auto_analysis():
    """Trigger the auto-analysis process"""
    st.session_state.analyzing = True
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "🔍 **Analyzing your blueprint...** Please wait while I perform a comprehensive analysis of all rooms, dimensions, and features."
    })
    st.rerun()


def process_question(question):
    """Process user question"""
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.spinner("🤔 Analyzing..."):
        st.session_state.uploaded_file.seek(0)
        file_bytes = st.session_state.uploaded_file.read()
        
        # Build context from previous messages
        if len(st.session_state.messages) > 2:
            context = "Previous conversation:\n"
            for msg in st.session_state.messages[:-1]:
                context += f"{msg['role']}: {msg['content'][:150]}...\n"
            full_question = f"{context}\nNew question: {question}"
        else:
            full_question = question
        
        result = analyze_blueprint_api(
            file_bytes,
            st.session_state.uploaded_file.name,
            question=full_question,
            auto_analyze=False
        )
        
        raw_response = result.get('analysis', result.get('error', 'Error occurred')) if result.get('success') else f"Error: {result.get('error', 'Unknown error')}"
        response = clean_response(raw_response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()


def reset_application():
    """Reset the application to initial state"""
    st.session_state.messages = []
    st.session_state.blueprint_uploaded = False
    st.session_state.uploaded_file = None
    st.session_state.show_welcome = True
    st.session_state.auto_analyzed = False
    st.session_state.analyzing = False
    st.rerun()