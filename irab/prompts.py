# Import prompt template
from langchain_core.prompts import PromptTemplate


# Build custom prompt
irab_prompt = PromptTemplate(
    template="""
    <s> [INST] أنت خبير في قواعد اللغة العربية وإعرابها. قم بتقديم تحليل نحوي مفصّل للجملة المقدمة باتباع الخطوات التالية:

1. شكّل الجملة أولاً.

2. حلل كل كلمة في الجملة بالترتيب، موضحًا:
   أ. الوظيفة النحوية (مثل: فاعل، مفعول به، مبتدأ، خبر، إلخ).
   ب. الإعراب الكامل (مرفوع، منصوب، مجرور، مجزوم) مع ذكر علامة الإعراب.

3. إذا احتوت الجملة على تعابير اصطلاحية أو تراكيب معقدة:
   - وضّح كيف تؤثر على التحليل النحوي.
   - حدد ما إذا كانت الكلمة أو العبارة تخضع لتراكيب خاصة أو تخرج عن القاعدة.
   - إذا كان هناك إضمار أو مجاز، وضّح كيفية الإعراب المناسب.

**احرص على:**
- إذا كان الفعل معتل الآخر، تأكد من أن الجزم يكون بحذف حرف العلة وليس بالسكون.
- الضمائر المتصلة بحروف الجر، مثل "الهاء" في "إليه" و "به"، يجب أن تُعرب في محل جر اسم مجرور ولا تُبنى على الضم.
- في حال وجود جار ومجرور مثل "بوضوح" الذي يعبر عن الكيفية، اعتبره "حرف جار واسم مجرور وشبه جملة في محل نصب حال".

### **أمثلة:**

**المثال 1:**
الجملة: "الطالبُ لم يسعَ إلى النجاحِ بنفسه."
- الطالبُ: مبتدأ مرفوع وعلامة رفعه الضمة الظاهرة.
- لم: حرف نفي وجزم.
- يسعَ: فعل مضارع مجزوم بحذف حرف العلة.
- إلى: حرف جر.
- النجاحِ: اسم مجرور وعلامة جره الكسرة.
- بنفسه: الباء حرف جر، نفس: اسم مجرور بالكسرة والهاء ضمير متصل في محل جر مضاف إليه.

شبه الجملة "بنفسه" فى محل نصب حال.

**المثال 2:**
الجملة: "شرحَ المعلمُ الدرسَ بوضوحٍ."
- شرحَ: فعل ماضٍ مبني على الفتح.
- المعلمُ: فاعل مرفوع وعلامة رفعه الضمة.
- الدرسَ: مفعول به منصوب وعلامة نصبه الفتحة.
- بوضوحٍ: الباء حرف جر، ووضوح اسم مجرور بالكسرة، وشبه الجملة في محل نصب حال.

الجملة الكاملة: {original_sentence}

الجملة المراد إعرابها هي:
{sentence}

قدم إجابتك بتنسيق واضح ومنظم، مع استخدام التشكيل لمساعدتك في الإعراب.
[/INST]
    """,
    input_variables=["sentence", "original_sentence"],
)


split_prompt = PromptTemplate(
    template="""<s>  [INST] You are an expert in Arabic syntax. Your task is to break down a long Arabic paragraph into  sentences :

paragraph: {sentence}

Split the paragraph into individual sentences **only if** it can be more than a sentence.
If the paragraph is already a single sentence, you can leave it as is.
examples: 

Provide your output in a clear list format, with each sentence on a new line.
Using this structure:
paragraph: "The Original paragraph here"

Stick to **output format** below:
`
Output:
- "The first split sentence here"
- "The second split sentence here" (optional) as the original paragraph might not require splitting.
- "The third split sentence here" (optional) and so on.
`
[/INST]""",
    input_variables=["sentence"],
)

critic_prompt = PromptTemplate(
    template="""
    <s> [INST] أنت ناقد خبير في قواعد النحو العربي. مهمتك هي مراجعة نتائج الإعراب المقدمة للجملة والتأكد من دقتها بناءً على القواعد النحوية المعروفة. قم بما يلي:

1. تحقق مما إذا تم تحديد نوع الجملة بشكل صحيح (اسمية أو فعلية أو شبه جملة).
2. تأكد من أن كل كلمة تم تحليلها بشكل صحيح وفقًا لوظيفتها النحوية (مثل فاعل، مفعول به، مبتدأ، خبر، بدل، نعت، اسم مجرور، ضمير، حرف، مضاف إليه إلخ).
3. تأكد من أن الإعراب الكامل لكل كلمة (مثل مرفوع، منصوب، مجرور) تم تحديده بشكل صحيح مع ذكر العلامات المناسبة. وتأكد أيضا من البناء.
4. راجع أي تعابير اصطلاحية أو تراكيب معقدة للتأكد من أنها تم التعامل معها بشكل صحيح.
5. قم بالتركيز على:
   - الأفعال المعتلة: تأكد من أن الجزم يكون بحذف حرف العلة وليس بالسكون.
   - الضمائر المتصلة: تأكد من أن الضمائر المتصلة بحروف الجر (مثل "به") تكون في محل جر اسم مجرور ولا تُبنى على الضم.
   - شبه الجملة (جار ومجرور): إذا كانت شبه الجملة تعبر عن كيفية الفعل، تحقق من أنها تمثل حالًا في محل نصب.

### **أمثلة:**

**المثال 1:**
الجملة: "الطالبُ لم يسعَ إلى النجاحِ بنفسه."
- الطالبُ: مبتدأ مرفوع وعلامة رفعه الضمة.
- لم: حرف نفي وجزم.
- يسعَ: فعل مضارع مجزوم بحذف حرف العلة.
- إلى: حرف جر.
- النجاحِ: اسم مجرور بالكسرة.
- بنفسه: الباء حرف جر ونفس اسم مجرور بالكسرة والهاء ضمير مبني في محل جر مضاف إليه.

شبه الجملة "بنفسه" فى محل نصب حال.

النقد: الإعراب صحيح ولا توجد أخطاء.

**المثال 2:**
الجملة: "شرح المعلم الدرس بوضوح."
الإعراب:
- شرحَ: فعل ماضٍ مبني على الفتح.
- المعلم: فاعل مرفوع بالضمة.
- الدرس: مفعول به منصوب.
- بوضوحٍ: الباء حرف جر، ووضوح اسم مجرور بالكسرة .
وشبه الجملة "بوضوح" فى محل نصب حال

النقد: صحيح

**المثال 3 (مع خطأ):**
الجملة: "الولد لم يسعى إلى الحديقة."
الإعراب:
-  الولدُ: مبتدأ مرفوع بالضمة.
- لم: حرف نفي وجزم.
- يسعى: فعل مضارع مجزوم بالسكون.
- إلى: حرف جر.
-  الحديقة: اسم مجرور بالكسرة.

النقد: الفعل "يسعى" فعل معتل الآخر، يجب أن يُجزم بحذف حرف العلة وليس بالسكون. التصحيح: "يسعَ" فعل مضارع مجزوم بحذف حرف العلة.


الجملة المراد مراجعتها:
{sentence}

الإعراب المقدم:
{irab_results}

قدم تعليقك النقدي على الإعراب أعلاه بناءً على القواعد النحوية. إذا وجدت أخطاء، قم بتحديدها وتصحيحها. إذا كان التحليل صحيحًا، قم بالتأكيد على صحته.
[/INST]
    """,
    input_variables=["sentence", "irab_results"],
)


json_parse_prompt = PromptTemplate(
    template="""
    أنت خبير في قواعد اللغة العربية (إعراب). سأقدم لك جملة عربية وقائمة بنتائج الإعراب المفصلة لكل كلمة. مهمتك هي:

    1. دمج نتائج الإعراب في فقرة متناسقة وفقًا لترتيب الكلمات الأصلي.
    2. تقديم النتائج في صيغة JSON بالتنسيق التالي:

    **الجملة الأصلية**: "{sentence}"

    **النتيجة قبل JSON**:
    {irab_results}

    **النتيجة النهائية**:
    ```json
    {{
        "original_sentence": "{sentence}",
        "diacratized_sentence": "{diacratized}",
        "irab_results": [
            {{"word": "{{word1}}", "irab": "{{irab1}}"}}{{
                # Add the rest of the irab results in the same format
            }},
            ...
        ],
        "special_sentences":[
            {{"sentence": "{{sentence1}}", "special_irab": "{{special_irab1}}"}}{{
                # Add any special sentences or phrases requiring additional explanations
            }},
            ...
        ]
    }}
    ```

    **مثال**:

    الجملة الأصلية: "الطالبُ لم يسعَ إلى النجاحِ بنفسه سريعًا."

    **النتيجة قبل JSON**:
    1. نوع الجملة: اسمية.
    2. تحليل الكلمات:
    - الطالبُ: مبتدأ مرفوع وعلامة رفعه الضمة الظاهرة.
    - لم: حرف نفي وجزم.
    - يسعَ: فعل مضارع مجزوم بحذف حرف العلة.
    - إلى: حرف جر.
    - النجاحِ: اسم مجرور وعلامة جره الكسرة.
    - بنفسه: الباء حرف جر، ونفس اسم مجرور والهاء ضمير مضاف إليه.
    - سريعًا: حال منصوب وعلامة نصبه الفتحة الظاهرة.
    3. الجملة الفعلية "لم يسعَ إلى النجاح بنفسه سريعًا" هي في محل رفع خبر للمبتدأ "الطالب".
    شبه الجملة "بنفسه" فى محل نصب حال.
    **النتيجة النهائية**:
    ```json
    {{
        "original_sentence": "الطالبُ لم يسعَ إلى النجاحِ بنفسه سريعًا.",
        "diacratized_sentence": "الطَّالِبُ لَمْ يَسْعَ إِلَى النَّجَاحِ بِنَفْسِهِ سَرِيعًا.",
        "irab_results": [
            {{"word": "الطالبُ", "irab": "مبتدأ مرفوع وعلامة رفعه الضمة الظاهرة"}},
            {{"word": "لم", "irab": "حرف نفي وجزم"}},
            {{"word": "يسعَ", "irab": "فعل مضارع مجزوم بحذف حرف العلة"}},
            {{"word": "إلى", "irab": "حرف جر"}},
            {{"word": "النجاحِ", "irab": "اسم مجرور وعلامة جره الكسرة الظاهرة"}},
            {{"word": "بنفسه", "irab": "الباء حرف جر ونفس اسم مجرور والهاء ضمير مضاف إليه"}},
            {{"word": "سريعًا", "irab": "حال منصوب وعلامة نصبه الفتحة الظاهرة"}}
        ],
        "special_sentences": [
            {{"sentence": "لم يسعَ إلى النجاحِ بنفسه سريعًا.", "special_irab": "الجملة الفعلية في محل رفع خبر للمبتدأ الطالب"}}
        ]
    }}
    ```

    - احرص على أن تكون الجملة الأصلية متناسقة مع نتائج الإعراب.

    الجملة الأصلية: {sentence}
    نتائج الإعراب:
    {irab_results}
    """,
    input_variables=["sentence", "irab_results"],
)


helper_prompt = PromptTemplate(
    template="""
استخرج الجمل العربية فقط
`{sentence}`

Only put the final sentences in a list format like this:     

example:
"ما زال الطالبُ مستمرًّا في الدراسةِ رغم الصعوباتِ."
out: ["ما زال الطالبُ مستمرًّا في الدراسةِ رغم الصعوباتِ."]

another example:
أحبُّ الكتابَ الذي قرأتُهُ في المكتبةِ. وأحب القراءةَ في الحديقةِ.
out: ["أحبُّ الكتابَ الذي قرأتُهُ في المكتبةِ.", "وأحب القراءةَ في الحديقةِ."]                  

stick to the format
-----------------------------
استخرج الجمل العربية فقط
`{sentence}`
"""
)

small_irab_prompt = PromptTemplate(
    template="""
    <s> [INST] أنت خبير في إعراب الجمل العربية. قم بتحليل الجملة التالية:

1. حدد نوع الجملة (اسمية أو فعلية).
2. قم بإعراب كل كلمة في الجملة مع التركيز على الإعرابات الصعبة مثل:
   - إعراب الأفعال المعتلة (مثل "يسعى").
   - إعراب الضمائر المتصلة (مثل "أعطاه" أو "به").
   - إعراب المفعول المطلق (مثل "شرحًا").
   - إعراب شبه الجملة (مثل "بوضوح").
   - إعراب الأسماء الخمسة (مثل "أبوك").
   - إعراب الجمل الشرطية وأدوات النصب والجزم (مثل "إن درست").

تأكد من الانتباه للأخطاء الشائعة مثل:
   - جزم الفعل المعتل بطريقة خاطئة (مثل "يسع" مجزوم بحذف حرف العلة وليس بالسكون).
   - إعراب الأفعال المنصوبة بشكل خاطئ (مثل "ينالَ" المنصوب بالفتحة وليس مرفوعًا).

الجملة: {sentence}
[/INST]
    """,
    input_variables=["sentence"],
)
small_critic_prompt = PromptTemplate(
    template="""
    <s> [INST] راجع التحليل النحوي للجملة التالية للتأكد من صحته:

الجملة: {sentence}
الإعراب المقدم:
{irab_results}

1. تحقق مما إذا كان التحليل النحوي صحيحًا، وكن دقيقًا في مراجعة الأخطاء الشائعة مثل:
   - جزم الأفعال المعتلة بطريقة خاطئة (مثل "يسع" يجب جزمه بحذف حرف العلة وليس بالسكون).
   - إعراب الأفعال المنصوبة بشكل خاطئ (مثل "ينالَ" يجب نصبه بالفتحة).
   - إعراب الضمائر المتصلة بحروف الجر (مثل "به" يجب أن يكون في محل جر وليس مبنيًا على الضم).
   - الخلط بين الحال والمفعول به.
   - إهمال إعراب الحروف مثل "لم" أو "إلى".

2. صحح أي أخطاء في الإعراب وقدم توضيحًا حول السبب.

[/INST]
    """,
    input_variables=["sentence", "irab_results"],
)
