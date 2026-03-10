# import os
# from dotenv import load_dotenv
# from google import genai
# import chromadb

# # -----------------------------
# # Load API Key
# # -----------------------------

# load_dotenv()

# API_KEY = os.getenv("GEMINI_API_KEY")

# client_gemini = genai.Client(api_key=API_KEY)

# # -----------------------------
# # Connect to Chroma Vector DB
# # -----------------------------

# chroma_client = chromadb.PersistentClient(
#     path="vector_db"
# )

# collection = chroma_client.get_collection(
#     name="video_rag"
# )

# # -----------------------------
# # Ask user question
# # -----------------------------

# question = input("\nAsk your question: ")

# # -----------------------------
# # Embed the question
# # -----------------------------

# response = client_gemini.models.embed_content(
#     model="models/gemini-embedding-001",
#     contents=[question]
# )

# query_embedding = response.embeddings[0].values

# # -----------------------------
# # Search Vector Database
# # -----------------------------

# results = collection.query(
#     query_embeddings=[query_embedding],
#     n_results=5
# )

# documents = results["documents"][0]
# metadatas = results["metadatas"][0]

# # -----------------------------
# # Build Context
# # -----------------------------

# context = ""

# for doc, meta in zip(documents, metadatas):

#     context += f"""
# Source Video: {meta['source']}
# Timestamp: {meta['start']}s - {meta['end']}s

# {doc}

# ---
# """

# # -----------------------------
# # Send context to Gemini
# # -----------------------------

# prompt = f"""
# Answer the user's question using ONLY the provided context.

# Context:
# {context}

# Question:
# {question}

# If the answer exists in the context, provide the timestamp and source video.
# If not found, say the information is not available.
# """

# answer = client_gemini.models.generate_content(
#     model="models/gemini-2.5-flash",
#     contents=prompt
# )

# print("\n-----------------------------")
# print("ANSWER")
# print("-----------------------------\n")

# print(answer.text)







import os
import chromadb
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load API key
# -----------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY is None:
    raise ValueError("GEMINI_API_KEY not found in .env")

# -----------------------------
# Initialize Gemini Client
# -----------------------------

client_gemini = genai.Client(api_key=API_KEY)

# -----------------------------
# Connect to Chroma Vector DB
# -----------------------------

chroma_client = chromadb.PersistentClient(
    path="vector_db"
)

collection = chroma_client.get_collection(
    name="video_rag"
)

# -----------------------------
# Reranking Function
# -----------------------------

def rerank_chunks(question, documents):

    joined_chunks = ""

    for i, doc in enumerate(documents):
        joined_chunks += f"\nChunk {i}:\n{doc}\n"

    prompt = f"""
You are a retrieval assistant.

From the chunks below, select the 3 most relevant chunks
for answering the question.

Return ONLY the chunk numbers separated by commas.

Question:
{question}

Chunks:
{joined_chunks}
"""

    response = client_gemini.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    numbers = response.text.strip()

    indices = [int(x) for x in numbers.split(",")]

    return indices


# -----------------------------
# Ask user question
# -----------------------------

question = input("\nAsk your question: ")

# -----------------------------
# Embed the question
# -----------------------------

embed_response = client_gemini.models.embed_content(
    model="models/gemini-embedding-001",
    contents=[question]
)

query_embedding = embed_response.embeddings[0].values

# -----------------------------
# Vector search
# -----------------------------

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10
)

documents = results["documents"][0]
metadatas = results["metadatas"][0]

# -----------------------------
# Rerank results
# -----------------------------

indices = rerank_chunks(question, documents)

documents = [documents[i] for i in indices]
metadatas = [metadatas[i] for i in indices]

# -----------------------------
# Build context
# -----------------------------

context = ""

for doc, meta in zip(documents, metadatas):

    def format_time(seconds):
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"

start = format_time(meta["start"])
end = format_time(meta["end"])

context += f"""
Source Video: {meta['source'].replace('_chunks.json','')}
Timestamp: {start} - {end}

Content:
{doc}
"""


# -----------------------------
# Final Answer Generation
# -----------------------------

prompt = f"""
Answer the question using ONLY the provided context.

Context:
{context}

Question:
{question}

If the answer exists in the context:
- provide the explanation
- include the source video and timestamp

If not found, say the information is not available.
"""

answer = client_gemini.models.generate_content(
    model="models/gemini-2.5-flash",
    contents=prompt
)

# -----------------------------
# Display Answer
# -----------------------------

print("\n-----------------------------------")
print("ANSWER")
print("-----------------------------------\n")

print(answer.text)