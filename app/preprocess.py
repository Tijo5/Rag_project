import os
import fitz  # PyMuPDF for reading PDFs
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Step 1: Extract Text from PDF
def extract_text_from_pdf(pdf_path, output_txt_path):
    """Extract text from a PDF file and save it to a text file."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()

    with open(output_txt_path, "w", encoding="utf-8") as text_file:
        text_file.write(text)
    print(f"Extracted text saved to {output_txt_path}")

# Step 2: Load Text File
def load_text_file(txt_path):
    """Load the content of a text file."""
    with open(txt_path, "r", encoding="utf-8") as file:
        return file.read()

# Step 3: Split Text into Chunks
def split_into_chunks(content, chunk_size=1000, chunk_overlap=200):
    """Split text into manageable chunks using RecursiveCharacterTextSplitter."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.create_documents([content])
    return chunks

# Step 4: Create FAISS Index
def create_faiss_index(chunks, index_path, embedding_model='sentence-transformers/all-MiniLM-L6-v2'):
    """Embed the text chunks and create a FAISS index."""
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    vector_store = FAISS.from_documents(documents=chunks, embedding=embeddings)
    
    if not os.path.exists(index_path):
        os.makedirs(index_path)
    vector_store.save_local(index_path)
    print(f"FAISS index saved to {index_path}")
