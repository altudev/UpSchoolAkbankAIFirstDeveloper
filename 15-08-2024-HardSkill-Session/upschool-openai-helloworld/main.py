import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Streamlit app
st.title("Lipstick Stylist Assistant")

skin_tone = "Wheatish"
occasion = "Party"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system",
         "content": "You are a helpful lipstick stylist and assistant. You know the best about the latest trends and can help customers find the perfect shade. Use your imagination to create the top 5 colourful choices, Keep it short and concise. Give the responses in a list format in a **MARKDOWN** format! Do not include anything else in your responses. Create the response for following specifications:" + f"Skin Tone:{skin_tone}\n\nOccasion:{occasion}"}
    ]

# Display chat messages
for message in st.session_state.messages[1:]:  # Skip the system message
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask about lipstick trends or shades...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
        )

        response = completion.choices[0].message.content
        message_placeholder.markdown(response)

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Write response to file
    with open('response.md', 'w') as f:
        f.write(response)

# Add a section for displaying the contents of response.md
st.subheader("Latest Response")
try:
    with open('response.md', 'r') as f:
        st.markdown(f.read())
except FileNotFoundError:
    st.write("No response generated yet.")