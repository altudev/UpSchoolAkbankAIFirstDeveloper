import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Streamlit app
st.title("Enhanced Gift Recommendation System")

# User input form
st.header("Gift Recipient Information")

relation = st.selectbox(
    "Relationship to recipient",
    ["Relative", "Friend", "Family", "Sibling", "Colleague", "Partner"]
)

country = st.text_input("Recipient's country")

hobbies = st.text_area("Recipient's hobbies (comma-separated)")

gender = st.radio("Recipient's gender", ["Male", "Female", "Other"])

age = st.number_input("Recipient's age", min_value=0, max_value=120, value=30)

budget = st.slider("Budget for the gift ($)", 0, 1000, 50)

# Color selection
colors = [
    "Red", "Blue", "Green", "Yellow", "Purple", "Pink", "Orange", "Black",
    "White", "Gray", "Brown", "Turquoise", "Gold", "Silver", "Lavender"
]
selected_colors = st.multiselect("Select preferred colors", colors, default=["Blue", "Green"])

# Initialize messages in session state if not present
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system",
         "content": "You are a helpful gift recommendation assistant with knowledge of global cultures and gift-giving traditions. Provide gift suggestions based on the information given about the recipient, including their country and color preferences. Format your response as a markdown table with 5 gift ideas. The table should have five columns: 'Gift Idea', 'Price Range', 'Why It's a Good Fit', 'Cultural Relevance', and 'Where to Buy'. Keep descriptions concise but informative, especially regarding cultural aspects."}
    ]

# Button to generate recommendations
if st.button("Get Gift Recommendations"):
    # Prepare the user message
    user_message = f"""
    Please suggest gift ideas for a {age}-year-old {gender.lower()} {relation.lower()} living in {country} with the following hobbies: {hobbies}.
    The budget for the gift is ${budget}.
    The preferred colors are: {', '.join(selected_colors)}.
    Consider the cultural norms and gift-giving traditions of {country} in your recommendations.
    Present your recommendations in a markdown table format with five columns: 'Gift Idea', 'Price Range', 'Why It's a Good Fit', 'Cultural Relevance', and 'Where to Buy'.
    In the 'Where to Buy' column, suggest 1-2 popular online retailers or specialized stores in {country} where the item can be purchased at a competitive price.
    Ensure that at least some of the gift ideas incorporate the preferred colors when appropriate.
    """

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_message})

    try:
        # Generate recommendations using OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
        )

        recommendations = completion.choices[0].message.content

        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": recommendations})

        # Display recommendations
        st.header("Gift Recommendations")
        st.markdown(recommendations)

        # Save recommendations to file
        with open('gift_recommendations.md', 'w') as f:
            f.write(recommendations)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Display saved recommendations
st.header("Previous Recommendations")
try:
    with open('gift_recommendations.md', 'r') as f:
        st.markdown(f.read())
except FileNotFoundError:
    st.write("No previous recommendations found.")