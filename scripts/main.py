#!/usr/bin/python
from interface import UserInterface

# TODO: possibly split functionalities in run.py into 2-3 files with descriptive names
# TODO: add preprocessing
# TODO: add tests
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
