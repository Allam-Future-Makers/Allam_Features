from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(template ="""Given the latest user question and answer interaction and the current memory file content, update the memory file as follows:

1. user_personal_info: Identify and update any new personal information inferred from the user interaction. Include data like name, age, profession, preferences, etc.
2. user_areas_of_interest: Identify patterns or specific areas of interest based on repeated or recent topics in the user’s questions. Use concise keywords to describe areas. Pay attention, some words may be mentioned but it is not of main interest. 
3. short_term_memory: Log the recent question and answer and any inferred short-term knowledge. This section should help the chatbot recall recent topics and should reset or refresh after a specific number of interactions (e.g., keep the last 5–10).
4. long_term_memory: Look for recurring or significant insights that may indicate the user’s deeper interests, values, or habits. Update this section with patterns that persist over time or reveal the user’s underlying motivations. This could include:
    - Frequent topics or preferences that appear across several sessions.
    - Stated goals or intentions that may guide future interactions.
    - Personal details or contexts that seem to be lasting (e.g., interests in specific fields, common themes, or repeated requests for certain knowledge).

Based on the given interaction, update the memory file in the following structure, adding new information to each section as necessary. If no new updates are needed for a specific section, leave it as it is.

"user_personal_info": [List any new or updated personal info], 
"user_areas_of_interest": [List new or relevant topics based on recurring interest], 
"short_term_memory": [list of lists (not list of json) of most recent question and answer, limited to recent 5–10 interactions. example: [[question, answer],[question,answer], ...], 
"long_term_memory": [Analyze the query-answer interactions in the short-term memory then record any deep or recurring insights about the user’s interests, values, or goals. Always check if any updates available for this section.] 

here is the past query and answer interaction:
{query_answer}

and here is the current memory file content:
{memory_content}

now do your job and return a JSON with the following keys ['user_personal_info','user_areas_of_interest','short_term_memory','long_term_memory'] contains the past information added to them the updates.
If you see that certain key has no current update, return value for its key as empty string.
replace any single quotation with double quotation.
""", input_variables=["query_answer","memory_file"])