from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

def create_vector_db(documents, persist_directory):
    """
    Create a Chroma vector database from document chunks
    
    Args:
        documents (list): List of document chunks to embed
        persist_directory (str): Directory to save the vector database
        
    Returns:
        Chroma: The created vector database
    """
    print("\nCreating vector database...")
    
    # Initialize HuggingFace embeddings model
    # We use all-MiniLM-L6-v2 which provides a good balance of quality and speed
    print("Initializing embedding model...")
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}  # Use CPU for compatibility
    )
    
    # Create directory if it doesn't exist
    os.makedirs(persist_directory, exist_ok=True)
    
    # Create and persist the vector database
    print(f"Embedding {len(documents)} document chunks...")
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    
    # Persist the database to disk
    vectordb.persist()
    print(f"Vector database created and saved to {persist_directory}")
    
    return vectordb

def load_vector_db(persist_directory):
    """
    Load a previously created Chroma vector database
    
    Args:
        persist_directory (str): Directory where the vector database is stored
        
    Returns:
        Chroma: The loaded vector database, or None if not found
    """
    # Initialize embedding model - must match the one used to create the database
    print("Initializing embedding model...")
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # Load the persisted vector database
    if os.path.exists(persist_directory):
        print(f"Loading vector database from {persist_directory}...")
        vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_model
        )
        print("Vector database loaded successfully")
        return vectordb
    else:
        print(f"No vector database found at {persist_directory}")
        return None