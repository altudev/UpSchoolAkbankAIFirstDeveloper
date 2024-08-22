import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Streamlit app
st.title("DALL-E Image Generator")

# Sidebar for settings
st.sidebar.header("Settings")

# Model selection
model = st.sidebar.selectbox("Select Model", ["dall-e-2", "dall-e-3"])

# Size selection
size = st.sidebar.selectbox("Select Image Size", ["256x256", "512x512", "1024x1024"])

# Number of images
n = st.sidebar.slider("Number of Images", min_value=1, max_value=5, value=1)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_url" in message:
            st.image(message["image_url"])

# Chat input
prompt = st.chat_input("Enter your image prompt...")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate image
    with st.chat_message("assistant"):
        with st.spinner("Generating image..."):
            try:
                response = client.images.generate(
                    model=model,
                    prompt=prompt,
                    size=size,
                    quality="standard",
                    n=n,
                )

                for i, image_data in enumerate(response.data):
                    image_url = image_data.url
                    st.image(image_url, caption=f"Generated Image {i + 1}")
                    st.markdown(f"[Download Image {i + 1}]({image_url})")

                # Add assistant message to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Here {'are' if n > 1 else 'is'} your generated image{'s' if n > 1 else ''}:",
                    "image_url": [img.url for img in response.data]
                })

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()