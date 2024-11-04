import os

from agent.agent_utils.handle_multimodality import HandleMultiModality


class AgentMain:
    def __init__(self, id, verbose=True, grade_answer=True):

        # multimodality variables
        self.query = ""
        self.voice_path = ""
        self.image_path = ""

        # api-related variables
        self.watsons = {
            "key": "I23GGOrvbVPdcG-MzPGPmxv8Cv7LezjfmmDQT2APmmet",
            "project_id": "40481c96-7240-4b7d-8d44-08a21aea2013",
        }
        self.gemini_keys = [
            "AIzaSyA0WgVJxLelaY3fvIhq4XK8Av9udDfJ9rI",
            "AIzaSyDof2hE1nOYkSx3vslyRl696NVoBeXCKH8",
            "AIzaSyC57_NvRsktnNgLvtyutDclVkCS2I4MKDI",
            "AIzaSyDzyMWZB82YyWKzf21k6qdiAn4JG6DXL-Q",
            "AIzaSyC2YG-msSXWXOxnzaxSlEPnQE4scpNLOAc",
        ]
        self.ocr_keys = [
            "V54R51Hw76NjxTksiDS7BjxOOBuVJcKoZQEcLkGvio8Qn9D09KCisTkqDDaKBUGV"
        ]
        self.iterator = 0
        self.id = id
        self.verbose = verbose
        self.grade_answer = grade_answer

        parent_directory = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(
            parent_directory, "agent_memory", f"memory_for_user_{id}.txt"
        )
        if not os.path.exists(data_file_path):
            with open(data_file_path, "w") as f:
                f.write(
                    "There memory file is currently empty because no past query-answer interactions exist"
                )

    def __call__(self, query: str = "", voice_path: str = "", image_path: str = ""):
        modality_handler_object = HandleMultiModality(
            self, query, voice_path, image_path
        )
        answer = modality_handler_object()
        return answer
