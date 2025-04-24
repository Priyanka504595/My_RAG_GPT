import os
import re
import streamlit as st
import datetime
import csv
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv(find_dotenv())

DB_FAISS_PATH = "vectorstore/db_faiss"

@st.cache_resource
def get_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db

def set_custom_prompt():
    custom_template = """
    Use the pieces of information provided in the context to answer user's question.
    If you don't know the answer, say that you don't know. Do not hallucinate.

    Context: {context}
    Question: {question}

    Answer:
    """
    return PromptTemplate(template=custom_template, input_variables=["context", "question"])

def load_llm():
    return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

def log_chat(name, question, answer, sources):
    os.makedirs("logs", exist_ok=True)
    filename = f"logs/chat_{name}_{datetime.date.today()}.csv"
    source_files = "; ".join([
        f"{os.path.basename(doc.metadata.get('source', ''))} (Page {doc.metadata.get('page', 'N/A')})"
        for doc in sources
    ])
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        timestamp = datetime.datetime.now().isoformat()
        combined_text = f"Q: {question}\nA: {answer}"
        writer.writerow([name, timestamp, combined_text, source_files])

def main():
    st.set_page_config(page_title="NeuroRAG (OpenAI Version)", page_icon="🧠")
    st.title("Welcome to NeuroRAG - your intelligent AI assistant.")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'username' not in st.session_state:
        st.session_state.username = ""
    st.session_state.username = st.text_input("Enter your name to begin:")
    if not st.session_state.username.strip():
        st.warning("Please enter your name above to begin chatting.")
        st.stop()

    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    prompt = st.chat_input("Ask me something based on your uploaded files")

    if prompt:
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        try:
            vectorstore = get_vectorstore()
            qa_chain = RetrievalQA.from_chain_type(
                llm=load_llm(),
                chain_type="stuff",
                retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
                return_source_documents=True,
                chain_type_kwargs={"prompt": set_custom_prompt()}
            )

            response = qa_chain.invoke({"query": prompt})
            result = response["result"]
            source_documents = response["source_documents"]

            if any(x in result.lower() for x in ["context does not provide any information", "I cannot answer", "no information", "I don't have that information","I don't know"]):
                result_to_show = result
            else:
                sources = "\n".join([
                    f"- Page {doc.metadata.get('page', 'N/A')} from {os.path.basename(doc.metadata.get('source', ''))}"
                    for doc in source_documents
                ])
                result_to_show = result + "\n\n**Source Documents:**\n" + sources

            st.chat_message('assistant').markdown(result_to_show)
            st.session_state.messages.append({'role': 'assistant', 'content': result_to_show})

            # Log chat
            log_chat(st.session_state.username, prompt, result, source_documents)

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()