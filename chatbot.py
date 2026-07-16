import os
#print(os.getenv("GOOGLE_API_KEY"))

import requests

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# ----------------------------
# Load Embedding Model
# ----------------------------

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ----------------------------
# Load FAISS Database
# ----------------------------

db = FAISS.load_local(
    "vectorstore",
    embedding_model,
    allow_dangerous_deserialization=True
)

# ----------------------------
# Ollama Model
# ----------------------------

MODEL_NAME = "gemma2:2b"

# ----------------------------
# Question Answer Function
# ----------------------------

def answer_question(question):

    docs = db.similarity_search(
        question,
        k=3
    )

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are QnA bot.

Answer ONLY from the provided context.

If the answer is not present in the context, reply:

I could not find that information in the knowledge base.

Context:
{context}

Question:
{question}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    result = response.json()

    if "response" in result:
        return result["response"]

    return "Unable to generate response."

# ----------------------------
# Testing
# ----------------------------

if __name__ == "__main__":

    while True:

        query = input("You: ")

        if query.lower() == "exit":
            break

        answer = answer_question(query)

        print("\nBot:", answer)
