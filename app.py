import streamlit as st
import os
from vector_db import load_vector_db
from chatbot import create_chatbot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Document Chatbot",
    page_icon="📚",
    layout="centered"
)

# Add custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTextInput, .stTextArea {
        padding: 0.5rem;
    }
    .user-message {
        background-color: #00000;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .bot-message {
        background-color: #000000;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .document-info {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 3px solid #4CAF50;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Check if Claude API key is available
if not os.getenv("ANTHROPIC_API_KEY"):
    st.error("ANTHROPIC_API_KEY not found in environment variables.")
    st.info("Please add your Claude API key to the .env file.")
    st.stop()

# Title and description
st.title("📚 Document Chatbot")
st.markdown("Ask questions about your documents using Claude AI")

# Sidebar for information and document stats
with st.sidebar:
    st.header("About")
    st.info(
        "This app uses Claude AI to answer questions about your documents. "
        "It supports PDFs, Word documents, text files, and images with text."
    )

    st.header("Instructions")
    st.markdown(
        "1. Place document files in the 'documents' folder\n"
        "2. Run 'python process_documents.py' to process the documents\n"
        "3. Start this app with 'streamlit run app.py'\n"
        "4. Ask questions about your documents"
    )

    # Document stats
    st.header("Document Information")
    db_folder = "db"

    # Show document stats if available
    if os.path.exists(db_folder):
        try:
            # Count documents in the database
            collection_size = sum(len(files)
                                  for _, _, files in os.walk(db_folder))
            st.markdown(
                f"<div class='document-info'>Vector database is ready with document information.</div>", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not read database stats: {e}")
    else:
        st.warning(
            "No vector database found. Please process your documents first.")

# Load the vector database
db_folder = "db"
vectordb = load_vector_db(db_folder)

if vectordb is None:
    st.error("No vector database found. Please process your documents first.")
    st.info("Run 'python process_documents.py' to process your documents.")
    st.stop()

# Create the chatbot
qa_chain = create_chatbot(vectordb)

# Display chat history
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(
                f"<div class='user-message'>🧑‍💻 You: {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                f"<div class='bot-message'>🤖 Bot: {message['content']}</div>", unsafe_allow_html=True)

# Chat input
prompt = st.text_area("Ask a question about your documents:", height=100)

if st.button("Send"):
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.container():
            st.markdown(
                f"<div class='user-message'>🧑‍💻 You: {prompt}</div>", unsafe_allow_html=True)

        # Get response from chatbot
        with st.spinner("Thinking..."):
            response = qa_chain.invoke({"question": prompt})
            answer = response["answer"]

        # Add bot message to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": answer})

        # Display bot message
        with st.container():
            st.markdown(
                f"<div class='bot-message'>🤖 Bot: {answer}</div>", unsafe_allow_html=True)

        # Clear input
        prompt = ""
        st.experimental_rerun()
