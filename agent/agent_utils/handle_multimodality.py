import requests, base64, sys, os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_prompts import image_modality_prompt 
from agent_utils.ocr_api_tool import ScanDocFlowOcr
from agent_utils.main_agent import MainAgent


class HandleMultiModality:
    def __init__(self, instance, query: str = "", voice_path: str = "", image_path: str = ""):
        self.instance = instance
        self.gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            api_key= instance.gemini_keys[instance.iterator%len(instance.gemini_keys)]
        )
        
        self.main_agent_object = MainAgent(self.instance)

        self.query = query
        self.voice_path = voice_path
        self.image_path = image_path

        mode_bin = mode_bin = "{:d}{:d}{:d}".format(bool(self.image_path), bool(self.voice_path), bool(self.query))
        self.mode = int(mode_bin, 2)
    
    def voice2txt(self, voice_path:str):
        API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
        headers = {"Authorization": "Bearer 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"}
        with open(voice_path, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        transcript = response.json()['text']
        return transcript
    
    def img2txt(self, image_path:str):
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
        
        chain = image_modality_prompt.prompt | self.gemini_llm | JsonOutputParser()
        try:
            result = chain.invoke({"query":self.query, "image_data":image_data})
        except:
            return self.img2txt(image_path)
        self.instance.iterator +=1
        description = result['precise_description'] 
        query_answer = result['query_answer']
        needs_ocr = result['needed_ocr']
        language = result['language']

        if needs_ocr and (language.lower() == 'arabic'):
            text_in_image = self.get_text_via_ocr(image_path)
            answered = False
            return answered, description, text_in_image
        else:
            answered = True
            return answered, description, query_answer
    
    def get_text_via_ocr(self,image_path):
        ocr_object = ScanDocFlowOcr(self.instance)
        return ocr_object(image_path)

    def invoke(self):
        if self.mode == 1:
            """query only as input"""
            final_query = self.query
            answer = self.main_agent_object(final_query)
            return answer
        elif self.mode == 2:
            """voice only as input"""
            final_query = self.voice2txt(self.voice_path)
            answer = self.main_agent_object(final_query)
            return answer
        elif self.mode == 3:
            """query + voice as input"""
            final_query = f"query: {self.query}\n audio_transcript: {self.voice2txt(self.voice_path)}"
            answer = self.main_agent_object(final_query)
            return answer
        elif self.mode == 4:
            """image only as input --> output is the image description"""
            _1, _2, _3 = self.img2txt(self.image_path)
            answer = _2
            return answer
        elif self.mode == 5:
            """query + image as input"""
            _1 , _2, _3  = self.img2txt(self.image_path)
            if _1:
                answer = _3
                return answer
            else:
                final_query = f"query: {self.query}\n image_description: {_2}\n image_text: {_3}"
                answer = self.main_agent_object(final_query)
                return answer
        elif self.mode == 6:
            """image + voice as input"""
            self.query = f"transcript_query: {self.voice2txt(self.voice_path)}"
            _1 , _2, _3  = self.img2txt(self.image_path)
            if _1:
                answer = _3
                return answer
            else:
                final_query = f"query: {self.query}\n image_description: {_2}\n image_text: {_3}"
                answer = self.main_agent_object(final_query)
                return answer
        elif self.mode == 7:
            """query + image + voice as input"""
            self.query = f"query: {self.query}\n transcript_query: {self.voice2txt(self.voice_path)}"
            _1 , _2, _3  = self.img2txt(self.image_path)
            if _1:
                answer = _3
                return answer
            else:
                final_query = f"query: {self.query}\n image_description: {_2}\n image_text: {_3}"
                answer = self.main_agent_object(final_query)
                return answer
    
    def __call__(self):
        return self.invoke()

