import chromadb
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from utils.config import API_KEY

# ✅ Initialize Google GenAI LLM & Embeddings
gemini_llm = GoogleGenAI(model="gemini-2.0-flash", api_key=API_KEY)
embed_model = GoogleGenAIEmbedding(model_name="text-embedding-004", api_key=API_KEY)

# ✅ Connect to Existing ChromaDB Collection
chroma_client = chromadb.PersistentClient(path="./chroma_db")  # Persistent storage
chroma_collection = chroma_client.get_or_create_collection("mentorconnect_rag")

def query_vectors(query_text: str):
    """
    Query the trained vector store for relevant information.

    Args:
        query_text (str): User query.

    Returns:
        dict: Response containing relevant information.
    """
    try:
        # ✅ Load Chroma Vector Store & Storage Context
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # ✅ Create Vector Store Index from Stored Embeddings
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store, storage_context=storage_context, embed_model=embed_model
        )

        # ✅ Create Query Engine
        query_engine = index.as_query_engine(llm=gemini_llm)

        # ✅ Process Query
        response = query_engine.query(query_text)

        return {"query": query_text, "response": str(response)}

    except Exception as e:
        return {"error": str(e)}
