# Waffestry RAG Suite 🧇 — Self-RAG & Corrective-RAG

This project demonstrates how to build **Self-RAG** and **Corrective-RAG** pipelines using **LangChain + OpenAI + ChromaDB + Streamlit** for Waffestry's Cafe Automation.

---

## 🗂️ Project Structure

```
waffestry_rag_app/
├── main.py                    # Streamlit UI
├── self_rag_chain.py          # Self-RAG logic
├── corrective_rag_chain.py    # Corrective-RAG logic
├── verifier_prompt.py         # Verifier prompt template
├── utils.py                   # Helper utilities (uncertainty checks)
├── chroma_db.py               # ChromaDB Loader
├── ingest_data.py             # Data ingestion script
├── data/
│   └── chunks.json            # Your SOP/Menu data in chunks
├── requirements.txt
└── .env                       # OpenAI API Key
```

---

## 🛠️ Setup Instructions

### 1. Clone Repo & Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add OpenAI API Key
Create a `.env` file and paste:
```
OPENAI_API_KEY=your-openai-key-here
```

### 3. Prepare Data
- Place your Waffestry SOP/Menu chunks in `data/chunks.json`
  ```json
  [
    {"content": "Mango Waffle is made using fresh mango pulp..."},
    {"content": "Inventory SOP: Always order butter from Vendor A..."}
  ]
  ```

### 4. Ingest Data into Chroma VectorDB
```bash
python ingest_data.py
```
This will create a local `chroma_db/` directory with your vector store.

### 5. Run the Streamlit App
```bash
streamlit run main.py
```

---

## 🎮 How to Use
1. Select RAG Type: **Self-RAG** or **Corrective-RAG**
2. Ask a question (e.g., "Do you have gluten-free waffles?")
3. The system will display:
   - Initial LLM Answer
   - Whether RAG was triggered
   - Corrected answer (if hallucination detected)

---

## 🧠 RAG Types Explained
| Type            | Behavior | Use Case |
|-----------------|----------|----------|
| **Self-RAG**    | LLM tries from memory, triggers retrieval if unsure | Customer FAQ Bot |
| **Corrective-RAG** | LLM generates, Verifier fact-checks, RAG corrects if needed | Allergy & Ingredient Info Bot |

---

## 📦 Dependencies
```
openai
langchain
chromadb
streamlit
python-dotenv
```

---

## 🚀 Next Steps
- Add Fusion-RAG for SOP multi-doc synthesis
- Integrate WhatsApp API for order workflows
- Analytics dashboard using Adaptive RAG

---

## 📬 Contact
For queries or collaborations, reach out to **Waffestry AI Team**