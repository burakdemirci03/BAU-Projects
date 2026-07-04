import os
import uuid
import streamlit as st
from chatbot import Chatbot

languages = {
    "English": "English",
    "Türkçe": "Türkçe",
    "Deutsch": "Deutsch",
    "Français": "Français",
    "Italiano": "Italiano",
    "Español": "Español",
    "日本語": "日本語",
}
    
# ---------- Session ID Generation ---------- #
def session_id():
    return str(uuid.uuid4()).upper()


# ---------- Custom CSS Implementation ---------- #
def apply_custom_css():
    st.markdown("""
        <style>
            [data-testid="stChatMessage"] {
                border: 1.5px solid #e0e0e0;
                border-radius: 15px;
                padding: 10px;
                margin-bottom: 10px;
                transition: all 0.3s ease;
            }

            [data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {
                flex-direction: row-reverse;
                text-align: right;
                background-color: #1a1f29; 
                border-color: #2d3545;
            }

            [data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) {
                background-color: #171b24;
                border-color: #2a3242;
                text-align: left;
            }

            [data-testid="stChatMessage"]:has(.violation-container) {
                background-color: #451a1a !important;
                border: 2px solid #ff4b4b !important;
            }
            
            .violation-container {
                color: #ff4b4b !important;
                font-weight: bold;
                display: block;
                width: 100%;
                text-align: left;
            }

            [data-testid="stChatMessageContent"] {
                width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)


# ---------- Page Configuration ---------- #
st.set_page_config(page_title="RAG Assistant", layout="centered")
st.title("AI Assistant")
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4()).upper()
id = st.session_state.session_id
apply_custom_css()


# ---------- Chatbot Initialization ---------- #
if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot()


# ---------- History Management ---------- #
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    stored_history = st.session_state.chatbot.read_history()
    
    for chat in stored_history:
        st.session_state.messages.append({"role": "user", "content": chat["user"]})
        st.session_state.messages.append({"role": "assistant", "content": chat["assistant"]})

# ---------- Sidebar Controls ---------- #
with st.sidebar:
    st.header("Model Configurations")
    
    # Slider for k (Number of retrieved chunks)
    k_value = st.slider(
        "Retrieval Count (k)", 
        min_value=1, 
        max_value=10, 
        value=4,
        help="Number of document chunks to retrieve for context (default: 4)."
    )
    
    # Slider for n (Conversation history buffer)
    n_value = st.slider(
        "History Buffer (n)", 
        min_value=0, 
        max_value=10, 
        value=5,
        help="Number of previous interactions the AI should remember (default: 5)."
    )

    # Dropdown for response language
    selected_lang = st.selectbox(
        "Response Language",
        options=list(languages.keys()),
        index=0,
        help="The language the AI will use to respond."
    )
    
    st.divider()

    st.header("Extract Knowledge")
    
    # File uploader for text files
    uploaded_files = st.file_uploader(
        "Choose text files", 
        type="txt", 
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("Load to the Database"):
            with st.status("Extracting and Indexing...", expanded=True) as status:
                for uploaded_file in uploaded_files:
                    st.write(f"Processing: {uploaded_file.name}")
                    st.session_state.chatbot.extract_txt(uploaded_file)
                
                status.update(label="Index Updated Successfully!", state="complete", expanded=False)
            st.success(f"Successfully processed {len(uploaded_files)} files.")

    st.divider()

    st.header("Delete Chat History")

    # Clear history button
    if st.button("Clear History"):
        st.session_state.chatbot.clear_history()
        st.session_state.messages = []
        st.success("Chat history cleared.")

# ---------- Display Chat History on UI ---------- #
for message in st.session_state.messages:
    icon = "👤" if message["role"] == "user" else "🧠"
    with st.chat_message(message["role"], avatar=icon):
        if "INJECTION PROTECTION GUARDRAILS VIOLATED" in message["content"]:
            st.markdown(f'<div class="violation-container">⚠️ {message["content"]}</div>', 
                        unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# ---------- Chatbot Logic ---------- #
if prompt := st.chat_input("Ask a question based on the context..."):
    # Display user message immediately
    st.chat_message("user", avatar="👤").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate and display assistant response
    with st.chat_message("assistant", avatar="🧠"):
        with st.spinner("Searching documents..."):
            response = st.session_state.chatbot.chat(prompt,
                                                     id=id,
                                                     k=k_value,
                                                     n_history=n_value,
                                                     language=languages[selected_lang])

            # Display response with guardrail violation styling
            if "INJECTION PROTECTION GUARDRAILS VIOLATED" in response:
                st.markdown(f'<div class="violation-container">⚠️ {response}</div>', 
                            unsafe_allow_html=True)
            else:
                st.markdown(response)

    # Update session state messages
    st.session_state.messages.append({"role": "assistant", "content": response})