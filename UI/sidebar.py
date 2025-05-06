import streamlit as st
from api_utils import upload_document, list_documents, delete_document
from translations import get_text, available_languages


def display_sidebar():
    # Use stored browser language instead of detecting again
    if "detected_browser_language" in st.session_state:
        browser_language = st.session_state.detected_browser_language
        primary_language = browser_language.split('-')[0].lower()
    else:
        primary_language = "en"

    # Language selector
    st.sidebar.header(get_text("select_language", st.session_state.language))

    # Create language options with full names
    language_names = {
        "en": "English",
        "fr": "Français",
        "zh": "简体中文",
        "es": "Español",
        "it": "Italiano",
        "de": "Deutsch",
        "ja": "日本語",
    }

    # Display language options
    languages = list(language_names.keys())
    selected_index = languages.index(st.session_state.language) if st.session_state.language in languages else 0

    selected_language = st.sidebar.selectbox(
        "Language",
        options=languages,
        index=selected_index,
        format_func=lambda x: language_names[x],
        label_visibility="collapsed"
    )

    # Show auto-detection info
    if primary_language in available_languages:
        display_language = language_names.get(primary_language, primary_language)
        st.sidebar.caption(
            get_text("auto_detected", st.session_state.language, browser_lang=display_language)
        )

    # Update language when selection changes
    if st.session_state.language != selected_language:
        st.session_state.language = selected_language
        st.rerun()

    # Sidebar: Model Selection
    model_options = ["Gemma3"]
    st.sidebar.selectbox(
        get_text("select_model", st.session_state.language),
        options=model_options,
        key="model"
    )

    # Sidebar: Upload Document
    st.sidebar.header(get_text("upload_document", st.session_state.language))
    uploaded_file = st.sidebar.file_uploader(
        get_text("choose_file", st.session_state.language),
        type=["pdf", "docx", "txt"]
    )
    if uploaded_file is not None:
        if st.sidebar.button(get_text("upload_button", st.session_state.language)):
            with st.spinner(get_text("uploading", st.session_state.language)):
                upload_response = upload_document(uploaded_file)
                if upload_response:
                    st.sidebar.success(
                        get_text(
                            "upload_success",
                            st.session_state.language,
                            filename=uploaded_file.name,
                            file_id=upload_response['file_id']
                        )
                    )
                    st.session_state.documents = list_documents()  # Refresh the list after upload

    # Sidebar: List Documents
    st.sidebar.header(get_text("uploaded_documents", st.session_state.language))
    if st.sidebar.button(get_text("refresh_documents", st.session_state.language)):
        with st.spinner(get_text("refreshing", st.session_state.language)):
            st.session_state.documents = list_documents()

    # Initialize document list if not present
    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()

    documents = st.session_state.documents
    if documents:
        for doc in documents:
            st.sidebar.text(f"{doc['filename']} (ID: {doc['id']}, Uploaded: {doc['upload_timestamp']})")

        # Delete Document
        selected_file_id = st.sidebar.selectbox(
            get_text("select_to_delete", st.session_state.language),
            options=[doc['id'] for doc in documents],
            format_func=lambda x: next(doc['filename'] for doc in documents if doc['id'] == x)
        )
        if st.sidebar.button(get_text("delete_button", st.session_state.language)):
            with st.spinner(get_text("deleting", st.session_state.language)):
                delete_response = delete_document(selected_file_id)
                if delete_response:
                    st.sidebar.success(
                        get_text(
                            "delete_success",
                            st.session_state.language,
                            file_id=selected_file_id
                        )
                    )
                    st.session_state.documents = list_documents() # Refresh the list after deletion
                    st.rerun() #refresh UI to reflect the change
                else:
                    st.sidebar.error(
                        get_text(
                            "delete_error",
                            st.session_state.language,
                            file_id=selected_file_id
                        )
                    )
