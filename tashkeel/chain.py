from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_ibm import WatsonxLLM
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import tashkeel_prompt, verification_prompt, gemini_prompt
import os
import json
import re


class TashkeelChain:
    def __init__(self):
        self._initialize_llms()
        self.chain = self._build_chain()

    def _initialize_llms(self):
        os.environ["WATSONX_APIKEY"] = "tBmyiiTXb1TYJQPrYHOCjiek8iIQGZoqqZreZwrpSRCM"
        os.environ["GOOGLE_API_KEY"] = "AIzaSyA0WgVJxLelaY3fvIhq4XK8Av9udDfJ9rI"

        self.watsonx_llm = WatsonxLLM(
            model_id="sdaia/allam-1-13b-instruct",
            url="https://eu-de.ml.cloud.ibm.com",
            project_id="89b6a9d9-cb31-48fd-b5a4-9ed49fdaab52",
            params={"max_new_tokens": 1536, "temperature": 0.0},
        )
        self.gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", temperature=0
        )

    def _build_chain(self):
        initial_tashkeel = (
            {"sentence": RunnablePassthrough()} | tashkeel_prompt | self.watsonx_llm
        )

        verification = (
            {"original": lambda x: x["sentence"], "diacritized": initial_tashkeel}
            | verification_prompt
            | self.watsonx_llm
            | RunnableLambda(lambda x: x.strip())
        )

        return (
            {"old": verification, "sentence": lambda x: x["sentence"]}
            | gemini_prompt
            | self.gemini_llm
            | RunnableLambda(
                lambda x: self._extract_diacritized_from_content(x.content)
            )  # Access content and extract diacritized part
        )

    def _extract_diacritized_from_content(self, content):
        # Try to extract JSON from the content
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            try:
                parsed_output = json.loads(json_match.group())
                if "diacritized" in parsed_output:
                    return parsed_output["diacritized"].strip()
                elif "original" in parsed_output and "diacritized" in parsed_output:
                    return parsed_output["diacritized"].strip()
            except json.JSONDecodeError:
                pass  # If JSON parsing fails, we'll fall back to the original content

        # If JSON extraction fails, return the entire content
        return content.strip()

    def __call__(self, sentence):
        try:
            return self.chain.invoke({"sentence": sentence})
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            # You might want to add more specific error handling here
            return None
