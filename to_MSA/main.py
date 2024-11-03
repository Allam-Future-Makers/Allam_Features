from chain import ToMSAChain
import argparse, time

class Main:
    def __init__(self):
        self.watsons = {
            'key' : "tBmyiiTXb1TYJQPrYHOCjiek8iIQGZoqqZreZwrpSRCM",
            'project_id' : "89b6a9d9-cb31-48fd-b5a4-9ed49fdaab52"
        }
        self.gemini_keys = [
            "AIzaSyA0WgVJxLelaY3fvIhq4XK8Av9udDfJ9rI",
            "AIzaSyDof2hE1nOYkSx3vslyRl696NVoBeXCKH8",
            "AIzaSyC57_NvRsktnNgLvtyutDclVkCS2I4MKDI",
            "AIzaSyDzyMWZB82YyWKzf21k6qdiAn4JG6DXL-Q",
            "AIzaSyC2YG-msSXWXOxnzaxSlEPnQE4scpNLOAc"
        ]
        self.iterator = 0

    def main(self, paragraph):

        chain = ToMSAChain(self)
        
        s = time.time()
        text_result = chain(paragraph)
        e = time.time()
        print(f"Coversion Ellapsed: {e-s : 0.8f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Path to the paragraph text.")
    parser.add_argument(
        "paragraph", type=str, help="paragraph_to_be_processed"
    )
    args = parser.parse_args()
    main_cls = Main()
    main_cls.main(args.paragraph)