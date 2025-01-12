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