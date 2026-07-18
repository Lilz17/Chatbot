
# Personal Revision Helper

An AI-powered Study Assistant designed to transform your raw lecture notes and research PDFs into an interactive knowledge base. Unlike basic chatbots, this project uses **RAG (Retrieval-Augmented Generation)** to provide accurate, context-aware answers, create quizzes, and generate study aids.

## Key Features

* **Persistent Knowledge Base:** Uses `ChromaDB` to store and manage your study materials efficiently.
* **Professional Reasoning:** Powered by `Llama 3.1` (via Ollama) for high-quality, academic-grade responses.
* **Intelligent Retrieval:** Employs **Maximal Marginal Relevance (MMR)** to ensure retrieved context is both relevant and diverse.
* **Modern Stack:** Built using `uv` for lightning-fast dependency management and `Docling` for high-fidelity PDF parsing.



## Tech Stack

* **Language:** Python 3.12+
* **Frameworks:** LangChain, ChromaDB
* **Inference:** Ollama (Llama 3.1)
* **PDF Extraction:** Docling
* **Dependency Manager:** `uv`



## Quick Start

### 1. Setup Environment

```bash
# Create and activate environment
uv venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows

# Install dependencies
uv sync
```

### 2. Prepare the Knowledge Base

Place your PDFs into `data/research/` and run the ingestion pipeline:

```bash
python ingest.py
```

### 3. Launch the Assistant

```bash
# Text Interface
python chatbot.py
```

## Project Log & Roadmap

### Recent Improvements


* **Migration:** Transitioned to `uv` for industrial-grade dependency management.
* **Extraction:** Upgraded to `DoclingLoader` for better accuracy with complex PDF layouts.
* **Search Optimization:** Switched to MMR for superior retrieval results compared to basic semantic search.


### Development Roadmap


* [ ] **Citation Engine:** Implement source tracking (filename & page) for model responses.
* [ ] **Quiz Module:** Automatically generate practice questions from notes.
* [ ] **Flashcard Export:** Export key terms to CSV/Anki format.
* [ ] **Parallel Ingestion:** Speed up processing for large document libraries.
* [ ] **UI/Voice:** Refactor `voice_assistant.py` and `app.py`.



## Notes for Contributors

* Ensure `Ollama` is running locally before executing `chatbot.py`.
* If modifying the ingestion pipeline, ensure `sanitize_metadata()` is utilized to maintain `ChromaDB` compatibility.


