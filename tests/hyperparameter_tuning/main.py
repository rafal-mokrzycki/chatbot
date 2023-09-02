import os
from pathlib import Path

import repackage

repackage.up(2)

from scripts.interface import make_conversation


def main(verbose=False):
    # file to take queries from
    queries_file_path = Path(__file__).parent.joinpath("queries.txt")

    # target file to write queries and answers to
    answers_file_path = Path(__file__).parent.joinpath("answers.csv")

    # target file header
    header = "question;score;answer\n"

    # if target file does not exist, create it
    if not os.path.isfile(answers_file_path):
        with open(answers_file_path, "w", encoding="utf-8") as f:
            f.write(header)

    # read queries, perform conversation and write queries and answers into trget file
    with open(queries_file_path, "r", encoding="utf-8") as q:
        with open(answers_file_path, "a", encoding="utf-8") as a:
            for query in q.readlines():
                answer = make_conversation(query=query, verbose=verbose) + "\n"
                final_query = query.replace("\n", "")
                final_answer = (
                    answer.replace("score: ", "")
                    .replace(".", ",", 1)
                    .replace(" ", ";", 1)
                )
                result = f"{final_query};{final_answer}"
                a.write(result)


if __name__ == "__main__":
    main(verbose=True)
