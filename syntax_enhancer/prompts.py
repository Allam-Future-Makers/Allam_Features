from langchain_core.prompts import PromptTemplate

syntax_enhance_allam_prompt = PromptTemplate(template="""
<s>[INST]
                                  
اقترح مرادفات لبعض الكلمات في الجملة العربية التالية إذا كانت تُحسن المعنى وتجعله أكثر دقة وسلاسة. وأرجع التعديلات حسب صيغة الإخراج المعطاة لك
التعديلات قد تكون:
- اقتراح بدائل لكلمة أو بدائل لمجموعة من الكلمات
- حذف بعض الكلمات
تأكد من توافق الكلمات المقترحة مع السياق اللغوي والثقافي العربي،
على الاتفاق الجنسي واللغوي مع الكلمات المجاورة.
تأكد من تجانس جميع التعديلات إذا تم تركيبهم معا فى نص واحد
إذا لم تكن هناك حاجة للتعديل ، أرجع الخرج حسب صيغة الخرج المعطاة لك فى حالة عدم وجود تعديلات".
إذا كان النص قرآن أو حديث نبوى ممنوع منعًا باتًا التعديل فيه

صيغة الإخراج المطلوبة إذا كان هناك تعديل:
```json
{{
    "original_sentence": "[الجملة]",
    "modifications": {{
        "[الكلمة الأصلية]": "[الكلمة البديلة]",
        ...
    }}
}}```
أو
صيغة الإخراج المطلوبة إذا لم يكن هناك تعديل:
```json
{{
    "original_sentence": "[الجملة]",
    "modifications": {{}}
}}```                             

أمثلة:

```json{{                                  
"original_sentence": "ذهب أحمد إلى المكتبة ليشتري كتاب، وبعد ذلك ذهب إلى منزله وبدأ بقراءة الكتاب الذي اشتراه من المكتبة.",
"modifications": {{
    "وبدأ بقراءة الكتاب الذي اشتراه من المكتبة": "وبدأ بقراءة الكتاب",
    }}
}}```
,
```json{{                                  
"original_sentence": "الطبيب قام بتقديم العلاج المناسب للمريض الذي كان بحاجة إلى الدواء الفعال",
"modifications": {{
    "قام بتقديم" : "وصف",
    }}
}}```
,
```json{{                                  
"original_sentence": "المدرسة مكان مهم لتعليم الطلاب.",
"modifications": {{}}
}}```
,
```json{{                                  
"original_sentence": "التقرير النهائي الذي تم تقديمه من قبل المدير كان يحتوي على توصيات لتحسين الأداء.",
"modifications": {{
    "الذي تم تقديمه" : "",
    }}
}}```
,
```json{{                                  
"original_sentence": "الطالب قام بإظهار اهتمامه الكبير في الدراسة.",
"modifications": {{
    "قام بإظهار" : "أبدى",
    }}
}}```
,
```json{{                                  
"original_sentence": "قام المدير بإعطاء الموظفين النصائح الضرورية لكي يقوموا بإكمال العمل بطريقة سريعة ومناسبة.",
"modifications": {{
    "قام المدير بإعطاء الموظفين" : "قدّم المدير للموظفين",
    "لكى يقوموا بإكمال" : "ليكملوا"
    }}
}}```

الآن قم بدورك على هذا النص:
{sentence}
[/INST]                                  
""")


syntax_enhance_gemini_prompt = PromptTemplate(template="""
                                  
اقترح مرادفات لبعض الكلمات في الجملة العربية التالية إذا كانت تُحسن المعنى وتجعله أكثر دقة وسلاسة. وأرجع التعديلات حسب صيغة الإخراج المعطاة لك
التعديلات قد تكون:
- اقتراح بدائل لكلمة أو بدائل لمجموعة من الكلمات
- حذف بعض الكلمات
تأكد من توافق الكلمات المقترحة مع السياق اللغوي والثقافي العربي،
على الاتفاق الجنسي واللغوي مع الكلمات المجاورة.
تأكد من تجانس جميع التعديلات إذا تم تركيبهم معا فى نص واحد
إذا لم تكن هناك حاجة للتعديل ، أرجع الخرج حسب صيغة الخرج المعطاة لك فى حالة عدم وجود تعديلات".
إذا كان النص قرآن أو حديث نبوى ممنوع منعًا باتًا التعديل فيه

صيغة الإخراج المطلوبة إذا كان هناك تعديل:
```json
{{
    "original_sentence": "[الجملة]",
    "modifications": {{
        "[الكلمة الأصلية]": "[الكلمة البديلة]",
        ...
    }}
}}```
أو
صيغة الإخراج المطلوبة إذا لم يكن هناك تعديل:
```json
{{
    "original_sentence": "[الجملة]",
    "modifications": {{}}
}}```                             

أمثلة:

```json{{                                  
"original_sentence": "ذهب أحمد إلى المكتبة ليشتري كتاب، وبعد ذلك ذهب إلى منزله وبدأ بقراءة الكتاب الذي اشتراه من المكتبة.",
"modifications": {{
    "وبدأ بقراءة الكتاب الذي اشتراه من المكتبة": "وبدأ بقراءة الكتاب",
    }}
}}```
,
```json{{                                  
"original_sentence": "الطبيب قام بتقديم العلاج المناسب للمريض الذي كان بحاجة إلى الدواء الفعال",
"modifications": {{
    "قام بتقديم" : "وصف",
    }}
}}```
,
```json{{                                  
"original_sentence": "المدرسة مكان مهم لتعليم الطلاب.",
"modifications": {{}}
}}```
,
```json{{                                  
"original_sentence": "التقرير النهائي الذي تم تقديمه من قبل المدير كان يحتوي على توصيات لتحسين الأداء.",
"modifications": {{
    "الذي تم تقديمه" : "",
    }}
}}```
,
```json{{                                  
"original_sentence": "الطالب قام بإظهار اهتمامه الكبير في الدراسة.",
"modifications": {{
    "قام بإظهار" : "أبدى",
    }}
}}```
,
```json{{                                  
"original_sentence": "قام المدير بإعطاء الموظفين النصائح الضرورية لكي يقوموا بإكمال العمل بطريقة سريعة ومناسبة.",
"modifications": {{
    "قام المدير بإعطاء الموظفين" : "قدّم المدير للموظفين",
    "لكى يقوموا بإكمال" : "ليكملوا"
    }}
}}```

الآن قم بدورك على هذا النص:
{sentence}
""")