from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
            template="""You are a grader assessing whether an answer is useful to resolve a question.

            Here is the answer:
            \n ------- \n
            {answer} 
            \n ------- \n
            Here is the question: {query}

            Evaluate the answer based on these criteria:
            1. Completeness: Does the answer address all aspects of the question?
            2. Relevance: Is the information provided directly relevant to the query?
            3. Specificity: Does the answer provide specific details or examples?
            4. Clarity: Is the answer easy to understand and free from ambiguity?

            # Examples of good and bad answers:

            Good Answer Examples:
                1. Query: قم بتشكيل الجملة الآتية : ذهبت إلى البيت، فطرقت الباب بقوة، ولكن لم أجد أحدًا. عدت خائبًا، ولم أتمكن من تحقيق ما أردت
                Answer: ذهبتُ إلى البيتِ، فطرقتُ البابَ بقوةٍ، ولكن لم أجدْ أحدًا. عدتُ خائبًا، ولم أتمكنْ من تحقيقِ ما أردتُ.

                2. Query: أعرب الجملة الآتية كاملة: ضرب المعلم الطالب
                Answer: \nضرب: فعل ماضي مبني على الفتح\nالمعلم: فاعل مرفوع وعلامة رفعه الضمة الظاهرة على آخره\nالطالب: مفعول به منصوب وعلامة نصبه الفتحة الظاهرة على آخره 

            Bad Answer Examples
                1. Query: قم بتشكيل الجملة الآتية : ذهبت إلى البيت، فطرقت الباب بقوة، ولكن لم أجد أحدًا. عدت خائبًا، ولم أتمكن من تحقيق ما أردت
                Answer: أنا لا أعرف الإجابة برجاء تزويدي بمعلومات أخرى.

                2. Query: أعرب الجملة الآتية كاملة: ضرب المعلم الطالب
                Answer: \nالمعلم: فاعل مرفوع وعلامة رفعه الضمة الظاهرة على آخره\nالطالب: مفعول به منصوب وعلامة نصبه الفتحة الظاهرة على آخره 

            
            **Important Note:** Questions that primarily seek personal opinions, emotions, or subjective judgments (e.g., "كيف حالك", "من أنت","How do you do?" ) are considered good answers regardless of their content.

            Give a binary score 'yes' or 'no' to indicate whether the answer is useful to resolve a question.
            Provide the binary score as a JSON with a single key 'is_good_answer' and no preamble or explanation.""",
            input_variables=["answer", "query"],
        )