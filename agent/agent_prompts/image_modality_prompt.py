from langchain_core.prompts import ChatPromptTemplate # type: ignore

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
        Given an image, provide a JSON with the following keys:

        1. 'precise_description': A concise, detailed description of the image content.
        2. 'query_answer': The answer to a given query related to the image. Leave empty ('') if no query was given.
        3. 'needed_ocr': Boolean value True if the answer relies mainly on text in the image, otherwise False.
        4. 'language': The primary language in the image, one of ['English', 'Arabic', 'Other', '']. Use 'Other' for mixed or unknown languages, and '' if there’s no text.

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
