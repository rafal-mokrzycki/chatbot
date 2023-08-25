from interface import UserInterface

if __name__ == "__main__":
    queries = [
        "Jakie powinny być marginesy w pracy?",
        "Jak zmienić promotora?",
        "Czy mogę zmienić formę studiów?",
        "Kim był Kopernik?",
        "Kiedy wybuchła I wojna światowa?",
        "Ile mieszkańców ma Warszawa?",
    ]
    interface = UserInterface()
    for query in queries:
        print(interface.make_conversation(query=query))
