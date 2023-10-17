import os
from dotenv import load_dotenv

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.callbacks import get_openai_callback

import streamlit as st

load_dotenv('key.env')

llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

model = ChatOpenAI()

st.title("Start the Code Here")

input_list = st.sidebar.text_input("Input list", "aeroplane")
output_list = st.sidebar.text_input("Output list", "'a','e','r','o','p','l','a','n','e'")

lang = st.sidebar.selectbox("Programming Language", ["c", "c++", "java", "python", "html", "sql"])
operation = st.sidebar.selectbox("Choose Operation", ["Convert word to letters", "Convert letters to word"])

if operation == "Convert word to letters":
    text = st.text_input("give the text", "convert word to letters")
elif operation == "Convert letters to word":
    text = st.text_input("give the text", "convert letters to word")


prompt_text = "use {lang} to {text} with input: {inp} and output: {outp}. Please give me only code"

if st.button("Run"):
    template = ChatPromptTemplate.from_messages([("system", prompt_text)])
    template = template.format_messages(text=text, lang=lang, inp=input_list, outp=output_list)
    code = model(template)  # Assign the result to the 'code' variable

    st.subheader("Output:")
    st.code(code.content)

    with get_openai_callback() as callback:
        tokens=model(template)
        st.write(callback)

    with open("logs.txt", "a") as logfile:
        logfile.write(f"Language: {lang}\n")
        logfile.write(f"Input: {input_list}\n")
        logfile.write(f"Output: {output_list}\n")
        logfile.write(f"Text: {text}\n")
        logfile.write(f"output code: {code.content}\n")
