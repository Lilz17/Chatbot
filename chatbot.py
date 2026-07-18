import os
import json

import requests

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ----------------------------
# Load Embedding Model
# ----------------------------

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ----------------------------
# Load Chroma Database
# ----------------------------

db = Chroma(
    persist_directory="./vectorstore",
    embedding_function=embedding_model
)

# ----------------------------
# Ollama Model
# ----------------------------

#MODEL_NAME = "gemma2:2b"
MODEL_NAME = "llama3.1"

# ----------------------------
# Question Answer Function
# ----------------------------

def answer_question(question):
    # docs = db.similarity_search(question, k=3)

    # replacing semantic match with maximal marginal relevance for information retrieval
    docs = db.max_marginal_relevance_search(question, k=3, fetch_k=10)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an academic research assistant. Use a concise, professional tone. Avoid robotic phrasing.
Answer accurately based on the context. 
If you don't know the answer, respond with "Sorry, I could not find that information in my knowledge bank".

Context: {context}
Question: {question}
Answer:
"""
    
    # Post the request
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": True # changed to True for real-time responses
            },
            timeout=120,
            stream=True
        )
        if response.status_code != 200:
            return "Error: Unable to connect to the model."
    except requests.exceptions.RequestException as e:
        return f"Error: Could not reach the Ollama server. ({e})"

    # process stream line-by-line
    print("Bot: ", end="", flush=True)
    full_response = ""

    try:
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if "response" in chunk:
                    piece = chunk["response"]
                    print(piece, end="", flush=True)
                    full_response += piece
        print()

        # empty message
        if not full_response:
            return "Sorry, the model failed to generate a response."
            
        return full_response
    
    except Exception as e:
        return f"Error while processing stream: {e}"

    # result = response.json()

    # if "response" in result:
    #     return result["response"]

    # return "Unable to generate response."

# ----------------------------
# Testing
# ----------------------------

if __name__ == "__main__":
    print("\nThe chatbot is now active. Type 'exit' to quit.")
    #print()

    while True:
        query = input("\nYou: ")
        if query.lower() == "exit":
            print("Goodbye!")
            break

        answer = answer_question(query)
        print("Bot:", answer)
