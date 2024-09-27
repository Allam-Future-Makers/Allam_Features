from prompts import correct_prompt, correct_parser_prompt, critic_prompt, critic_parser_prompt
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from langchain_ibm import WatsonxLLM
from langchain_google_genai import ChatGoogleGenerativeAI
import os

class ToMSAChain:
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
            correct_prompt | self.watsonx_llm | correct_parser_prompt | self.gemini_llm | JsonOutputParser() 
            | {"sentence": RunnablePassthrough()} 
            | critic_prompt | self.watsonx_llm | critic_parser_prompt | self.gemini_llm | JsonOutputParser() 
        )
        return llm_chain
    
    def __call__(self, sentence):
        if self.cares_about_requests:
            self.iterator += 1
            self.watsonx_llm, self.gemini_llm = self._initialize_LLMs(self.iterator)
        self.llm_chain = self._build_chain()
        return self.llm_chain.invoke({"sentence":sentence})