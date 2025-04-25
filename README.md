Inspired by https://archive.is/2025.04.13-061540/https://medium.com/data-science-collective/rag-in-action-build-your-own-local-pdf-chatbot-as-a-beginner-96c2833869ff

# Multimodal Document Chatbot

A powerful chatbot that can answer questions about your documents - including PDFs, Word documents, text files, and images with text.

## Features

- **Multiple Document Types**: Process PDFs, Word documents (.docx), text files, and images (.jpg, .png, etc.)
- **Built-in OCR**: Extract text from images and scanned documents using EasyOCR
- **Semantic Search**: Find relevant information across all your documents
- **Claude AI Integration**: Get intelligent, human-like responses to your questions
- **User-Friendly Interface**: Easy-to-use web interface built with Streamlit

## Requirements

- Python 3.8+
- Claude API key (from Anthropic)

## Installation

1. Clone this repository or download the files

2. Create a virtual environment and activate it:
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project directory with your Claude API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

### 1. Prepare your documents

Place your document files in a folder called `documents` in the project directory. The system supports:
- PDF files (.pdf)
- Word documents (.docx, .doc)
- Text files (.txt)
- Image files with text (.jpg, .jpeg, .png, .bmp, .tiff, .tif)

### 2. Process the documents

Run the following command to process your documents and create the vector database:

```bash
python process_documents.py
```

You can specify custom folders if needed:

```bash
python process_documents.py --docs_folder custom_docs --db_folder custom_db
```
### 3. Run Streamlit to access the user interface

Then start the app:

```bash
streamlit run app.py
```

#### 4. Open your browser

Go http://localhost:8501 if it doesn't open automatically.