from langchain_core.prompts import PromptTemplate

ayah_prompt_allam = PromptTemplate(template="""
<s>
[INST]
رد على السؤال المعطى لك من خلال النص المعطى الذى يحتوى على:
آية من القرآن الكريم وإعرابها وتفسيرها ورابط يحتوى على مقطع صوتى  يحتوى على القراءة الصحيحة لها. 
                                                                                            
صيغة الإخراج المطلوبة :
```json
{{
"answer": "[الرد الدقيق  المختصر الكافى على السؤال بدون أخطاء فى النص القرآنى]"
}}```
,

قم بدورك الآن. هذا هو السؤال المعطى لك:
{query}

وهذا هو النص المعطى لك:
{context}     

ملحوظة مهمة:
1. إذا كان الرد على السؤال به `'` أو  `"` استبدلهما ب `❝`
2. استخدم نص الآية الصحيح من النص المعطى لك فى الإجابة لضمان عدم وجود أخطاء فى النص القرآنى
3. إذا كان سؤال الشخص عن القراءة الصحيحة أو التلاوة الصحيحة أعطه :
- النص الصحيح للآية 
- رابط المقطع الصوتى الخاص بتلاوة وقراءة الآية 
                                   
صيغة الإخراج المطلوبة :
```json
{{
"answer": "[الرد الدقيق  المختصر الكافى على السؤال بدون أخطاء فى النص القرآنى]"
}}```                              
[/INST]
""")

ayah_prompt_gemini = PromptTemplate(template="""

                                    
أجب على السؤال المعطى لك من خلال فهم النص المعطى لك.
النص المعطى يحتوى على آية من القرآن الكريم وإعرابها وتفسيرها ورابط يحتوى على القراءة الصحيحة لها. هذا الرابط المعطى مع الآية رابط لمقطع صوتى به تلاوة وقراءة صحيحة للآية                                   

هام جدا:
إذا كان سؤال الشخص عن القراءة الصحيحة أو التلاوة الصحيحة أعطه :
1. نص الآية 
2. رابط المقطع الصوتى الخاص بتلاوة وقراءة الآية                                    
                                                                                                                                                                  
صيغة الإخراج المطلوبة :
```json
{{
"answer": "[الرد الدقيق والكافى على السؤال]"
}}```
,

ملحوظة مهمة:
إذا كان معنى الكلمة به `'` أو  `"` استبدلهما ب `❝`
                        
قم بدورك الآن. هذا هو السؤال المعطى لك:
{query}

وهذا هو النص المعطى لك:
{context}     

""")
