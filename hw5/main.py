from query_system_multiagent import answer_question


def main():
    print("HW5 Multi-Agent QA System")
    print("Type 'exit' to quit.\n")
    while True:
        try:
            q = input("Question: ").strip()
        except EOFError:
            break
        if not q or q.lower() in {"exit", "quit"}:
            break
        result = answer_question(q)
        print(f"Answer: {result['answer']}\n")


if __name__ == "__main__":
    main()
