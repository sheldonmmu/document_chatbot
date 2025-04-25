import os
import argparse
from document_processor import load_and_split_documents
from vector_db import create_vector_db

def main():
    """
    Main function to process documents and create a vector database
    """
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Process documents and create a vector database")
    parser.add_argument("--docs_folder", type=str, default="documents", 
                       help="Folder containing document files (PDFs, Word docs, etc.)")
    parser.add_argument("--db_folder", type=str, default="db", 
                       help="Folder to save the vector database")
    args = parser.parse_args()
    
    print(f"=== Document Processing Tool ===")
    print(f"Documents folder: {args.docs_folder}")
    print(f"Database folder: {args.db_folder}")
    
    # Create docs_folder if it doesn't exist
    if not os.path.exists(args.docs_folder):
        os.makedirs(args.docs_folder)
        print(f"\nCreated folder {args.docs_folder}")
        print(f"Please place your document files in {args.docs_folder} and run this script again")
        return
    
    # Check if the folder is empty
    if not os.listdir(args.docs_folder):
        print(f"\nThe folder {args.docs_folder} is empty")
        print(f"Please add document files (PDFs, Word docs, text files, images) and run again")
        return
    
    # Load and split documents
    print(f"\nProcessing documents from {args.docs_folder}...")
    chunks = load_and_split_documents(args.docs_folder)
    
    if not chunks:
        print("\nNo document chunks were created. Please check your files and try again.")
        return
    
    # Create vector database
    vectordb = create_vector_db(chunks, args.db_folder)
    
    print("\n=== Processing Complete ===")
    print(f"Successfully processed documents and created vector database.")
    print(f"You can now run the chatbot app with: streamlit run app.py")

if __name__ == "__main__":
    main()