import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

embedding_function = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

def load_chroma_db(persist_directory="chroma_db"):
    db = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)
    return db
