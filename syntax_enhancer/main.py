from chain import SyntaxEnhancerChain
import argparse, time

class Main:
    def __init__(self):
        self.watsons = {
            'key' : "I23GGOrvbVPdcG-MzPGPmxv8Cv7LezjfmmDQT2APmmet",
            'project_id' : "40481c96-7240-4b7d-8d44-08a21aea2013"
        }
        self.gemini_keys = [
            "AIzaSyA0WgVJxLelaY3fvIhq4XK8Av9udDfJ9rI",
            "AIzaSyDof2hE1nOYkSx3vslyRl696NVoBeXCKH8",
            "AIzaSyC57_NvRsktnNgLvtyutDclVkCS2I4MKDI",
            "AIzaSyDzyMWZB82YyWKzf21k6qdiAn4JG6DXL-Q",
            "AIzaSyC2YG-msSXWXOxnzaxSlEPnQE4scpNLOAc"
        ]
        self.iterator = 0

    def main(self, sentence):
        
        chain = SyntaxEnhancerChain(self)
        
        s = time.time()
        json_result = chain(sentence)
        
        e = time.time()
        print(f"Coversion Ellapsed: {e-s : 0.8f} seconds")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="sentence to be processed.")
    parser.add_argument(
        "sentence", type=str, help="sentence to be processed"
    )
    args = parser.parse_args()
    main_cls = Main()
    main_cls.main(args.sentence)
