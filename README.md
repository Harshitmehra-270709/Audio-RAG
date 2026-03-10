# Audio-to-RAG (Retrieval-Augmented Generation) Pipeline

An end-to-end Python pipeline designed to transcribe audio files, intelligently chunk the resulting text, generate mathematical vector embeddings, and allow seamless semantic querying using a local vector database. 

##  Overview

This repository provides a complete toolset for processing spoken content and making it searchable and interactive. Instead of just reading a long transcript, you can "chat" with your audio files. 

### Core Workflow:
1. **Transcription**: Converts `.mp3` and `.wav` audio files into raw text transcripts.
2. **Chunking**: Breaks down large text passages into smaller, meaningful segments (with optional overlap) to retain contextual continuity.
3. **Embedding**: Transforms text chunks into vector representations using state-of-the-art embedding models.
4. **Vector Storage**: Persists embeddings locally in a SQLite-backed Vector Database (ChromaDB) for instant retrieval.
5. **RAG Search**: Leverages Retrieval-Augmented Generation to search the database for relevant context and answer user-defined queries accurately.

##  Repository Structure

- `Speech_to_text.py`: Handles audio transcription via speech recognition APIs.
- `chunk_transcripts.py` & `overlap_chunks.py`: Algorithms for breaking down transcripts into optimal context windows.
- `create_embeddings.py`: Generates the vector embeddings for the chunks.
- `rag_query.py`: The main query interface where the magic happens—combines retrieval with generation to answer your questions.

##  Getting Started

### Prerequisites

- Python 3.8+
- Required API Keys (e.g., for LLMs/Transcription services) placed into a `.env` file at the root.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Harshitmehra-270709/rag-model.git
   cd rag-model
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
   *Windows:* `.\venv\Scripts\Activate.ps1`
   *macOS/Linux:* `source venv/bin/activate`

3. **Install dependencies:**
   *(Ensure you have your specific requirements installed, often via `pip install -r requirements.txt`)*

### Setup

- Create a `.env` file in the root directory and add your API keys.
- **Note:** The `.env` file is explicitly ignored in the `.gitignore` to keep your credentials safe.

##  Important Note About Data

By design, this repository does **NOT** track large artifacts to keep the commit history clean:
-  Raw Audio files (`*.mp3`, `*.wav`, `*.m4a`) are ignored.
-  The generated local Vector Database (`vector_db/`) and intermediate `.json` chunks are ignored.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
