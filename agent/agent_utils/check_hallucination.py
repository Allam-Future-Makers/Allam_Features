import sys, os

# Add the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_prompts.check_hallucination_prompt import prompt
from agent_prompts.ReAct_system_template import ReActTemp

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.output_parsers import JsonOutputParser

class HallucinationChain:
    def __init__(self, instance):
        self.instance = instance

    def __call__(self, query, answer, ReAct_messages): 
        """
        helper function used to check if there is hallucination in the answer or not. 
        """
        self.ReAct_temp_object = ReActTemp(self.instance)
        self.system = self.ReAct_temp_object.update_system_template()

        gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key=self.instance.gemini_keys[self.instance.iterator % len(self.instance.gemini_keys)])
        
        hallucination_grader = prompt | gemini_llm | JsonOutputParser()
        print("\\\\\n",query, "\\\\\n" , answer, len(ReAct_messages), len(self.system))
        result = hallucination_grader.invoke({"query": query, "answer": answer, "messages":ReAct_messages, "ReAct_system_template": self.system})['is_hallucinating']

        self.instance.iterator +=1
        return result