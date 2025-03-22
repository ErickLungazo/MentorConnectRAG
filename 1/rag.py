import os
import chromadb
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.vector_stores.chroma import ChromaVectorStore
from utils import API_KEY  # Assuming API_KEY is stored in utils.py

# ✅ Initialize Google GenAI LLM & Embeddings
# gemini_llm = GoogleGenAI(api_key=API_KEY)
gemini_llm = GoogleGenAI(
    model="gemini-2.0-flash",
    api_key=API_KEY)
embed_model = GoogleGenAIEmbedding(model_name="text-embedding-004", api_key=API_KEY)

# ✅ Create ChromaDB Client & Collection (Ephemeral - In-Memory)
chroma_client = chromadb.EphemeralClient()  # Use `PersistentClient(path="./chroma_db")` for persistence
chroma_collection = chroma_client.create_collection("mentorconnect_rag")

# ✅ Load Documents
documents = SimpleDirectoryReader("data").load_data()

# ✅ Setup Chroma Vector Store & Storage Context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# ✅ Create Vector Store Index
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=embed_model)

# ✅ Create Query Engine
query_engine = index.as_query_engine(llm=gemini_llm)

# ✅ Query the System
query = "What is mentor connect?"
response = query_engine.query(query)

# ✅ Print the Response
print(response)
