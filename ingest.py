from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import os

PDF_PATH = 'data/research/'
# run from within root

def load_documents():

    documents = []

    # pdf_files = [
    #     "data/faq.pdf",
    #     "data/courses.pdf",
    #     "data/notices.pdf",
    #     "data/placements.pdf",
    #     "data/pgcp_ai_course.pdf"
    # ]

    pdf_files = [
        os.path.join(PDF_PATH, file)
        for file in os.listdir(PDF_PATH)
        if file.endswith('.pdf')
    ]

    for pdf in pdf_files:

        loader = PyPDFLoader(pdf)

        docs = loader.load()

        documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    return chunks

def create_vector_store():

    chunks = load_documents()

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(
        chunks,
        embedding_model
    )

    db.save_local("vectorstore")

if __name__ == "__main__":
    create_vector_store()