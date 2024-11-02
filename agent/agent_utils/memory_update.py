import sys, os
# Add the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_prompts.memory_update_prompt import prompt
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI


class MemoryUpdateChain:
    def __init__(self,instance):
        self.instance = instance 

    def update_memory(self, query_answer):
        with open(os.path.join("agent_memory", f"memory_for_user_{self.instance.id}.txt"), "r") as f:
            current_memory_content = f.read()
        
        gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=self.instance.gemini_keys[self.instance.iterator % len(self.instance.gemini_keys)])
        chain = prompt | gemini_llm | JsonOutputParser()
        result = chain.invoke({"query_answer":query_answer, "memory_content":current_memory_content})

        self.instance.iterator += 1

        for k, v in result.items():
            current_memory_content =  f"{k} : {v}\n"
        
        with open(os.path.join("agent_memory", f"memory_for_user_{self.instance.id}.txt"), "w") as f:
            f.write(current_memory_content)

        return None
