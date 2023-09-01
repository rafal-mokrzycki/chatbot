#!/usr/bin/python
from interface import make_conversation


# TODO: add possiblity to deal with multiple questions from users
def main(verbose: bool = False):
    queries = [
        "Jakie powinny być marginesy w pracy?",
        "Jak zmienić promotora?",
        "Czy mogę zmienić formę studiów?",
        "Kim był Kopernik?",
        "Kiedy wybuchła I wojna światowa?",
        "Ile mieszkańców ma Warszawa?",
    ]

    for query in queries:
        print(100 * "#")
        print(query)
        print(make_conversation(query=query, verbose=verbose))


if __name__ == "__main__":
    main()
