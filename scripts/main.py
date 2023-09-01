#!/usr/bin/python
from interface import make_conversation

# TODO: add possiblity to deal with multiple questions from users
if __name__ == "__main__":
    queries = [
        "Jakie powinny być marginesy w pracy?",
        "Jak zmienić promotora?",
        "Czy mogę zmienić formę studiów?",
        "Kim był Kopernik?",
        "Kiedy wybuchła I wojna światowa?",
        "Ile mieszkańców ma Warszawa?",
    ]

    for query in queries:
        print(query)
        print(make_conversation(query=query))
        print(100 * "#")
