import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import tempfile

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Streamlit app
st.title("Audio Transcription and Translation")

# File uploader
audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

# Language selection
language = st.text_input("Enter the language for translation:")

# Function to save uploaded file temporarily
def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    return None

# Process button
if st.button("Transcribe and Translate") and audio_file is not None and language:
    with st.spinner("Processing audio..."):
        try:
            # Save uploaded file
            temp_audio_path = save_uploaded_file(audio_file)

            # Transcribe audio
            with open(temp_audio_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="srt"
                )

            st.success("Audio transcribed successfully!")

            # Translate transcription
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a very helpful and talented translator who can translate all languages and srt files."},
                    {"role": "user", "content": f"Could you please translate the .srt text below to {language}? Do not add any comments of yours only the translation. "
                                                f"Please do not change the timestamps and structure of the file.\n<Transcription>{transcription}</Transcription>"}
                ]
            )

            translated_srt = response.choices[0].message.content

            st.success("Translation completed!")

            # Display translated subtitles
            st.subheader("Translated Subtitles")
            st.text_area("SRT Content", translated_srt, height=300)

            # Download button for translated SRT
            st.download_button(
                label="Download Translated SRT",
                data=translated_srt,
                file_name="translated_subtitles.srt",
                mime="text/plain"
            )

            # Clean up temporary file
            os.unlink(temp_audio_path)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Instructions
st.sidebar.header("Instructions")
st.sidebar.markdown("""
1. Upload an audio file (mp3, wav, or m4a format).
2. Enter the desired language for translation.
3. Click 'Transcribe and Translate' to process the audio.
4. View the translated subtitles and download the SRT file.
""")