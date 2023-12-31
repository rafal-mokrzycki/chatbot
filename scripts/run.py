#!/usr/bin/python
import argparse

import repackage
from loader import PineconeIndex

repackage.up()
from interface import make_conversation

from config.config import load_config


def main():
    pi = PineconeIndex()

    config = load_config()
    parser = argparse.ArgumentParser(
        prog="ChatBot",
        description="",
        epilog="",
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
        const=config["pinecone"]["namespace"]["raw"],
        type=str,
    )
    group.add_argument(
        "--load_data",
        help="Loads data from a given file into a Pinecone index.",
        nargs="?",
        const=config["pinecone"]["target_filename"]["raw"],
        type=str,
    )
    group.add_argument(
        "--make_conversation",
        help="Enables to talk with chatbot.",
        nargs="?",
        const="aaa",
        type=str,
    )
    parser.add_argument("-v", "--verbose", action="store_true")
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
        pi.load_data_into_index(vars(args)["load_data"])
    elif args.make_conversation:
        while True:
            query = input("O co chcesz mnie zapytać?\n")
            if query == "q":
                break
            print(make_conversation(query=query, verbose=vars(args)["verbose"]))


if __name__ == "__main__":
    main()
