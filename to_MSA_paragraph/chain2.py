from prompts import new_correct_prompt_text, whole_paragraph_organizer_prompt
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_core.output_parsers import JsonOutputParser
from langchain_ibm import WatsonxLLM
from langchain_google_genai import ChatGoogleGenerativeAI
import os, re
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from functools import partial


class ToMSAParagraphChain:
    def __init__(self, path_to_paragraph, chunk_size=80):
    
        self.watson_keys = ["tBmyiiTXb1TYJQPrYHOCjiek8iIQGZoqqZreZwrpSRCM"]
        self.gemini_keys = [
            "AIzaSyA0WgVJxLelaY3fvIhq4XK8Av9udDfJ9rI",
            "AIzaSyDof2hE1nOYkSx3vslyRl696NVoBeXCKH8",
            "AIzaSyC57_NvRsktnNgLvtyutDclVkCS2I4MKDI",
            "AIzaSyDzyMWZB82YyWKzf21k6qdiAn4JG6DXL-Q",
            "AIzaSyC2YG-msSXWXOxnzaxSlEPnQE4scpNLOAc"
        ]
    
        self.gemini_llm = self._initialize_gemini()[0]

        os.environ["WATSONX_APIKEY"] = self.watson_keys[0]
        self.watsonx_llm = WatsonxLLM(
            model_id="sdaia/allam-1-13b-instruct",
            url="https://eu-de.ml.cloud.ibm.com",
            project_id="89b6a9d9-cb31-48fd-b5a4-9ed49fdaab52",
            params={"max_new_tokens": 1536, "temperature": 0},
        )

        try:
            with open(path_to_paragraph, 'r', encoding="utf-8") as f:
                paragraph = f.read()
                words = paragraph.split()
                #words = words[:len(words)//8]
                self.chunks = []
                for i in range(0,len(words), chunk_size):
                    self.chunks.append(" ".join(words[i:i+chunk_size]))
        except Exception as e:
            print(f"Error: {e}")
             
        self.to_MSA_chain = self._build_parallel_chain(self.chunks)


    def _initialize_gemini(self):
        api_key = self.gemini_keys[1]

        self.gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", temperature=0, api_key=api_key
        )
        safety_settings = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }
        # store the original method
        original_generate = ChatGoogleGenerativeAI._generate
        # patch
        ChatGoogleGenerativeAI._generate = partial(
            self.gemini_llm._generate, safety_settings=safety_settings
        )
        self.gemini_llm.google_api_key = api_key
        return self.gemini_llm, original_generate
    
    def _reset_default_gemini_arguments(self, gemini_llm):
        ChatGoogleGenerativeAI._generate = self._initialize_gemini()[1]
        return gemini_llm
    
    def _build_mini_chain(self, chunk):
        llm_chain = (
            RunnableLambda(lambda x: chunk) 
            | new_correct_prompt_text 
            | self.watsonx_llm
            | RunnableLambda(lambda x: x + "\n---------------------------\n") # for splitting the whole text to help the model
        )
        return llm_chain
    
    def _build_parallel_chain(self, chunks):
        tasks = {f"sentence_{idx}": self._build_mini_chain(chunk) for idx, chunk in enumerate(chunks)}
        parallel_chain = (
            RunnableParallel(**tasks) 
            | RunnableLambda(lambda x: x.values())
            | whole_paragraph_organizer_prompt 
            | self._initialize_gemini()[0] 
            | RunnableLambda(self._reset_default_gemini_arguments) 
            | JsonOutputParser()
        ) 
        return parallel_chain

    def __call__(self):
        result = self._build_parallel_chain(self.chunks).invoke({})
        with open("paragraph_processed.txt",'w', encoding="utf-8") as f:
            f.write(result["combined_corrected_text"])
        return None







whole_paragraph_organizer_prompt