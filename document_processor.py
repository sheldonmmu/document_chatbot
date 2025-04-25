from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import tempfile
from PIL import Image
import easyocr
import time

# Initialize EasyOCR reader (only do this once)
# We use lazy loading to only initialize when needed
reader = None

def get_ocr_reader():
    """
    Get or initialize the EasyOCR reader
    
    Returns:
        easyocr.Reader: Initialized OCR reader
    """
    global reader
    if reader is None:
        print("Initializing EasyOCR reader (this may take a moment the first time)...")
        reader = easyocr.Reader(['en'])  # Initialize for English
    return reader

def extract_text_from_image(image_path):
    """
    Extract text from an image using EasyOCR
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Extracted text from the image
    """
    try:
        # Get the OCR reader
        ocr_reader = get_ocr_reader()
        
        # Use EasyOCR to extract text
        print(f"Extracting text from image: {image_path}")
        start_time = time.time()
        results = ocr_reader.readtext(image_path)
        end_time = time.time()
        print(f"OCR completed in {end_time - start_time:.2f} seconds")
        
        # Concatenate the detected text
        text = ""
        for (_, text_result, _) in results:
            text += text_result + " "
        
        return text
    except Exception as e:
        print(f"Error extracting text from {image_path}: {e}")
        return ""

def load_and_split_documents(docs_folder):
    """
    Load documents from a folder and split them into chunks
    Supports: PDF, DOCX, TXT, and image files (JPG, PNG)
    
    Args:
        docs_folder (str): Path to the folder containing documents
        
    Returns:
        list: List of document chunks ready for embedding
    """
    documents = []
    
    # Check if the folder exists
    if not os.path.exists(docs_folder):
        print(f"Folder {docs_folder} does not exist")
        return documents
    
    # Get all files in the folder
    all_files = os.listdir(docs_folder)
    
    if not all_files:
        print(f"No files found in {docs_folder}")
        return documents
    
    # Track document counts by type for reporting
    doc_counts = {
        "pdf": 0,
        "word": 0,
        "text": 0,
        "image": 0,
        "unsupported": 0
    }
    
    # Process each file based on its extension
    for file in all_files:
        file_path = os.path.join(docs_folder, file)
        file_ext = os.path.splitext(file)[1].lower()
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
            
        try:
            print(f"Loading {file_path}")
            
            # PDF files
            if file_ext == '.pdf':
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
                doc_counts["pdf"] += 1
            
            # Word documents
            elif file_ext in ['.docx', '.doc']:
                loader = Docx2txtLoader(file_path)
                documents.extend(loader.load())
                doc_counts["word"] += 1
            
            # Text files
            elif file_ext == '.txt':
                loader = TextLoader(file_path)
                documents.extend(loader.load())
                doc_counts["text"] += 1
            
            # Image files (using EasyOCR)
            elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']:
                text = extract_text_from_image(file_path)
                if text:
                    # Create a temporary text file with the extracted text
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp:
                        temp.write(text.encode('utf-8'))
                        temp_path = temp.name
                    
                    # Load the temporary text file
                    loader = TextLoader(temp_path)
                    documents.extend(loader.load())
                    
                    # Remove the temporary file
                    os.unlink(temp_path)
                doc_counts["image"] += 1
            else:
                print(f"Unsupported file type: {file_ext}")
                doc_counts["unsupported"] += 1
                
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    # Print summary of processed documents
    print("\nDocument processing summary:")
    print(f"PDF files: {doc_counts['pdf']}")
    print(f"Word documents: {doc_counts['word']}")
    print(f"Text files: {doc_counts['text']}")
    print(f"Image files: {doc_counts['image']}")
    print(f"Unsupported files: {doc_counts['unsupported']}")
    
    # If no documents were loaded, return empty list
    if not documents:
        print("No documents were successfully loaded.")
        return documents
    
    # Split documents into chunks for better processing
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Characters per chunk
        chunk_overlap=200,  # Overlap between chunks to maintain context
        length_function=len
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"\nSplit {len(documents)} documents into {len(chunks)} chunks")
    
    return chunks