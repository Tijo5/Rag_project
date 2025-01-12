#!/bin/bash

# First run main.py for preprocessing
echo "Running preprocessing with main.py..."
python app/main.py

# Then run rag.py for question-answering
echo "Starting the RAG system with rag.py..."
python app/rag.py
