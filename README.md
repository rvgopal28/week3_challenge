# README.md - Waffestry RAG Suite

## Project Name:

**Waffestry AI — Smart Café Assistant**

## Overview:

An AI-powered assistant for Waffestry café that answers customer/staff queries using advanced Retrieval-Augmented Generation (RAG) methods.

---

## Features:

* Self-RAG
* Corrective RAG
* Corrective RAG v2
* Fallback RAG
* Web Search RAG
* Adaptive RAG

---

## Prerequisites:

* Python 3.10+
* ChromaDB
* OpenAI API Key

## Installation:

```bash
pip install -r requirements.txt
```

## Environment Variables:

Create a `.env` file:

```
OPENAI_API_KEY=sk-xxxxx
```

## Preparing ChromaDB:

Ensure `chunks.json` is available in `data/`. Ingest data:

```bash
python ingest_data.py
```

## Running the App:

```bash
streamlit run main.py
```

## Usage:

1. Select a RAG Type.
2. Choose or type a query.
3. Submit and view responses.
4. Use Back button to change modes.

## Folder Structure:

```
waffestry_rag_suite/
├── main.py
├── self_rag_chain.py
├── corrective_rag_chain.py
├── corrective_rag_v2_chain.py
├── fallback_rag_chain.py
├── web_search_rag_chain.py
├── adaptive_rag_chain.py
├── response_formatter.py
├── utils.py
├── chroma_db.py
├── ingest_data.py
├── data/
│   ├── chunks.json
│   └── waffestry_logo.png
├── requirements.txt
└── README.md
```

## License:

MIT License.

## Contact:

[https://waffestry.com](https://waffestry.com) | @waffestry

---

End of README
