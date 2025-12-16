from langchain_community.utilities import SQLDatabase
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY, 
    model='gpt-4.1-mini', 
    temperature=0)

db = SQLDatabase.from_uri("sqlite:///sales.db")

embedding = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vectorstore = Chroma(
    persist_directory="./chroma_db", 
    embedding_function=embedding
)
retriever = vectorstore.as_retriever()