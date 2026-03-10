import os
import json
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from google import genai

# load_dotenv()

# api_key = os.getenv("GEMINI_API_KEY")
# genai.configure(api_key=api_key)
# client = chromadb.Client(
#     settings=chromadb.Settings(
#         persist_directory="vector_db"
#     )
# )
# collection = client.get_or_create_collection(name="video_rag")
# INPUT_FOLDER = "overlap_chunks"

# for file_name in os.listdir(INPUT_FOLDER):
#     if file_name.endswith(".json"):
#         file_path = os.path.join(INPUT_FOLDER,file_name)

#         with open(file_path ,"r" ,encoding="utf-8") as f:
#             data= json.load(f)
#         for chunk in data:
#             response = genai.embed_content(
#                 model="models/text-embedding-004",
#                 content=chunk["text"]

#             )
#             embedding = response["embedding"]
#             collection.add(
#                 documents=[chunk["text"]],
#                 embeddings=[embedding],
#                 metadatas=[{
#                     "source":chunk["source"],
#                     "start":chunk["start"],
#                     "end":chunk["end"]
#                 }],
#                 ids =[f"{chunk['source']}_{ chunk['chunk_id'] }"]
#             )
# client.persist()
import os
import json
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from google import genai

# -------------------------
# Load API key
# -------------------------

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

# -------------------------
# Initialize Gemini client
# -------------------------

client_gemini = genai.Client(api_key=API_KEY)

# -------------------------
# Initialize ChromaDB
# -------------------------

import chromadb

# Initialize persistent Chroma database
chroma_client = chromadb.PersistentClient(
    path="vector_db"
)

collection = chroma_client.get_or_create_collection(
    name="video_rag"
)

# -------------------------
# Input folder
# -------------------------

INPUT_FOLDER = "overlap_chunks"

# -------------------------
# Process each chunk file
# -------------------------

for file_name in os.listdir(INPUT_FOLDER):

    if not file_name.endswith(".json"):
        continue

    print(f"Processing {file_name}")

    file_path = os.path.join(INPUT_FOLDER, file_name)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = []
    metadatas = []
    ids = []

    for chunk in data:

        texts.append(chunk["text"])

        metadatas.append({
            "source": chunk["source"],
            "start": chunk["start"],
            "end": chunk["end"]
        })

        ids.append(f"{chunk['source']}_{chunk['chunk_id']}")

    # -------------------------
    # Generate embeddings
    # -------------------------

    response = client_gemini.models.embed_content(
        model="models/gemini-embedding-001",
        contents=texts
    )

    embeddings = [e.values for e in response.embeddings]

    # -------------------------
    # Store in ChromaDB
    # -------------------------

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Stored {len(texts)} chunks")




print("we are done saving the embedding in the chromadb")
