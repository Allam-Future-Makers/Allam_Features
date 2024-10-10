from chain import ToMSAParagraphChain
from termcolor import colored
import argparse


def main(path_to_paragraph):
    try:
        with open(path_to_paragraph,'r') as f:
            paragraph = f.read()
            chain = ToMSAParagraphChain()
            result = chain(paragraph)
    except Exception as e:
        print(f"Error: {e}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Path to the paragraph text.")
    parser.add_argument(
        "file_name", type=str, help="The paragraph text file to process"
    )
    args = parser.parse_args()
    main(args.file_name)
