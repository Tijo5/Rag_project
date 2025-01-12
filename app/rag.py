import os
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA


# Load FAISS index
def load_faiss_index(index_path, embedding_model):
    """Load the FAISS index using the specified embedding model."""
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    return vector_store


# Create RAG system
def create_rag_system(index_path, embedding_model='sentence-transformers/all-MiniLM-L6-v2', model_name='gpt2'):
    """Create a Retrieval-Augmented Generation system."""
    # Load the FAISS index
    vector_store = load_faiss_index(index_path, embedding_model)

    # Initialize the HuggingFace model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    hf_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1,  # Use GPU if available
        max_new_tokens=100,  # Limit the number of tokens generated
        truncation=True,  # Explicitly enable truncation
        pad_token_id=tokenizer.eos_token_id  # Handle padding
    )

    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    # Define the prompt template
    prompt_template = """
You are an expert assistant. Use the following context to answer the user's question concisely and accurately.

Context:
{context}

Question: {question}

Provide a clear and structured answer:
"""
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template
    )

    # Create the RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain


# Limit context length
def limit_context(retrieved_docs, max_context_length=500):
    """Combine retrieved documents into a concise and meaningful context."""
    combined_context = "\n\n".join(doc.page_content.strip() for doc in retrieved_docs)
    return combined_context[:max_context_length] + "..." if len(combined_context) > max_context_length else combined_context


# Retrieve an answer
def get_answer(question, qa_chain, max_context_length=500):
    """Retrieve an answer to the user's question."""
    # Retrieve the most relevant documents
    retrieved_docs = qa_chain.retriever.get_relevant_documents(question)
    
    # Limit context length and join retrieved documents
    limited_context = limit_context(retrieved_docs, max_context_length)

    # Handle empty context
    if not retrieved_docs:
        return "I'm sorry, but I couldn't find any relevant information in the provided context."
    
    # Format inputs for the chain
    inputs = {"query": question, "context": limited_context}
    
    # Generate the answer
    answer = qa_chain.run(inputs)
    
    # Clean up and ensure meaningful output
    if not answer.strip():
        return "No relevant information found in the context provided."
    
    if answer.endswith((".", "!", "?")):
        return answer.strip()
    else:
        last_sentence_end = max(answer.rfind("."), answer.rfind("!"), answer.rfind("?"))
        if last_sentence_end != -1:
            return answer[:last_sentence_end + 1].strip()
        else:
            return answer.strip() + " (Response truncated for clarity)"




if __name__ == "__main__":
    # Path to the FAISS index directory
    index_path = "DataIndex"

    # Initialize the RAG system
    print("Initializing the RAG system...")
    rag_system = create_rag_system(index_path)
    print("RAG system ready! Ask your questions (type 'exit' to quit).")

    # User interaction loop
    while True:
        user_question = input("Your Question: ")
        if user_question.lower() == "exit":
            print("Exiting the RAG system. Goodbye!")
            break
        try:
            answer = get_answer(user_question, rag_system)
            print(f"Answer: {answer}")
        except Exception as e:
            print(f"An error occurred: {e}")
