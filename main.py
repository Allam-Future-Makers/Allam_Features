import requests
def voice2text(filename):
    
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {"Authorization": "Bearer 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"}
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


class HandleMultiModality:
    def __init__(self):
        pass

    def voice2text(self, file_path):    
        API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
        headers = {"Authorization": "Bearer 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"}
        with open(file_path, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()




def handle_multimodality(inp_type, input_path):
    if inp_type=='audio':
        try:
            output = voice2text(input_path)
            content = output['text']
        except Exception as e:
            print(f"Error: {e}")

    elif inp_type=='image_text':


    elif inp_type=='audio_image':