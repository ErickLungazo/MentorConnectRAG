import chromadb
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.readers.web import BeautifulSoupWebReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from utils.config import API_KEY
from llama_index.readers.youtube_transcript import YoutubeTranscriptReader
from llama_index.core import SimpleDirectoryReader
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

# Initialize LLM & Embedding Model
gemini_llm = GoogleGenAI(model="gemini-2.0-flash", api_key=API_KEY)
embed_model = GoogleGenAIEmbedding(model_name="text-embedding-004", api_key=API_KEY)

# Initialize ChromaDB Client & Collection
chroma_client = chromadb.PersistentClient(path="./chroma_db")  # Persistent storage
chroma_collection = chroma_client.get_or_create_collection("mentorconnect_rag")

def train_vectors(source_type, source_url, test_query):
    """
    Train the model by loading documents and creating the vector store index.

    Args:
        source_type (str): Type of source ("website", "file", "youtube").
        source_url (str): URL or file path of the source.
        test_query (str): Test query for validation.

    Returns:
        dict: A response containing the training status or error message.
    """
    try:
        # Load Documents Based on Source Type
        if source_type == "website":
            # Load data from website URLs using BeautifulSoupWebReader
            urls = [source_url]
            reader =BeautifulSoupWebReader()
            documents = reader.load_data(urls=urls)

        elif source_type == "file":
            # Load data from files in the "data" directory
            documents = SimpleDirectoryReader("data").load_data()

        elif source_type == "youtube":
            # Load transcripts from YouTube links
            youtube_links = [source_url]
            yt_reader = YoutubeTranscriptReader()
            documents = yt_reader.load_data(youtube_links)

        else:
            return {"error": "Invalid source type. Supported types are 'website', 'file', and 'youtube'."}

        # Setup Chroma Vector Store & Storage Context
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Create Vector Store Index
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            embed_model=embed_model
        )

        # Test Query
        query_engine = index.as_query_engine(llm=gemini_llm)
        test_response = query_engine.query(test_query)

        return {
            "message": "Training completed successfully!",
            "test_query": test_query,
            "test_response": str(test_response)
        }

    except Exception as e:
        return {"error": str(e)}