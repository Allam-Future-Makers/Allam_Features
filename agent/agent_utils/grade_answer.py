import sys, os

# Add the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_prompts.grade_answer_prompt import prompt
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.output_parsers import JsonOutputParser

class GradeAnswerChain:
    def __init__(self, instance):
        self.instance = instance
    
    def __call__(self, query, answer):
        """
        helper function used to grad the answer as good answer or bad answer. 
        """
        gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key=self.instance.gemini_keys[self.instance.iterator % len(self.instance.gemini_keys)])
        
        answer_grader = prompt | gemini_llm | JsonOutputParser()
        result = answer_grader.invoke({"query": query, "answer": answer})['is_good_answer']

        self.instance.iterator += 1

        return result
    