from chain import ToMSAParagraphChain
from termcolor import colored
import argparse


def main(path_to_pargraph):
    chain = ToMSAParagraphChain(cares_about_requests=False)
    try:
        file = open(path_to_pargraph, "r", encoding="utf-8")
        file.close()
        chain(path_to_pargraph)
    except:
        print("file path cannot be opened.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Path to the paragraph text.")
    parser.add_argument(
        "file_name", type=str, help="The paragraph text file to process"
    )
    args = parser.parse_args()
    main(args.file_name)
