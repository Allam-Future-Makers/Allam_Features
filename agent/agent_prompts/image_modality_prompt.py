from langchain_core.prompts import ChatPromptTemplate # type: ignore

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
        Given an image, provide a JSON with the following keys:

        1. 'precise_description': A concise, detailed description of the image content (وصف دقيق ومركز لمحتوى الصورة).
        2. 'query_answer': The answer to a given query related to the image.(إجابة السؤال المعطى الخاص بالصورة) Leave empty ('') if no query was given. (اتركه فارغا إذا لم يعطى سؤال)
        3. 'needed_ocr': Boolean value True if the answer relies mainly on text in the image, otherwise False. 
        4. 'language': The primary language in the image, one of ['English', 'Arabic', 'Other', '']. Use 'Other' for mixed or unknown languages, and '' if there’s no text. (النص الأساسى المهيمن على الصورة إذا كان بها نص. ويترك فارغا إذا لم يكن نص موجود فى الصورة أو أن النص المهيمن على الصورة ليس باللغة العربية أو الإنجليزية أو الخليط بينهما)

        The answer laguage is primarily the language of the query given (if no query given, the answer is primarily in English.) 

        Return your response as valid JSON with only these four keys: ['precise_description', 'query_answer', 'needed_ocr', 'language'].
        """),
        (
            "user",
            [
                {
                    "type": "text",
                    "text": "{query}",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64,{image_data}"},
                }
            ],
        ),
    ]
)