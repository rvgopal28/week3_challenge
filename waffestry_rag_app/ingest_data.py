from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import json

from dotenv import load_dotenv
load_dotenv()  # This will load variables from .env


embedding_function = OpenAIEmbeddings()

# Load your data (menu items, SOPs, etc.)
with open('data/chunks.json', 'r') as f:
    documents = json.load(f)

texts = [doc['content'] for doc in documents]

# Split large texts into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_chunks = []
for text in texts:
    all_chunks.extend(text_splitter.split_text(text))

# Ingest into Chroma
vectorstore = Chroma.from_texts(all_chunks, embedding_function, persist_directory="chroma_db")
# vectorstore.persist()  # No longer needed in Chroma >= 0.4.x
print("Data Ingested into ChromaDB")