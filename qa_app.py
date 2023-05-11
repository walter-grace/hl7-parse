import streamlit as st
from dotenv import load_dotenv
import os
import openai

load_dotenv()
model_engine = "gpt-3.5-turbo-0301"

openai.api_key = os.getenv('OPENAI_API_KEY')

def parse_hl7_message(hl7_message):
    prompt = f"""
        I am a highly intelligent AI that understands HL7 messages. I can parse and present the information in an organized and human-readable format. Given an HL7 message, I will extract the relevant information and present it accordingly.

        HL7 Message:
        {hl7_message}

        Parsed Information:
    """

    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=550,
        n=1,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message['content'].strip()

def answer_question(parsed_hl7_message, user_question):
    prompt = f"The parsed HL7 message is:\n{parsed_hl7_message}\n\nThe user asked: {user_question}\n\nThe answer to the user's question is:"

    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=550,
        n=1,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message['content'].strip()

st.title("HL7 Parser")

hl7_input = st.text_area("Enter your HL7 message here:")

if st.button("Parse HL7"):
    if hl7_input:
        parsed_hl7 = parse_hl7_message(hl7_input)
        st.session_state.parsed_hl7_message = parsed_hl7
    else:
        st.write("Please enter an HL7 message.")

if 'parsed_hl7_message' in st.session_state:
    st.subheader("Parsed HL7 Message")
    st.write(st.session_state.parsed_hl7_message)
    user_question = st.text_input("Ask a question about the parsed HL7 message:")
    if st.button("Submit Question"):
        if user_question:
            answer = answer_question(st.session_state.parsed_hl7_message, user_question)
            st.write(answer)
        else:
            st.write("Please enter a question.")