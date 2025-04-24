# NeuroRAG: A Retrieval-Augmented Generation Chatbot for Private and API-Based Document Querying

## Project Overview
**NeuroRAG** is an end-to-end Retrieval-Augmented Generation (RAG) application that enables natural language interaction with documents such as `.pdf`, `.txt`, `.md`, `.csv`, and `.xlsx`. The project supports both **local inference using Ollama** (for privacy) and **cloud-based inference using Hugging Face and OpenAI APIs** (for deployability).

It is built using:
- **LangChain** for chaining logic
- **FAISS** for vector store search
- **HuggingFace Embeddings** for semantic chunking
- **Streamlit** for an interactive chatbot UI
- **Ollama** for lightweight local LLM inference

---

## Functionalities
- Multi-format document support: `.pdf`, `.txt`, `.md`, `.csv`, `.xlsx`
- Local LLM inference using Ollama models like `gemma:2b` or `mistral`
- API-based inference using Hugging Face and OpenAI models
- RAG workflow with semantic search and document chunking
- Per-user session-based chat logging (CSV export)
- Streamlit UI with memory-based chat experience

---

## Folder Structure
```
NeuroRAG/
├── data/                     # Document upload folder
├── logs/                     # Auto-generated user logs (CSV)
├── vectorstore/              # FAISS vector DB
├── chatbot_ollama.py         # Local Ollama LLM chatbot
├── chatbot_withAPI.py        # Hugging Face or OpenAI API-based chatbot
├── prepare_vectordb.py       # Script to chunk and embed docs
├── requirements.txt          # Python dependencies
├── .env                      # API keys and environment vars
└── README.md                 # Project README
```

---

## Steps to Run This Project

### ➤ 1. Clone the repository
```bash
git clone https://github.com/your-username/MY_RAG_GPT.git
cd MY_RAG_GPT
```

### ➤ 2. Create a virtual environment and install requirements
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### ➤ 3. Download Ollama and pull a model
```bash
ollama serve
ollama pull gemma:2b       # or mistral
```

### ➤ 4. Prepare the vectorstore
```bash
python prepare_vectordb.py
```

### ➤ 5. Run with Ollama (private mode)
```bash
streamlit run chatbot_ollama.py
```

### ➤ 6. OR run with Hugging Face or OpenAI API
- Add `HF_TOKEN` or `OPENAI_API_KEY` to your `.env`
```bash
streamlit run chatbot_withAPI.py
```

---

## Models Used
### Ollama (local)
- `gemma:2b` (faster, lightweight)
- `mistral`

### Hugging Face API
- `mistral`
- `google/flan-t5-base`
- `and others..`

### OpenAI API
- `gpt-3.5-turbo`
- `gpt-4` (optional, higher cost)

---

## Testing, Errors & Debugging
- Hugging Face model tasks often returned `task not supported` → switched models
- Hugging Face inference caused long delays and errors due to free tier limits
- OpenAI usage restricted by rate limits and billing constraints
- Resolved by integrating Ollama for **local inference**
- Unicode errors from `.txt` files fixed by specifying UTF-8 encoding
- Reduced `max_length` to speed up long outputs
- Tested different `k` values (number of documents retrieved)
- Refined chunk size in `RecursiveCharacterTextSplitter`

---

## What I Learned
- How to build a full-stack RAG pipeline using LangChain
- Vector storage using FAISS with real documents
- Chunking and semantic similarity search with embeddings
- Setting up Ollama for running LLMs locally
- Creating a clean, memory-retaining UI in Streamlit
- Logging user conversations for tracking

---

## Conclusion

NeuroRAG is a powerful RAG-based chatbot system built with flexibility, privacy, and real-world use in mind. It offers both local and cloud model inference, and is ideal for research, internal tools, and advanced AI demonstrations.

---

