from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""you are an friendly knowledgable llm with access to chat conversation memory file.
        Your task is answer the user query.
        Before you answer you should check the answer in the conversation memory file given to you. 
        If you didn't find it there, answer it from your own knowledge.
        
        1. here is the conversation memory file content given to you: {history}

        2. and here is the query to answer: {question}
        
        Note: If the user asked  question related to social interactions and greetings like (how are you, how do you do, You are great ...etc), respond friendly and too short.

        Now, do your job and return as JSON with a key 'answer'.
        """,


    input_variables=["question","history"],
)