from langchain_core.prompts import PromptTemplate

correct_prompt_paragraph = PromptTemplate(template="""
<s>
[INST]
حلل المعطى لك ثم قم بإعطاء إجابة نهائية بها نصين (النص المعطى والنص المصحح) بعد القيام بالخمس خطوات القادمة:
1- قم بفحص النص المعطى لك هل هو مطابق لقواعد الكتابة اللغة العربية الفصحى و هل به أخطاء فى قواعد الكتابة باللغة العربية الفصحى أو به كلمات لا تنتمى للغة العربية الفصحى أم لا (وأجب بنعم أو لا) ثم اذهب للخطوة الثانية
2- أعد النص كما هى فى إجابتك النهائية إذا كانت إجابتك فى الخطوة الأولى ب (نعم النص مكتوب صحيح وفقًا لقواعد اللغة العربية الفصحى) ثم اذهب للخطوة الرابعة
3- قم بإعادة كتابة النص ليكون مكتوب طبقًا لقواعد اللغة العربية الفصحى وأعد النص المصحح فى إجابتك النهائية إذا كانت إجابتك فى الخطوة الأولى ب (لا لا ليس مكتوب وفقًا لقواعد اللغة العربية الفصحى) ثم اذهب للخطوة الرابعة
4- قم بالإمعان فى فهم النص المصحح ثم قسمه إلى رئيسية وجمل فرعية ثم اضبط علامات الترقيم بين الجمل بناءً على فهمك ثم انتقل للخطوة الخامسة
5- لا تقم بإضافة تلخيص النص السابق إلى النص المصحح فى إجابتك النهائية إذا إعطى لك تلخيص النص السابق (هذا التلخيص فقط للفهم ولا ترجعه فى إجابتك النهائية للنص المصحح فى إجابتك النهائية) . ثم أعطى إجابتك النهائية
                                     
                                                                   
قم بدراسة هذه الأمثلة للمساعدة:
الجملة من اللهجة المصرية: "ايوا واضح ان الاتنين ستات مشغولين أوى فى مكالمتهم دى."
التصحيح:"نعم من الواضح أن المرأتين مشغولتان فى مكالمتهما التليفونية هذه."
الجملة من اللهجة الموريتانية: "لمرا واقفة ولا قاعدة؟."
التصحيح:"هل المرأة واقفة أم جالسة؟"
الجملة من اللهجة المغربية: "شحال ديال الناس كاينين فى الصورة, وشنو كايديرو؟."
التصحيح:"كم عدد الأشخاص الموجودين فى الصورة, وماذا يفعلون؟"
الجملة من اللهجة الفلسطينية: "شو نوع الورد اللى قادر تشوفه حولين المنتزة؟"
التصحيح:"ما نوع الزهور التى يمكن رؤيتها حول الحديقة؟"
الجملة من اللهجة السعودية: "أنا تعبان اليوم، أبي أرتاح شوي"
التصحيح:"أنا متعب اليوم، أريد أن أرتاح قليلاً."
الجملة من اللهجة السعودية: "تعال نشرب قهوة ونقعد نسولف شوي"
التصحيح:"تعال نشرب قهوة ونتحدث قليلاً"

(أعط نصين على أية حالة حتى إذا كان النصين متطابقين ) اجعل إجابتك النهائية تتضمن نصين النص المعطى لك من المستخدم والنص المصححة
هذا هو النص المعطى لك من المستخدم:                         
{sentence}

[/INST]
""",
input_variables=['sentence'])

correct_parser_prompt_paragraph = PromptTemplate(template="""
أنت سوف تعطى إجابة عن نص معاد صياغته ليكون باللغة العربية الفصحى
وقد يكون النص المصحح هى نفس النص الأصلي  
give your answer as JSON with keys as 'input_text' and 'primary_corrected_text'
هذه هى الإجابة المعطاة لك:
{asnwer}
""",
input_variables=['answer'])


critic_prompt_paragraph = PromptTemplate(template="""
<s> [INST]
قم بفحص النصين المعطيين لك (نص مدخل من المستخدم و نص مصحح ليكون باللغة العربية الفصحى) ثم قم بالأربع خطوات القادمة على  الترتيب:
1- تأكد من أن النص المصحح لا يخالف قواعد اللغة العربية الفصحى وليس به كلمات لا تنتمى للغة العربية الفصحى (مثل: مش عارف , أنا واخد بالى ,... وغيرها من الكلمات التى لا تنتمى للغة العربية الفصحى) وأعط إجابتك ب (تخالف أو لا تخالف) ثم اذهب للخطوة الثانية
2- أعد تصحيح النص المصحح إذا كانت إجابتك فى الخطوة السابقة ب (تخالف). وإذا كانت إجابتك  فى الخطوة السابقة ب (لا تخالف) انتقل للخطوة الثالثة
3- قم بتصحيح الأخطاء فى النحو أو الصرف أو الإملاء إذا وجدت أخطاء ثم انتقل للخطوة الرابعة
4- قم بإمعان أن النص المصحح النهائي قصير على قدر الإمكان وتجنب التكرار بدون فقدان معلومات أو فقدان العلاقة بالنص المدخل من المستخدم

(أعط ثلاث نصوص على أية حالة حتى إذا كان نصين من الثلاث متطابقين أو الثلاث نصوص متطابقين).أعط إجابتك النهائية كثلاث نصوص (النص المدخل من المستخدم و النص المصحح الأولي والنص بعد تنفيذ الثلاث خطوات) بعد القيام بالأربع خطوات
هذان هما النصان المعطايين لك (النص المدخل من المستخدم والنص المصصح الأولي):
{sentence}
[/INST]
""",
input_variables=['sentence'])

critic_parser_prompt_paragraph = PromptTemplate(template="""
أنت سوف تعطى إجابة بها ثلاث نصوص (نص مدخل من المستخدم ونص مصحح أولي ونص مصحح نهائي
قد يكون الثلاث نصوص متطابقين  
give your answer as JSON with keys as 'input_text' and 'primary_corrected_text' and 'finally_corrected_text' and 'finally_corrected_text_short_summary'
هذه هى الإجابة المعطاة لك:
{asnwer}
""",
input_variables=['answer'])