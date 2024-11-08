import sys,re, os

# Add the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Add the grandparent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from agent_prompts.ReAct_system_template import ReActTemp

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from datetime import datetime

from agent_utils.web_search import WebSearchChain
from agent_utils.llm_knowledge import LLMKnowledgeChain

from to_MSA.chain import ToMSAChain
from irab.chain import IrabChain
from diacratization.chain import DiacratizeChain
from HolyQuran.chain import HolyQuranChain

from termcolor import colored


class ReActLoop:
    """
    ReActLoop class implements the ReAct loop prompting-technique for processing queries.

    The ReActLoop class manages the interaction between a large language model (LLM)
    and external tools to provide comprehensive and informative responses to user queries.
    """

    def __init__(self, instance):
        """
        Initializes the ReActLoop object.

        Args:
            verbose (bool, optional): Whether to print verbose output. Defaults to True.
        """
        self.instance = instance
        
        self.ReAct_temp_object = ReActTemp(self.instance)
        self.system = self.ReAct_temp_object.update_system_template()
        
        self.messages = []
        if self.system:
            self.messages.append(("system", self.system))

    def _execute(self, message: str = ""):
        """
        Executes one message through the ReAct model.
        This method will be called many times within the main ReAct loop.
        Args:
            message (str, optional): The input message. Defaults to "".

        Returns:
            str: The generated response from the LLM.
        """
        
        self.ReAct_model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            max_output_tokens=None,
            api_key= self.instance.gemini_keys[self.instance.iterator%(len(self.instance.gemini_keys))]
        )
        if message:
            self.messages.append(("user", message))

        result = self.ReAct_model.invoke(ChatPromptTemplate(self.messages).invoke({}))
        print(result.content) if self.instance.verbose else None
        self.instance.iterator +=1

        self.messages.append(("ai", result.content))
        return result.content

    def loop(self, Query):
        """
        Runs the main ReAct loop to process a query.

        Args:
            Query (str): The input query.

        Returns:
            str: The final answer generated by the ReAct loop.
        """

        # define the available tools to be used by ReAct loop actions.

        to_msa = ToMSAChain(self.instance, chunk_size=50)
        irab = IrabChain(self.instance)
        diacratize = DiacratizeChain(self.instance)
        holy_quran = HolyQuranChain(self.instance)
        web_search = WebSearchChain(self.instance)
        llm_knowledge = LLMKnowledgeChain(self.instance)
        get_current_datetime = lambda x: datetime.now().strftime("Today is %A, %Y-%m-%d and the current time is %I:%M:%S %p")

        # Execute the initial prompt
        response = self._execute(Query)
        tool = "None"

        # Main ReAct loop
        for i in range(20):
            # Check for PAUSE in the output and extract the tool and tool input returend from (Action:)
            if "PAUSE" in response and ("answer:" not in response.lower()):
                match = re.findall(
                    r'Action: (to_msa|irab|diacratize|holy_quran|web_search|llm_knowledge|get_current_datetime): (?:\'|")(.*?)(?:\'|")',
                    response,
                )
                if match:
                    tool, tool_input = match[0][0], match[0][1]
                
                # Execute the tool and update the response to be given back to the LLM to continue ReAct loop
                if tool != "None":
                    tool_res = eval(f'{tool}("{tool_input}")')
                    response = f"Observation: {tool_res}"
                else:
                    response = "Observation: I cannot answer using my available actions. so I will inform the user to explain more its query as I cannot answer it"

            # Extract the final answer (Answer:)from the response if the ReAct loop reached its end by the LLM
            elif "answer:" in response.lower():
                if tool == "to_msa":
                    tool = "to Modern Standard Arabic tool" + " 🕵️"
                elif tool == "irab":
                    tool = "irab tool" + " 📚"
                elif tool == "diacratize":
                    tool = "diacratize tool" + " 🇵🇸"
                elif tool == "holy_quran":
                    tool = "holy quran tool" + " 🕌"
                elif tool == "web_search":
                    tool = "web search tool" + " 🌐"
                elif tool == "llm_knowledge":
                    tool = "llm knowledge tool" + " 🤖"
                elif tool == "get_current_datetime":
                    tool = "get current datetime tool" + "🗓️"

                try:
                    if tool != "None":
                        print("Current Response:--------",response)
                        response = f"From {tool} >> " + re.findall("Answer: .*", response, re.DOTALL)[0]
                        response = re.sub(r'Answer:\s*', '', response)
                        response = re.sub(r'\s{2,}', ' ', response)

                    else:
                        response = re.findall("Answer: .*", response, re.DOTALL)[0]
                    
                except Exception as e:
                    try:
                        response = (
                            f"From {tool} --> "
                            + re.findall(r"Thought: (.+)", response, re.IGNORECASE)[0]
                            if tool != "None"
                            else re.findall(r"Thought: (.+)", response, re.IGNORECASE)[0]
                        )
                    except Exception as e:
                        print("---- while giving asnwer, we recieved this ---", e)
                        response = "Answer: Please ask me again as There is an Error displaying the results."
                return response

            # Send the response (given from above) to the LLM to continue its ReAct loop.
            response = self._execute(response)
            print(colored(response, "cyan")) if self.instance.verbose else None
        return response

    def __call__(self, Query):
        """
        exectures the ReAct loop when the class object like this `object(query)` is called instead of running `object.loop(query)`.
        """
        return self.loop(Query)