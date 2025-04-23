# llm details https://docs.anthropic.com/en/docs/about-claude/models/all-models

from langchain_anthropic import ChatAnthropic
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_chatbot(vectordb):
    """
    Create a chatbot using Claude API and the vector database
    
    Args:
        vectordb: Vector database for retrieving relevant document chunks
        
    Returns:
        ConversationalRetrievalChain: The chatbot chain
    """
    # Ensure API key is available
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    # Initialize the Claude model
    # We use claude-3-haiku for speed, but you can use other models like claude-3-sonnet for better quality
    print("Initializing Claude model...")
    llm = ChatAnthropic(
        model="claude-3-7-sonnet-20250219",
        #model="claude-3-haiku-20240307",
        temperature=0.7,  # Controls randomness: higher = more creative, lower = more deterministic
        anthropic_api_key=api_key
    )
    
    # Create conversation memory to maintain context across interactions
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # Create a system prompt that tells Claude how to respond
    system_prompt = """You are a helpful AI assistant that answers questions based on the provided documents.
    
    For each question:
    1. Focus on information from the provided document excerpts
    2. If the documents contain the answer, provide it clearly and concisely
    3. If the documents don't contain the answer, say "I don't find information about that in the documents"
    4. Use bullet points for multi-part answers
    5. Include relevant quotes when helpful
    
    Keep your responses friendly and helpful."""
    
    # Create the retrieval chain
    print("Creating conversational retrieval chain...")
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectordb.as_retriever(search_kwargs={"k": 4}),  # Retrieve top 4 most relevant chunks
        memory=memory,
        verbose=True
    )
    
    return qa_chain