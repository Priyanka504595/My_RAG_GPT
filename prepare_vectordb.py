import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv(find_dotenv())

DATA_FOLDER = "data"
FAISS_DB_PATH = "vectorstore/db_faiss"

def load_documents(folder_path):
    docs = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        if filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            docs.extend(loader.load())

        elif filename.endswith(".md"):
            loader = UnstructuredMarkdownLoader(filepath)
            docs.extend(loader.load())

        elif filename.endswith(".txt"):
            loader = TextLoader(filepath, encoding="utf-8", autodetect_encoding=True)
            docs.extend(loader.load())

        elif filename.endswith(".csv"):
            df = pd.read_csv(filepath)
            text = df.to_markdown(index=False)
            docs.append(Document(page_content=text, metadata={"source": filepath}))

        elif filename.endswith(".xlsx"):
            df = pd.read_excel(filepath)
            text = df.to_markdown(index=False)
            docs.append(Document(page_content=text, metadata={"source": filepath}))

        else:
            print(f"Skipping unsupported file: {filename}")

    return docs

def create_vectorstore(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    split_docs = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    vectorstore.save_local(FAISS_DB_PATH)
    print("Vectorstore created and saved.")

if __name__ == "__main__":
    all_docs = load_documents(DATA_FOLDER)
    create_vectorstore(all_docs)
