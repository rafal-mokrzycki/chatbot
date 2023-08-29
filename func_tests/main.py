import repackage

repackage.up()
from scripts.interface import UserInterface

if __name__ == "__main__":
    interface = UserInterface()
    # TODO: add line question;answer\n by creation of file
    with open(r"func_tests\queries.txt", "r") as q:
        with open(r"func_tests\answers.csv", "w") as a:
            for query in q.readlines():
                answer = interface.make_conversation(query=query)
                result = query.replace("\n", "") + ";" + answer + "\n"
                a.write(result)
