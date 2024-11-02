from chain import HolyQuranChain
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

    def main(self, query):
    
        chain = HolyQuranChain(self)
        
        s = time.time()
        result = chain(query)
        with open("query_answer.txt",'w', encoding="utf-8") as f:
            f.write(result)
        e = time.time()
        print(f"Coversion Ellapsed: {e-s : 0.8f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Path to the paragraph text.")
    parser.add_argument(
        "query", type=str, help="The query asked"
    )
    args = parser.parse_args()
    main_cls = Main()
    main_cls.main(args.query)