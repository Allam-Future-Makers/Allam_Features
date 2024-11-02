from chain import IrabChain
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

    def main(self, path_to_paragraph):
        with open(path_to_paragraph, 'r') as f:
            paragraph = f.read()
        
        chain = IrabChain(self)
        
        s = time.time()
        result = chain(paragraph)
        with open("paragraph_irabed.txt",'w', encoding="utf-8") as f:
            f.write(result)
        e = time.time()
        print(f"Coversion Ellapsed: {e-s : 0.8f} seconds")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Path to the paragraph text.")
    parser.add_argument(
        "file_name", type=str, help="The paragraph text file to process"
    )
    args = parser.parse_args()
    main_cls = Main()
    main_cls.main(args.file_name)
