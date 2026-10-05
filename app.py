import streamlit as st
from dotenv import load_dotenv
import requests
import os

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="AI Q&A Chatbot",
    page_icon="🤖"
)

# Title
st.title("🤖 AI Q&A Chatbot")
st.write("Ask me anything!")

# Question input
question = st.text_input(
    "Enter your question:",
    placeholder="Example: Explain inheritance in Java"
)

# Ask button
if st.button("Ask"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    elif not API_KEY:
        st.error("Gemini API key is missing. Please check your .env file.")

    else:

        # Gemini 3.5 Flash Lite
        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-3.5-flash-lite:generateContent"
        )

        # Request headers
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": API_KEY
        }

        # Data sent to Gemini
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": question
                        }
                    ]
                }
            ]
        }

        try:

            # Send request
            response = requests.post(
                url,
                headers=headers,
                json=data
            )

            # Successful response
            if response.status_code == 200:

                result = response.json()

                answer = (
                    result["candidates"][0]
                    ["content"]["parts"][0]["text"]
                )

                st.success("Answer:")
                st.write(answer)

            # API error
            else:

                st.error(
                    f"Gemini API Error: {response.status_code}"
                )

                st.write(response.text)

        except Exception as e:

            st.error("Something went wrong:")
            st.write(str(e))