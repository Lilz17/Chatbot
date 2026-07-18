from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

import os
import json

PDF_PATH = 'data/research/'
# run from within root

def sanitize_metadata(metadata):
    """Keep only known-safe primitive types."""
    safe_keys = ['source', 'file_path', 'page']
    new_meta = {}
    
    for k, v in metadata.items():
        # Only keep values that are simple primitives
        if isinstance(v, (str, int, float, bool)):
            new_meta[k] = v
        # If it's something else, ignore it or convert to string if critical
        elif v is None:
            new_meta[k] = None
        else:
            # Drop complex objects entirely to prevent Chroma from crashing
            continue
            
    return new_meta

def load_documents():

    documents = []

    if not os.path.exists(PDF_PATH):
        print(f"Directory {PDF_PATH} not found.")
        return []

    pdf_files = [
        os.path.join(PDF_PATH, file)
        for file in os.listdir(PDF_PATH)
        if file.endswith('.pdf')
    ]

    for pdf in pdf_files:
        #print(f"Loading {pdf}...")
        loader = DoclingLoader(file_path=pdf)
        docs = loader.load()
        documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)
    print(f"Loaded {len(chunks)} chunks from {len(pdf_files)} files.")
    return chunks

def create_vector_store():

    chunks = load_documents()

    for chunk in chunks:
        chunk.metadata = sanitize_metadata(chunk.metadata)

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="./vectorstore"
    )

    print("Vector store created and saved to ./vectorstore")
    return db

if __name__ == "__main__":
    create_vector_store()