from langchain_core.prompts import PromptTemplate

correct_prompt = PromptTemplate(template="""
<s>
[INST]
قم بإعطاء إجابة نهائية بها جملتين (جملة مدخلة من المستخدم وجملة مصححة) بعد القيام بالثلاث خطوات القادمة:
1- قم بفحص الجملة المعطاة لك هل هى مطابقة لقواعد الكتابة اللغة العربية الفصحى و هل بها أخطاء فى قواعد الكتابة باللغة العربية الفصحى أو بها كلمات لا تنتمى للغة العربية الفصحى أم لا (وأجب بنعم أو لا).
2- أعد الجملة كما هى فى إجابتك النهائية إذا كانت إجابتك فى الخطوة الأولى ب (نعم الجملة تنتمى لقواعد اللغة العربية الفصحى).
3- قم بإعادة كتابة الجملة لتكون مكتوبة بقواعد اللغة العربية الفصحى وأعد الجملة المصححة فى إجابتك النهائية إذا كانت إجابتك فى الخطوة الأولى ب (لا لا تنتمى لقواعد اللغة العربية الفصحى).

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

(أعط جملتين على أية حالة حتى إذا كانت الجملتين متطابقتين ) اجعل إجابتك النهائية تتضمن جملتين الجملة المدخلة من المستخدم والجملة المصححة

هذه هى الجملة المدخلة من المستخدم:                         
{sentence}

[/INST]
""",
input_variables=['sentence'])

correct_parser_prompt = PromptTemplate(template="""
أنت سوف تعطى إجابة عن جملة معاد صياغتها لتكون باللغة العربية الفصحى
وقد تكون الجملة المصححة هى نفس الجملة الأصلية  
give your answer as JSON with keys as 'input_sentence' and 'primary_corrected_sentence'
هذه هى الإجابة المعطاة لك:
{asnwer}
""",
input_variables=['answer'])


critic_prompt = PromptTemplate(template="""
<s> [INST]
قم بفحص الجملتين المعطاتين لك (جملة مدخلة من المستخدم و جملة مصححة لتكون باللغة العربية الفصحى (input_sentence and primary_corrected_sentence) ) ثم قم بالأربع خطوات القادمة على  الترتيب:
1- تأكد من أن الجملة المصححة لا تخالف قواعد اللغة العربية الفصحى وليس بها كلمات لا تنتمى للغة العربية الفصحى (مثل: مش عارف , أنا واخد بالى ,... وغيرها من الكلمات التى لا تنتمى للغة العربية الفصحى) وأعط إجابتك ب (تخالف أو لا تخالف)
2- أعد تصحيح الجملة المصححة إذا كانت إجابتك فى الخطوة السابقة ب (تخالف). وإذا كانت إجابتك  فى الخطوة السابقة ب (لا تخالف) انتقل للخطوة الثالثة
3- قم بتصحيح الأخطاء فى النحو أو الصرف أو الإملاء إذا وجدت أخطاء ثم انتقل للخطوة الرابعة
4- تأكد بإمعان أن الجملة المصححة النهائية قصيرة على قدر الإمكان بدون فقدان معلومات أو فقدان العلاقة بالجملة المدخلة
      
(أعط ثلاث جمل على أية حالة حتى إذا كانت جملتين من الثلاث متطابقتين أو الثلاث جمل متطابقة).أعط إجابتك النهائية كثلاث جمل (الجملة المدخلة من المستخدم و الجملة المصححة الأولية والجملة بعد تنفيذ الثلاث خطوات) بعد القيام بالثلاث خطوات
هذان هما الجملتان المعطاتان لك (الجملة المدخلة من المستخدم والجملة المصصحة الأولية):
{sentence}
[/INST]
""",
input_variables=['sentence'])

critic_parser_prompt = PromptTemplate(template="""
أنت سوف تعطى إجابة بها ثلاث جمل (جملة مدخلة من المستخدم وجملة مصححة أولية وجملة مصححة نهائية
قد يكون الثلاث جمل متطابقة  
give your answer as JSON with keys as 'input_sentence' and 'primary_corrected_sentence' and 'finally_corrected_sentence'
هذه هى الإجابة المعطاة لك:
{asnwer}
""",
input_variables=['answer'])