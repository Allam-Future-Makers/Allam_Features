from Allam_Features.to_MSA_paragraph.prompts import new_correct_prompt_text, whole_paragraph_organizer_prompt, whole_paragraph_organizer_prompt_in_case_of_long_context
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_core.output_parsers import JsonOutputParser
from langchain_ibm import WatsonxLLM
from langchain_google_genai import ChatGoogleGenerativeAI
import os, math, time
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from functools import partial


class ToMSAParagraphChain:
    def __init__(self, chunk_size=50):
        
        self.chunk_size = chunk_size
        self.watson_keys = ["tBmyiiTXb1TYJQPrYHOCjiek8iIQGZoqqZreZwrpSRCM"]
        self.gemini_keys = [
            "AIzaSyA0WgVJxLelaY3fvIhq4XK8Av9udDfJ9rI",
            "AIzaSyDof2hE1nOYkSx3vslyRl696NVoBeXCKH8",
            "AIzaSyC57_NvRsktnNgLvtyutDclVkCS2I4MKDI",
            "AIzaSyDzyMWZB82YyWKzf21k6qdiAn4JG6DXL-Q",
            "AIzaSyC2YG-msSXWXOxnzaxSlEPnQE4scpNLOAc"
        ]
    
        self.gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", temperature=0, api_key=self.gemini_keys[0]
        )


        os.environ["WATSONX_APIKEY"] = self.watson_keys[0]
        self.watsonx_llm = WatsonxLLM(
            model_id="sdaia/allam-1-13b-instruct",
            url="https://eu-de.ml.cloud.ibm.com",
            project_id="89b6a9d9-cb31-48fd-b5a4-9ed49fdaab52",
            params={"max_new_tokens": 1536, "temperature": 0},
        )

    
        

    def log(self, x):
        print(x)
        print("--------------")
        return x
    

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
            | new_correct_prompt_text 
            | self.watsonx_llm
            | RunnableLambda(lambda x: x + "\n-----------\n") # for splitting the whole text to help the model
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
            | RunnableLambda(lambda x : "\n-----------\n".join([i['combined_corrected_text'] for i in list(x.values())]) )
            | whole_paragraph_organizer_prompt_in_case_of_long_context
            | self._initialize_gemini(self.gemini_llm)[0] 
            | RunnableLambda(self._reset_default_gemini_arguments) 
            | JsonOutputParser()
        )
        return main_chain

    def __call__(self, paragraph):
        self.splits = [] 
        for i in range(math.ceil(len(paragraph)/8000)):
            splt = paragraph[i*8000: (i*8000)+8000]
            words = splt.split()
            self.chunks = []
            for i in range(0,len(words), self.chunk_size):
                self.chunks.append(" ".join(words[i:i+self.chunk_size]))
            self.splits.append(self.chunks)

        self.to_MSA_chain = self._build_parallel_chain(self.chunks)

        s = time.time()

        if len(self.splits) == 1:
            result = self._build_parallel_chain(self.chunks).invoke({})
        else:
            result = self._build_main_chain(self.splits).invoke({})

        with open("paragraph_processed.txt",'w', encoding="utf-8") as f:
            final_result = result["combined_corrected_text"].strip().strip('}')
            f.write(final_result)
        
        e = time.time()
        print(f"Coversion Ellapsed: {e-s : 0.8f} seconds")
        return final_result
