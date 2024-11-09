from chain import Mo3gamSearchChain
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

    def main(self, word, helper_sentence):
    
        chain = Mo3gamSearchChain(self)
        
        s = time.time()
        json_result = chain(word, helper_sentence)
        e = time.time()
        print(f"Coversion Ellapsed: {e-s : 0.8f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inputs of word and helper_sentence")
    parser.add_argument(
        "word", type=str, help="The given word."
    )
    parser.add_argument(
        "helper_sentence", nargs='?', default="", type=str, help="The optional helper sentence."
    )
    args = parser.parse_args()
    main_cls = Main()
    main_cls.main(args.word, args.helper_sentence)