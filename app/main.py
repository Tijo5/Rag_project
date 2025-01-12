import os
from preprocess import (
    extract_text_from_pdf,
    load_text_file,
    split_into_chunks,
    create_faiss_index
)

if __name__ == "__main__":
    # Define paths
    pdf_path = os.path.join("data", "communication.pdf")
    txt_path = os.path.join("data", "communication.txt")
    index_path = "DataIndex"

    # Step 1: Extract text from PDF
    print("Extracting text from PDF...")
    extract_text_from_pdf(pdf_path, txt_path)

    # Step 2: Load extracted text
    print("Loading extracted text...")
    content = load_text_file(txt_path)

    # Step 3: Split text into chunks
    print("Splitting text into chunks...")
    chunks = split_into_chunks(content)

    # Step 4: Create FAISS index
    print("Creating FAISS index...")
    create_faiss_index(chunks, index_path)

    print("Preprocessing completed successfully!")
