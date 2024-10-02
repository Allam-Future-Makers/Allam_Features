from chain import ToMSAParagraphChain
from termcolor import colored
import argparse


def main(path_to_paragraph):
    chain = ToMSAParagraphChain(path_to_paragraph= path_to_paragraph, cares_about_requests=True)
    result = chain()
    print(result)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Path to the paragraph text.")
    parser.add_argument(
        "file_name", type=str, help="The paragraph text file to process"
    )
    args = parser.parse_args()
    main(args.file_name)
