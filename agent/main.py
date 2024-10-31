from agent_utils.handle_multimodality import HandleMultiModality

class Main:
    def __init__(self):

        # multimodality variables
        self.query = ""
        self.voice_path = ""
        self.image_path = ""

        # api-related variables
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
        self.ocr_keys = ["V54R51Hw76NjxTksiDS7BjxOOBuVJcKoZQEcLkGvio8Qn9D09KCisTkqDDaKBUGV"]
        self.iterator = 0


    def  __call__(self, query:str="", voice_path:str="", image_path:str="" ):
        modality_handler_object = HandleMultiModality(self, query, voice_path, image_path)
        answer = modality_handler_object()
        return answer
