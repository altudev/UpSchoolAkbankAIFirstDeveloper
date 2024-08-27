import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set page config
st.set_page_config(page_title="ChatGPT Chatbot", page_icon="🤖", layout="centered")

# Custom CSS for dark theme and soft look
st.markdown("""
<style>
    .stApp {
        background-color: #2b2b2b;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #3a3a3a;
        color: #ffffff;
    }
    .stButton > button {
        background-color: #4a4a4a;
        color: #ffffff;
        border-radius: 20px;
    }
    .stTextArea > div > div > textarea {
        background-color: #3a3a3a;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Initialize chat history and model choice
if "messages" not in st.session_state:
    st.session_state.messages = []
if "model" not in st.session_state:
    st.session_state.model = "gpt-4o"

# Display app title
st.title("ChatGPT Chatbot 🤖")

# Model selection
st.session_state.model = st.radio(
    "Select a model:",
    ("gpt-4o", "gpt-4o-mini"),
    horizontal=True
)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("You:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate ChatGPT response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model=st.session_state.model,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error(f"Selected Model: {st.session_state.model}")

# Add a brief description
st.markdown(f"""
This is a simple chatbot powered by OpenAI's {st.session_state.model} model. 
Feel free to ask questions or have a conversation!
""")

# Debug information
st.sidebar.title("Debug Information")
st.sidebar.write(f"API Key set: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
st.sidebar.write(f"Selected Model: {st.session_state.model}")