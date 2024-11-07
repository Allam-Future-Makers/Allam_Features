import sys, os

# Add the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_utils.check_hallucination import HallucinationChain
from agent_utils.grade_answer import GradeAnswerChain
from agent_utils.ReAct_loop import ReActLoop

from agent_utils.memory_update import MemoryUpdateChain

from termcolor import colored

import warnings

warnings.filterwarnings("ignore", message="The function `loads` is in beta")


class MainAgent:
    """
    ReActAgent class encapsulates the ReAct loop, hallucination checking, and answer grading functionalities.

    Args:
        verbose (bool, optional): Whether to print verbose output. Defaults to True.
        grad_answer (bool, optional): Whether to grade and improve the final answer. Defaults to True.
    """

    def __init__(self, instance):
        self.instance = instance

        self.ReAct_loop_object = ReActLoop(self.instance)

        self.check_hallucination_object = HallucinationChain(self.instance)
        
        self.grad_answer_object = GradeAnswerChain(self.instance)
        
        self.update_memory_object = MemoryUpdateChain(self.instance)

        self.messages = []

    def _execute(self, Query):
        """
        Processes a query using the ReAct loop.

        Args:
            Query (str): The input query.

        Returns:
            str: The generated response.
        """
        result = self.ReAct_loop_object(Query)
        query_answer = f"Query: {Query}\nAnswer: {result}\n"
        self.update_memory_object.update_memory(query_answer)  # adds the current query and response to the summary.txt file
        
        self.messages = self.ReAct_loop_object.messages
        return result

    def correct_hallucination(self, query, answer, ReAct_messages):
        """
        Checks for hallucinations in the generated answer and corrects them if necessary.

        Args:
            query (str): The original query.
            answer (str): The generated answer.
            ReAct_messages (list): The messages formed during the ReAct loop.

        Returns:
            str: The corrected answer.
        """
        is_hallucinating = self.check_hallucination_object(query, answer, ReAct_messages)
        print(
            colored("Is there hallucination? ", "cyan"),
            colored(is_hallucinating, "cyan"),
        ) if self.instance.verbose else None

        while True:
            if is_hallucinating.lower() == "yes":
                print(
                    colored("we are correcting hallucination...", "cyan"), flush=True
                ) if self.instance.verbose else None
                answer = self._execute(query + ". Please be aware of hallucinating")
                ReAct_messages = self.messages
                is_hallucinating = self.check_hallucination_object(query, answer, ReAct_messages)
            else:
                return answer

    def correct_final_answer(self, query, answer, ReAct_messages):
        """
        Grades the final answer and improves it if necessary.

        Args:
            query (str): The original query.
            answer (str): The generated answer.
            ReAct_messages (list): The messages formed during the ReAct loop.

        Returns:
            str: The improved answer.
        """
        is_good_answer = self.grad_answer_object(query=query, answer=answer)
        while self.counter < 2: 
            if is_good_answer.lower() == "no":
                print(colored("we are optimizing your answer...", "red"), flush=True) if self.instance.verbose else None
                answer = self._execute(
                    "rewrite the following query to give a better answer. " + query
                )
                answer = self.correct_hallucination(query, answer, ReAct_messages)
                is_good_answer = self.grad_answer_object(query=query, answer=answer)
                self.counter += 1
            else:
                self.counter += 1
                return answer
            self.counter += 1
        return answer

    def answer_query(self, query):
        """
        Starts the interactive query-response loop.

        Args:
            grad_answer (bool, optional): Whether to grade and improve the final answer. Defaults to general_grading_option.
        """
        self.counter = 0 
        answer = self._execute(query)
        ReAct_messages = self.messages
        answer = self.correct_hallucination(query, answer, ReAct_messages)
        if self.instance.grade_answer:
            answer = self.correct_final_answer(query, answer, ReAct_messages)

        print(colored(answer, "magenta"), flush=True)
        return answer
    
    def __call__(self, query):
        return self.answer_query(query)