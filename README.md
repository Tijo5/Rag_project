# Retrieval-Augmented Generation (RAG) System

This project implements a Retrieval-Augmented Generation (RAG) system that retrieves and generates answers based on information from a specific document. The system uses a free model for text generation, making it a powerful and cost-effective solution for answering questions based on document content.

---

## Document Overview

The document used for this project is titled **"Communication Skills among University Students"**, presented at the **UKM Teaching and Learning Congress 2011**. It was authored by:

- Zanaton Haji Iksan, Effendi Zakaria, Tamby Subahan Mohd Meera, Kamisah Osman, Denise Koh Choon Lian, Siti Nur Diyana Mahmud, and Pramela Krish.

The document investigates the level of communication skills among university students at Universiti Kebangsaan Malaysia (UKM). It highlights:

- The importance of communication skills as part of generic skills.
- Measurement of communication skills via a self-administered questionnaire covering oral, written, and social behavior.
- Findings that university students have achieved good communication skills.

This study is valuable for exploring how communication skills are developed and assessed among university students, providing context for the RAG system to retrieve answers.

---

## Features
- **Retrieve** specific information from the document.
- **Generate** contextually accurate answers using the free model (GPT2).
- Fully containerized for deployment using Docker.
- Easily customizable to work with any text-based document.

---

## Requirements
- **Docker** (tested with Docker version 27.4.0 or later).
- Optional: **Python 3.11 or later** (for running locally without Docker).

---

## Setup Instructions

### Clone the Repository
1. Open your terminal.
2. Clone the project from GitHub:
   ```bash
   git clone https://github.com/Tijo5/Rag_project.git
   cd Rag_project
3. Build the Docker image:
   ```bash
   docker build -t rag_project .
5. Verify the image is built
   ```bash
   docker images

---

### Run the Container
1. Start the container:
   ```bash
   docker run -it rag_project
3. The container initializes the RAG system and prompts you to ask a question.


## Execution

### Preprocessing the Document
- Before querying, preprocess the document to prepare it for retrieval:
  ```bash
  python app/main.py


### Query the System
- Ask questions and get answers from the document:
  ```bash
  python app/rag.py

## Exemple

- Document Context

  ```bash
  "The process of communication generally involves four elements: the speaker, the receiver, the communication channel, and feedback."

- Query

   ```bash
   What are the four elements of the communication process?

- Response
   ```bash
   The four elements of the communication process are the speaker, the receiver, the communication channel, and feedback.

