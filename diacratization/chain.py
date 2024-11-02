
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_core.output_parsers import JsonOutputParser
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableParallel
from langchain_ibm import WatsonxLLM
from langchain_google_genai import ChatGoogleGenerativeAI

from diacratization.prompts import tashkeel_prompt, verification_prompt, whole_paragraph_organizer_prompt
import os, time, math
from functools import partial


class DiacratizeChain:
    def __init__(self, instance, chunk_size=50):
    
        # Set up variables
        self.instance = instance
         
        self.watson_key = instance.watsons['key']
        self.watson_project_id = instance.watsons['project_id']
        self.gemini_keys= instance.gemini_keys
        self.chunk_size = chunk_size

        # Initialize models
        model_params = {
            "max_new_tokens": 1536,
            "min_new_tokens": 0,
            "temperature": 0.00,
        }

        self.watsonx_llm = WatsonxLLM(
            project_id= self.watson_project_id,
            apikey= self.watson_key,
            model_id="sdaia/allam-1-13b-instruct",
            url="https://eu-de.ml.cloud.ibm.com",
            params=model_params
        )

        self.gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            temperature=0, 
            api_key=self.instance.gemini_keys[self.instance.iterator%len(self.instance.gemini_keys)]
        )



    def _initialize_gemini(self, gemini_llm):
        
        self.gemini_llm = gemini_llm

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

        return self.gemini_llm, original_generate
    
    def _reset_default_gemini_arguments(self, gemini_llm):
        ChatGoogleGenerativeAI._generate = self._initialize_gemini(self.gemini_llm)[1]
        return gemini_llm
    

    def _build_mini_chain(self, chunk):
        llm_chain = (
            RunnableLambda(lambda x: chunk) 
            | tashkeel_prompt 
            | self.watsonx_llm
            | {"original": RunnableLambda(lambda x: chunk), "diacritized": RunnablePassthrough()}
            | verification_prompt
            | self.watsonx_llm
            | RunnableLambda(lambda x: x.strip() + "\n-----------\n") # for splitting the whole text to help the model
        )
        return llm_chain



    def _build_parallel_chain(self, chunks):
        tasks = {f"chunk_{idx}": self._build_mini_chain(chunk) for idx, chunk in enumerate(chunks)}
        parallel_chain = (
            RunnableParallel(**tasks) 
            | RunnableLambda(lambda x: " ".join(list(x.values())))
            | whole_paragraph_organizer_prompt 
            | self._initialize_gemini(self.gemini_llm)[0] 
            | RunnableLambda(self._reset_default_gemini_arguments) 
            | JsonOutputParser()
        ) 
        return parallel_chain
    
    def _build_main_chain(self, splits):
        tasks = {f"split_{idx}": self._build_parallel_chain(splt) for idx, splt in enumerate(splits)}
        main_chain = (
            RunnableParallel(**tasks)
            | RunnableLambda(lambda x : "\n-----------\n".join([i['combined_diacratized_text'] for i in list(x.values())]) )
            | whole_paragraph_organizer_prompt
            | self._initialize_gemini(self.gemini_llm)[0] 
            | RunnableLambda(self._reset_default_gemini_arguments) 
            | JsonOutputParser()
        )
        return main_chain


    def __call__(self, paragraph):

        try:
            self.splits = [] 
            for i in range(math.ceil(len(paragraph)/8000)):
                splt = paragraph[i*8000: (i*8000)+8000]
                words = splt.split()
                self.chunks = []
                for i in range(0,len(words), self.chunk_size):
                    self.chunks.append(" ".join(words[i:i+self.chunk_size]))
                self.splits.append(self.chunks)

        except Exception as e:
            print(f"Error: {e}")

        if len(self.splits) == 1:
            result = self._build_parallel_chain(self.chunks).invoke({})
        else:
            result = self._build_main_chain(self.splits).invoke({})

        self.instance.iterator += 1

        return result
