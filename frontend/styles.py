# frontend/styles.py

def get_styles():
    """Return all CSS styles for the application"""
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* ========== CRITICAL: REMOVE ALL GAPS AND PADDING ========== */
    #MainMenu, footer, header {visibility: hidden;}
    .main, .block-container, .stApp, [data-testid="stAppViewContainer"] {
        background: #0a0e27 !important;
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    section.main > div {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    
    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        gap: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    [data-testid="column"] {
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    div[data-testid="column"]:first-child {
        padding-right: 0 !important;
        margin: 0 !important;
    }
    
    div[data-testid="column"]:last-child {
        padding-left: 0 !important;
        margin: 0 !important;
    }
    
    .row-widget.stHorizontal {
        gap: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    div.row-widget.stHorizontal > div {
        gap: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .stHorizontal {
        margin: 0 !important;
        padding: 0 !important;
        gap: 0 !important;
    }
    
    /* Top Header */
    .cbre-header {
        background: linear-gradient(135deg, #00695C 0%, #004D40 100%);
        padding: 20px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        position: sticky;
        top: 0;
        z-index: 1000;
        margin: 0 !important;
    }
    
    .logo-area {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .logo-icon {
        font-size: 36px;
    }
    
    .logo-text h1 {
        color: white;
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.5px;
    }
    
    .logo-text p {
        color: #B2DFDB;
        font-size: 13px;
        margin: 0;
    }
    
    .header-badge {
        background: rgba(255,255,255,0.15);
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }
    
    /* Left Panel - Blueprint Viewer */
    .left-panel {
        background: #1a1f3a;
        border-right: 2px solid #2d3454;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        height: calc(100vh - 80px);
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .blueprint-header {
        padding: 20px;
        background: #232946;
        border-bottom: 1px solid #2d3454;
    }
    
    .blueprint-header h3 {
        color: #00BFA5;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0;
    }
    
    .blueprint-viewer {
        flex: 1;
        overflow: auto;
        padding: 20px;
        background: #1a1f3a;
    }
    
    .blueprint-image {
        width: 100%;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        cursor: zoom-in;
        transition: transform 0.3s;
    }
    
    .blueprint-image:hover {
        transform: scale(1.02);
    }
    
    /* Right Panel - Chat Interface */
    .right-panel {
        flex: 1;
        display: flex;
        flex-direction: column;
        background: #0a0e27;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 30px;
        background: #0a0e27;
    }
    
    /* Welcome Screen */
    .welcome-screen {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        padding: 40px;
        text-align: center;
    }
    
    .welcome-icon {
        font-size: 80px;
        margin-bottom: 20px;
    }
    
    .welcome-title {
        color: white;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .welcome-subtitle {
        color: #8b92b5;
        font-size: 16px;
        margin-bottom: 30px;
        line-height: 1.6;
    }
    
    .upload-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 40px;
        max-width: 500px;
        width: 100%;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
    }
    
    .upload-title {
        color: white;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .upload-desc {
        color: rgba(255,255,255,0.9);
        font-size: 14px;
        margin-bottom: 25px;
    }
    
    .analyzing-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        text-align: center;
        color: white;
        font-size: 16px;
        font-weight: 600;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Message Bubbles */
    .message {
        display: flex;
        margin-bottom: 25px;
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
    
    .message.user {
        justify-content: flex-end;
    }
    
    .message.assistant {
        justify-content: flex-start;
    }
    
    .message-content {
        max-width: 70%;
        display: flex;
        gap: 12px;
        align-items: flex-start;
    }
    
    .message.user .message-content {
        flex-direction: row-reverse;
    }
    
    .avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .avatar.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .avatar.assistant {
        background: linear-gradient(135deg, #00BFA5 0%, #00897B 100%);
    }
    
    .bubble {
        padding: 16px 20px;
        border-radius: 18px;
        line-height: 1.6;
        font-size: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 100%;
    }
    
    .bubble.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .bubble.assistant {
        background: #232946;
        color: #e4e7f1;
        border-bottom-left-radius: 4px;
        border-left: 3px solid #00BFA5;
    }
    
    .quick-questions {
        padding: 20px 30px;
        background: #1a1f3a;
        border-top: 1px solid #2d3454;
        margin-top: 0 !important;
    }
    
    .quick-questions-title {
        color: #00BFA5;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
    }
    
    .input-area {
        padding: 20px 30px;
        background: #232946;
        border-top: 2px solid #2d3454;
        margin-top: 0 !important;
    }
    
    .stTextInput {
        margin-bottom: 0 !important;
    }
    
    .stTextInput > div > div {
        background: #1a1f3a !important;
        border: 2px solid #2d3454 !important;
        border-radius: 25px !important;
        padding: 4px 20px !important;
    }
    
    .stTextInput > div > div:focus-within {
        border-color: #00BFA5 !important;
        box-shadow: 0 0 0 3px rgba(0,191,165,0.15) !important;
    }
    
    .stTextInput input {
        background: transparent !important;
        border: none !important;
        color: white !important;
        font-size: 15px !important;
        padding: 12px 0 !important;
        height: auto !important;
    }
    
    .stTextInput input::placeholder {
        color: #6b7280 !important;
        opacity: 1 !important;
    }
    
    .stTextInput input:focus {
        box-shadow: none !important;
        outline: none !important;
        background: transparent !important;
    }
    
    .stTextInput label {
        display: none !important;
    }
    
    .stButton {
        margin: 0 !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #00BFA5 0%, #00897B 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 28px !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 12px rgba(0,191,165,0.3) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,191,165,0.4) !important;
    }
    
    [data-testid="stFileUploader"] {
        background: transparent;
    }
    
    [data-testid="stFileUploader"] > div {
        border: 2px dashed rgba(255,255,255,0.3) !important;
        border-radius: 15px !important;
        background: rgba(255,255,255,0.05) !important;
        padding: 30px !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: white !important;
        font-size: 15px !important;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1f3a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2d3454;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #3d4464;
    }
    
    .stSpinner > div {
        border-color: #00BFA5 transparent transparent transparent !important;
    }

    
</style>
"""