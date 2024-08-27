import streamlit as st
from .database.db_manager import DatabaseManager
from .services.chat_service import ChatService
from .config import Config

class ChatbotApp:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.db_session = self.db_manager.get_session()
        self.chat_service = ChatService(self.db_session)

    def run(self):
        st.set_page_config(
            page_title="Sketch ChatGPT",
            page_icon="✏️",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://www.example.com/help',
                'Report a bug': "https://www.example.com/bug",
                'About': "# This is a sketch-style ChatGPT app!"
            }
        )
        st.markdown('<link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap" rel="stylesheet">', unsafe_allow_html=True)
        self._set_custom_css()

        st.title("Sketch ChatGPT ✏️")

        if "model" not in st.session_state:
            st.session_state.model = "gpt-4o"
        st.session_state.model = st.selectbox(
            "Select a model:",
            ("gpt-4o", "gpt-4o-mini")
        )

        chat_history = self.chat_service.get_chat_history()
        for message in chat_history:
            with st.chat_message(message.role):
                st.markdown(message.content)

        if prompt := st.chat_input("You:"):
            user_message = self.chat_service.save_message("user", prompt, st.session_state.model)
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                try:
                    response = self.chat_service.generate_response(chat_history + [user_message], st.session_state.model)
                    message_placeholder.markdown(response)
                    self.chat_service.save_message("assistant", response, st.session_state.model)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

        st.markdown(f"""
        This is a simple chatbot powered by OpenAI's {st.session_state.model} model. 
        Feel free to ask questions or have a conversation!
        """)

        self._show_debug_info()

    def _set_custom_css(self):
        st.markdown("""
        <style>
            /* Sketch-style dark theme */
            .stApp {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: 'Comic Sans MS', cursive, sans-serif;
            }
            /* Sketch-style chat bubbles */
            .stChatMessage {
                background-color: #3a3a3a;
                border: 3px solid #ffffff;
                border-radius: 15px;
                padding: 10px;
                margin: 5px 0;
                position: relative;
                overflow: visible;
            }
            .stChatMessage::before {
                content: '';
                position: absolute;
                bottom: -10px;
                left: 20px;
                border-width: 10px 10px 0;
                border-style: solid;
                border-color: #ffffff transparent;
            }
            .stChatMessage.user {
                background-color: #4a4a4a;
            }
            .stChatMessage.user::before {
                left: auto;
                right: 20px;
            }
            /* Sketch-style input */
            .stChatInputContainer {
                border: 3px solid #ffffff;
                border-radius: 20px;
                padding: 5px;
                background-color: #3a3a3a;
            }
            .stChatInputContainer:focus-within {
                box-shadow: 0 0 10px #ffffff;
            }
            .stChatInput {
                background-color: transparent !important;
                border: none !important;
                padding: 10px !important;
                color: #ffffff !important;
                font-family: 'Comic Sans MS', cursive, sans-serif !important;
            }
            /* Sketch-style title */
            h1 {
                font-family: 'Permanent Marker', cursive;
                text-shadow: 2px 2px #4a4a4a;
                letter-spacing: 2px;
                transform: rotate(-2deg);
                display: inline-block;
            }
            /* Sketch-style selectbox */
            .stSelectbox {
                border: 3px solid #ffffff;
                border-radius: 10px;
                background-color: #3a3a3a;
            }
            .stSelectbox > div > div {
                background-color: #3a3a3a !important;
                color: #ffffff !important;
            }
        </style>
        """, unsafe_allow_html=True)

    def _show_debug_info(self):
        st.sidebar.title("Debug Information")
        st.sidebar.write(f"API Key set: {'Yes' if Config.OPENAI_API_KEY else 'No'}")
        st.sidebar.write(f"Selected Model: {st.session_state.model}")