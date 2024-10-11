from langchain_core.prompts import PromptTemplate

summarization_prompt = PromptTemplate(
    template="""
        You are a part of multi-agent system. Your rule is summarize the conversation given to you and output three things:
        1. the summary of the conversation
        2. the last asked question-answer pair if exist.
        3. the long-term knowledge about the person in the conversation.

        Your summary is in arabic.
            
        this is the conversation text given to you: {text}
        """, 
    input_variables=['text'])