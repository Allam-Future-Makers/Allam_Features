import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Mo3gam_Search.scripts.run_search import search_mo3gam
from Mo3gam_Search.scripts.run_indexing import index_mo3gam
from Mo3gam_Search.prompts import mo3gam_search_prompt
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from langchain_ibm import WatsonxLLM
from langchain_google_genai import ChatGoogleGenerativeAI

class Mo3gamSearchChain:
    def __init__(self, instance):
        index_mo3gam()  # created indices are stored here: sudo ls /var/lib/elasticsearch/indices/
        self.instance = instance

        # Initialize models
        self.model_params = {
            "max_new_tokens": 1536,
            "min_new_tokens": 0,
            "temperature": 0.00,
        }

    def _get_similar_context(query):
        result, hits, best_hit = search_mo3gam(query)
        context = ""
        for i,hit in enumerate(hits[:3]):
            res = hit["_source"]["mo3gam_verse"]
            context = context + f"context_{i}: {res}"
        return context
    
    def _get_similar_context_small(self,query):
        result, hits, best_hit = search_mo3gam(query)
        context = ""
        for i,hit in enumerate(hits[:1]):
            res = hit["_source"]["mo3gam_verse"]
            context = context + f"context_{i}: {res}"
        return context

    def __call__(self, word, helper_sentence):

        if helper_sentence:
            query = f"""
                        اكشف فى المعجم عن كلمة
                        {word}
                        فى جملة:
                        {helper_sentence}
                    """
        else:
            query = f"""
                        اكشف فى المعجم عن كلمة
                        {word}
                    """

        self.watsonx_llm = WatsonxLLM(
            project_id= self.instance.watsons['project_id'],
            apikey= self.instance.watsons['key'],
            model_id="sdaia/allam-1-13b-instruct",
            url="https://eu-de.ml.cloud.ibm.com",
            params=self.model_params
        )

        self.gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro", 
            temperature=0, 
            api_key=self.instance.gemini_keys[self.instance.iterator% len(self.instance.gemini_keys)]
        )

        
        try:
            chain =(
                {"query": RunnablePassthrough(),"context": RunnableLambda(self._get_similar_context)}
                | mo3gam_search_prompt
                | self.gemini_llm
                | JsonOutputParser()
            )
            json_result = chain.invoke(query)
        except:
            try:
                chain =(
                    {"query": RunnablePassthrough(),"context": RunnableLambda(self._get_similar_context_small)}
                    | mo3gam_search_prompt
                    | self.gemini_llm
                    | JsonOutputParser()
                )
                json_result = chain.invoke(query)
            except Exception as e:
                print(f"Error has occured:{e}")
        
        self.instance.iterator += 1
        return json_result['answer']