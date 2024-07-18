import openai
import os

# Function to get response from OpenAI API
def get_openai_response(prompt, api_key):
    """
    Send a prompt to OpenAI API and get the response.

    Parameters:
    prompt (str): The input prompt from the user.
    api_key (str): The OpenAI API key for authentication.

    Returns:
    str: The response from the OpenAI API.
    """
    # Create a client instance
    client = openai.OpenAI(api_key=api_key)

    # Call the OpenAI API with the given prompt
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Specify the ChatGPT model
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract and return the text part of the response
    return response.choices[0].message.content.strip()

def append_response_to_file(response, file_path):
    """
    Append the AI response to a file. Create the file if it does not exist.

    Parameters:
    response (str): The response from the OpenAI API.
    file_path (str): The path to the file where responses should be appended.
    """
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            # Create the file if it does not exist
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("AI Responses Log\n")
                file.write("================\n")

        # Append the response to the file
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"{response}\n")

    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

def main():
    """
    Main function to run the console application.
    """
    # Read the API key from a text file which is located in the same folder with main.py
    with open("api_key.txt", 'r') as file:
        api_key = file.read().strip()

    # Path to the file where responses will be appended
    file_path = "ai_responses.txt"

    # Continue to prompt the user for input until they choose to exit
    while True:
        # Read the prompt from the console
        user_input = input("Enter your prompt (or type 'exit' to quit): ")

        # Exit the loop if the user types 'exit'
        if user_input.lower() == 'exit':
            print("Exiting the application.")
            break

        try:
            # Get the response from OpenAI API
            response = get_openai_response(user_input, api_key)

            # Print the response to the console
            print(f"Response: {response}")

            # Append the response to the file
            append_response_to_file(response, file_path)

        except openai.APIError as e:
            print(f"An error occurred: {e}")

# Entry point of the script
if __name__ == "__main__":
    main()