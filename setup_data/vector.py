import pandas as pd
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()

df = pd.read_csv("./data/customer_reviews.csv")

documents = []
for _, row in df.iterrows():
    text = (
        f"Product: {row['product_name']} | "
        f"Sentiment: {row['sentiment']} | "
        f"Comment: {row['comment']}"
    )

    documents.append(
        Document(
            page_content=text,
            metadata={
                "product": row["product_name"],
                "sentiment": row["sentiment"]
            }
        )
    )

embedding = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

Chroma.from_documents(
    documents=documents,
    embedding=embedding,
    persist_directory="./chroma_db"
)

