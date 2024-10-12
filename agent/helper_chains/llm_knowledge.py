import sys
if "../" not in sys.path:
    sys.path.append("../")

from prompts.llm_knowledge_prompt import llm_knowledge_prompt
from utils.initialize_gemini import initialize_gemini
from helper_chains.summarization_chain import SummarizationChain

from langchain_core.output_parsers import StrOutputParser
from termcolor import colored
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

class llm_knowledge_chain:
    """
    This class leverages a large language model (LLM) to responed to user queries 
    that cannot be answered from web_search or from vectorstore.
    """
    def __init__(self):
        self.summarization_object = SummarizationChain() # for memory purposes.

    def __call__(self, query):
        """
        Processes a query using an LLM knowledge chain.

        Args:
            query (str): The input query.

        Returns:
            str: The answer generated by the LLM based on its knowledge.
        """
        # Load conversation history (if any) for chat-memory purposes
        self.history = self.summarization_object.get_summary()

        # Initialize the model       
        self.llm_knowledge_model = initialize_gemini(api_config_path="config/api4.yaml")
        
        # Build the LLM knowledge chain
        chain = (
                {"question": RunnablePassthrough(), "history":  RunnableLambda(lambda x: self.history)}
                | llm_knowledge_prompt
                | self.llm_knowledge_model
                | StrOutputParser()
        )
        # Execute the chain and return the answer
        return chain.invoke(query)
        