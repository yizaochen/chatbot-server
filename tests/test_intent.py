from app.llm_engine.chains.intent import few_shot_structured_llm


def main():
    questions = [
        # "What is line edge roughness when doing EUV lithography?",
        # "Help me translate the word 'hello' to Spanish.",
        "Anyway, I want this do RAG.",
    ]
    for question in questions:
        print(f"Question: {question}")
        response = few_shot_structured_llm.invoke({"input": question})
        print(response.intent)
        print("\n\n")


main()
