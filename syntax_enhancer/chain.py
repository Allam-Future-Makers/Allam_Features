import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sytax_enhancer.prompts import syntax_enhance_allam_prompt, syntax_enhance_gemini_prompt

from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_core.output_parsers import JsonOutputParser
from langchain_ibm import WatsonxLLM
from langchain_google_genai import ChatGoogleGenerativeAI
import os, math, time
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from functools import partial


class SyntaxEnhancerChain:
    def __init__(self, instance):
        
        # Set up variables
        self.instance = instance
        self.watson_key = instance.watsons['key']
        self.watson_project_id = instance.watsons['project_id']
        self.gemini_keys= instance.gemini_keys

        # Initialize models
        self.model_params = {
            "max_new_tokens": 1536,
            "min_new_tokens": 0,
            "temperature": 0.2,
        }


    def __call__(self, sentence):

        self.allam_llm = WatsonxLLM(
            project_id= self.watson_project_id,
            apikey= self.watson_key,
            model_id="sdaia/allam-1-13b-instruct",
            url="https://eu-de.ml.cloud.ibm.com",
            params=self.model_params
        )

        self.gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            temperature=0.2, 
            api_key=self.gemini_keys[self.instance.iterator%len(self.gemini_keys)]
        )

        try:
            chain = syntax_enhance_allam_prompt | self.allam_llm | JsonOutputParser()
            json_result = chain.invoke({"sentence":sentence})
        except:
            try:
                chain = syntax_enhance_gemini_prompt | self.gemini_llm | JsonOutputParser()
                json_result = chain.invoke({"sentence":sentence})
            except Exception as e:
                print("Error: {e}")

        self.instance.iterator += 1
        
        return json_result
