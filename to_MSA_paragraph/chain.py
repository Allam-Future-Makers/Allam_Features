from prompts import correct_prompt_paragraph, correct_parser_prompt_paragraph, critic_prompt_paragraph, critic_parser_prompt_paragraph
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from langchain_ibm import WatsonxLLM
from langchain_google_genai import ChatGoogleGenerativeAI
import os, re

class ToMSAParagraphChain:
    def __init__(self, cares_about_requests=False):
        self.iterator = 0
        self.cares_about_requests = cares_about_requests
        self.watson_keys = ["tBmyiiTXb1TYJQPrYHOCjiek8iIQGZoqqZreZwrpSRCM"]
        self.gemini_keys = ["AIzaSyA0WgVJxLelaY3fvIhq4XK8Av9udDfJ9rI", "AIzaSyDof2hE1nOYkSx3vslyRl696NVoBeXCKH8", "AIzaSyC57_NvRsktnNgLvtyutDclVkCS2I4MKDI", "AIzaSyDzyMWZB82YyWKzf21k6qdiAn4JG6DXL-Q"]
        self.watsonx_llm, self.gemini_llm = self._initialize_LLMs(self.iterator)
        self.to_MSA_chain = self._build_chain()

    def _initialize_LLMs(self, id):
        os.environ['WATSONX_APIKEY'] = self.watson_keys[id % 1]
        os.environ["GOOGLE_API_KEY"] = self.gemini_keys[id % 4]

        self.watsonx_llm = WatsonxLLM(
            model_id="sdaia/allam-1-13b-instruct",
            url="https://eu-de.ml.cloud.ibm.com",
            project_id="89b6a9d9-cb31-48fd-b5a4-9ed49fdaab52",
            params={
                "max_new_tokens": 1536,
                "temperature": 0.2
            }
        )
        self.gemini_llm = ChatGoogleGenerativeAI(model= 'gemini-1.5-flash', temperature=0)
        return self.watsonx_llm, self.gemini_llm

    def _build_chain(self):
        llm_chain = (
            correct_prompt_paragraph | self.watsonx_llm | correct_parser_prompt_paragraph | self.gemini_llm | JsonOutputParser() 
            | {"sentence": RunnablePassthrough()} 
            | critic_prompt_paragraph | self.watsonx_llm | critic_parser_prompt_paragraph | self.gemini_llm | JsonOutputParser() 
        )
        return llm_chain
    
    def _process_paragraph(self, chain, paragraph, chunk_size=60):

        words = paragraph.split()
        waiting_messages = ["Patience is a virtue. Thanks for waiting!", "Almost there! Your answer is coming soon.", "Hang tight...", "See the gears turning as our AI processes your request...", "Watch as our AI works its magic"]
        processed_paragraph = ""
        
        with open("to_MSA.txt", 'w') as f:
            f.write("")
        i=0
        j=0
        iterator=0
        summary = ""
        past_sentence = "لا يوجد نص سابق حيث أن النص الغير مصحح التالى المعطى لك هو بداية الكلام"
        while i < len(words):
            print(waiting_messages[iterator % len(waiting_messages)])
            iterator += 1 
            for j in  words[i:i+chunk_size: -1]:
                if j.endswith('.'):
                    break 
            
            chunk = " ".join(words[i:i+chunk_size-j])
            # Modify the chain to process the chunk'
            while True:
                try:
                    result = chain.invoke({"sentence": chunk, "past_sentence": past_sentence})
                    break
                except: 
                    continue
            past_sentence = words[i:(i+chunk_size-j)//4] 
            i = i+chunk_size-j  
            try:
                current_chunk_processed = result['finally_corrected_text']
            except:
                response = str(result)
                pattern_correct = r'"finally_corrected_text":\s*"([^"]*)"'
                current_chunk_processed = re.findall(pattern_correct, response)[0]
            with open("to_MSA.txt", 'a') as f:
                f.write(str(current_chunk_processed))
            processed_paragraph += current_chunk_processed + "\n"
        return processed_paragraph
    
    def __call__(self, path_to_paragraph):
        if self.cares_about_requests:
            self.iterator += 1
            self.watsonx_llm, self.gemini_llm = self._initialize_LLMs(self.iterator)
        with open(path_to_paragraph,'r') as f:
            self.paragraph = f.read() 
        self.llm_chain = self._build_chain()
        return self._process_paragraph(self.llm_chain, self.paragraph)