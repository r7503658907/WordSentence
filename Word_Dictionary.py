import streamlit as st
from langchain_groq import ChatGroq
import re
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def translate_hindi_to_english(hindi_word):
    llm = ChatGroq(
        model="mixtral-8x7b-32768",
        temperature=0,
        groq_api_key=GROQ_API_KEY
    )

    prompt = f"""
    Hindi word: {hindi_word}

    1. Correct the spelling if needed.
    2. Provide the correct English translation.
    3. Provide the English pronunciation in IPA format specifically for the English word.
    4. Generate five example sentences in both Hindi and English.

    Output format:
    - Hindi word: [Correct Hindi]
    - English translation: [English Word]
    - Pronunciation (English word): /IPA Format/
    - Sentences:
      1. [Hindi sentence]
         [English sentence]
      2. ...
      3. ...
      4. ...
      5. ...
    """

    response = llm.invoke(prompt)

    # Extract only the content from the response
    content = response.content if hasattr(response, "content") else response

    # Remove unwanted sentences dynamically
    unwanted_patterns = [
        r"Main apne abhilochan ko pura karna chahta hoon.*",  # Example unwanted sentence
        r"\(.*?\)",  # Removes any extra Hindi transliteration in parentheses
    ]

    for pattern in unwanted_patterns:
        content = re.sub(pattern, "", content, flags=re.MULTILINE)

    return content.strip()


# Streamlit UI
st.title("Hindi to English Translator")
hindi_word = st.text_input("Enter a Hindi word:")

if st.button("Translate"):
    if hindi_word:
        output = translate_hindi_to_english(hindi_word)
        st.text_area("Translation Result:", output, height=300)
    else:
        st.warning("Please enter a Hindi word.")
