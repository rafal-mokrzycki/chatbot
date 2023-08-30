import os

import repackage

repackage.up()
from pathlib import Path

from scripts.interface import UserInterface


def main():
    interface = UserInterface()

    # file to take queries from
    queries_file_path = Path(__file__).parent.joinpath("queries.txt")

    # target file to write queries and answers to
    answers_file_path = Path(__file__).parent.joinpath("answers.csv")

    # target file header
    header = "question;answer\n"

    # if target file does not exist, create it
    if not os.path.isfile(answers_file_path):
        with open(answers_file_path, "w") as f:
            f.write(header)

    # read queries, perform conversation and write queries and answers into trget file
    with open(queries_file_path, "r") as q:
        with open(answers_file_path, "a") as a:
            for query in q.readlines():
                answer = interface.make_conversation(query=query) + "\n"
                final_query = query.replace("\n", "")
                result = f"{final_query};{answer}"
                a.write(result)


if __name__ == "__main__":
    main()
