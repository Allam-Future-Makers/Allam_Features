import sys, os, re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from HolyQuran.scripts.run_search import search_quran
from HolyQuran.scripts.run_indexing import index_quran
from HolyQuran.prompts import ayah_prompt_allam, ayah_prompt_gemini
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from langchain_ibm import WatsonxLLM
from langchain_google_genai import ChatGoogleGenerativeAI


class HolyQuranChain:
    def __init__(self, instance):
        index_quran()  # created indices are stored here: sudo ls /var/lib/elasticsearch/indices/
        self.instance = instance

        # Initialize models
        self.model_params = {
            "max_new_tokens": 1536,
            "min_new_tokens": 0,
            "temperature": 0.00,
        }


    def _get_similar_context(self, query):
        res, hits, best_hit = search_quran(query)
        context = []
        c = ""
        for i,hit in enumerate(hits[:3], start=1):
            d = hit["_source"] 
            c = c + 'نص_الآية' + " " + d['Ayah'] + " " 
            c = c + 'إعراب_الآية' +  d['I3rab'] + " "
            c = c + 'تفسير_الآية' + d['Tafseer_Saadi'] + " "
            c = c + 'التلاوة_و_القراءة_الصحيحة_للآية_عبر_رابط_لمقطع_صوتى' + d['telawa'] + " "
            context.append(f"النص_{i}" + str(c))
            with open("test.txt", "a") as f:
                f.write(str(context)) 

        return "\n".join(context)

    def get_results(self, query):

        self.watsonx_llm = WatsonxLLM(
            project_id=self.instance.watsons["project_id"],
            apikey=self.instance.watsons["key"],
            model_id="sdaia/allam-1-13b-instruct",
            url="https://eu-de.ml.cloud.ibm.com",
            params=self.model_params,
        )

        self.gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            api_key=self.instance.gemini_keys[
                self.instance.iterator % len(self.instance.gemini_keys)
            ],
        )

        try:
            def log(x):
                print("From Allam: --- ", x)
                return x

            chain = (
                {
                    "query": RunnablePassthrough(),
                    "context": RunnableLambda(self._get_similar_context),
                }
                | ayah_prompt_allam
                | self.watsonx_llm
                | RunnableLambda(lambda x: log)
                | JsonOutputParser()
            )
            result = chain.invoke(query)["answer"]
            links = re.findall(r"http[|s]?://[^\s]+", result)

            print("Allam\n")
        except:
            try:
                chain = (
                    {
                        "query": RunnablePassthrough(),
                        "context": RunnableLambda(self._get_similar_context),
                    }
                    | ayah_prompt_gemini
                    | self.gemini_llm
                    | JsonOutputParser()
                )
                result = chain.invoke(query)["answer"]
                links = re.findall(r"http[|s]?://[^\s]+", result)
                print("Gemini\n")
            except Exception as e:
                print(f"Error has occured:{e}")

        self.instance.iterator += 1
        if links:
            pattern = r"http[s]?://\S+"
            # Remove the URL from the text
            result = re.sub(pattern, "", result).replace("الرابط","المقطع الصوتي")
        return result, links

    def __call__(self, query):
        result, links = self.get_results(query)
        return result
