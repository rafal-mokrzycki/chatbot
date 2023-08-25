import argparse

from config import load_config
from loader import PineconeIndex


def main():
    pi = PineconeIndex()
    config = load_config()
    parser = argparse.ArgumentParser(
        prog="ProgramName",
        description="What the program does",
        epilog="Text at the bottom of help",
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--create_index",
        help="Creates a Pinecone index",
        nargs="?",
        const=config["pinecone"]["index_name"],
        type=str,
    )
    group.add_argument(
        "--recreate_index",
        help="Rereates a Pinecone index",
        nargs="?",
        const=config["pinecone"]["index_name"],
        type=str,
    )
    group.add_argument(
        "--delete_index",
        help="Deletes a Pinecone index.",
        nargs="?",
        const=config["pinecone"]["index_name"],
        type=str,
    )
    group.add_argument(
        "--delete_data",
        help="Deletes all data in a given Pinecone index namespace.",
        nargs="?",
        const="sentences_raw",
        type=str,
    )
    group.add_argument(
        "--load_data",
        help="Loads data from a given file into a Pinecone index.",
        nargs="?",
        const="sentences_raw.csv",
        type=str,
    )
    args = parser.parse_args()
    if args.create_index:
        print(pi.create_index())
    elif args.recreate_index:
        print(pi._delete_index())
        print(pi.create_index())
    elif args.delete_index:
        order = input(f"Are you sure you want to delete index `{pi.index_name}`? [Y/n]\n")
        if order.upper() == "Y":
            pi._delete_index()
    elif args.delete_data:
        pi._delete_data(vars(args)["delete_data"])
    elif args.load_data:
        pi.load_data_into_index("sentences_raw.csv")


if __name__ == "__main__":
    main()