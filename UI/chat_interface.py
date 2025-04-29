# chat_interface.py
import streamlit as st
from api_utils import get_api_response
from translations import get_text


def display_chat_interface():
    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(get_text("chat_placeholder", st.session_state.language)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner(get_text("generating", st.session_state.language)):
            response = get_api_response(prompt, st.session_state.session_id, st.session_state.model)

            if response:
                st.session_state.session_id = response.get('session_id')
                st.session_state.messages.append({"role": "assistant", "content": response['answer']})

                with st.chat_message("assistant"):
                    st.markdown(response['answer'])

                    with st.expander(get_text("details", st.session_state.language)):
                        st.subheader(get_text("generated_answer", st.session_state.language))
                        st.code(response['answer'])
                        st.subheader(get_text("model_used", st.session_state.language))
                        st.code(response['model'])
                        st.subheader(get_text("session_id", st.session_state.language))
                        st.code(response['session_id'])
            else:
                st.error(get_text("api_error", st.session_state.language))
