import sys, os

# Add the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_tools.search_web import WebSearch
from agent_prompts.web_search_prompt import prompt

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI

class WebSearchChain:
    """
    This class performs has chain to extract knowledge got from the web_search tool found at `tools.search_web`.
    """

    def __init__(self, instance):
        self.instance = instance

    def __call__(self, query):
        """
        Processes a query using a web search chain.

        Args:
            query (str): The input query.

        Returns:
            str: The retrieved answer.
        """
        # Load conversation history (if any) for chat-memory purposes
        parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_file_path = os.path.join(parent_directory, "agent_memory", f"memory_for_user_{self.instance.id}.txt")
        with open(data_file_path,"r") as f:
            current_memory = f.read()

        # Initialize the model and web_search tool    
        
        gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=self.instance.gemini_keys[self.instance.iterator % len(self.instance.gemini_keys)])
        search_object = WebSearch()

        # Build the chain that gets the answer from the retrieved text by web_search tool
        chain = (
                {"context": search_object.search_query , "question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: current_memory)}
                | prompt
                | gemini_llm
                | JsonOutputParser()
        )
        # Execute the web search chain and return the answer
        result = chain.invoke(query)['answer']

        self.instance.iterator += 1
        return result