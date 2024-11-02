import requests, json, base64, re

class ScanDocFlowOcr:
    def __init__(self, instance):
        self.instance =  instance
        self.access_token = self.instance.ocr_keys[self.instance.iterator%len(self.instance.ocr_keys)]
        self.url = f"https://backend.scandocflow.com/v1/api/documents/extract?access_token={self.access_token}"

    def get_text(self, image_path):
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        payload = json.dumps({
            "type": "ocr",
            "files": [
                {
                "title": "image.jpeg",
                "src": f"data:image/jpeg;base64,{base64_image}"
                }
            ]
        })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.post(self.url, headers=headers, data=payload)    
        response_data = json.loads(response.text)
        # Extract the base64 encoded text
        plain_text_base64 = response_data["documents"][0]["plainTextBase64"]
        # Decode the base64 text
        decoded_text = base64.b64decode(plain_text_base64).decode('utf-8')
        organized_text = "\n".join([" ".join(re.sub(r'\s+', ' ', text_line.strip()).split()[::-1]) for text_line in decoded_text.split("\n")])
        return organized_text
    
    def __call__(self, image_path):
        result = self.get_text(image_path)
        self.instance.interator +=1
        return result