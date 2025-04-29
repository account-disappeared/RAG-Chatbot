import streamlit as st
from sidebar import display_sidebar
from chat_interface import display_chat_interface
from translations import get_text, available_languages
from language_detection import detect_browser_language

# Initialize session state for messages and session ID
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

# Detect and set language only once
if "language" not in st.session_state:
    # Detect browser language with a unique key
    browser_language = detect_browser_language(key="browser_language_initial")

    # Extract the primary language code
    primary_language = browser_language.split('-')[0].lower()

    # Set to detected language if supported, otherwise default to English
    if primary_language in available_languages:
        st.session_state.language = primary_language
    else:
        st.session_state.language = "en"

    # Store the detected browser language for display
    st.session_state.detected_browser_language = browser_language

# Set page title according to selected language
st.title(get_text("app_title", st.session_state.language))

# Display the sidebar
display_sidebar()

# Display the chat interface
display_chat_interface()
