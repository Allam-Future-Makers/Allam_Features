from langchain_core.prompts import PromptTemplate

correct_prompt_text = PromptTemplate(template="""
<s>
[INST]
حلل المعطى لك ثم قم بإعطاء إجابة نهائية بها نصين (أولًا: النص المعطى لك بدون النص السابق(قد ينقسم النص المعطى لك إلى جزئين ... نص مصحح سابق و نص غير مصحح معطى لتصحيحه) , وثانيًا: النص المصحح) بعد القيام بالخمس خطوات القادمة:
1- قم بفهم معنى النص  المصحح السابق (سوف تجد هذا النص المصحح السابق من ضمن النص المعطى لك) لتجعل النص المصحح الحالى مطابق للمعنى العام ولا تقم بالتكرار من النص السابق إلى النص المصحح الحالى. فقط استخدم النص المصحح السابق فى فهم المعنى. ثم اذهب للخطوة الثانية
2- قم بفحص النص  الغير مصحح المعطى لك هل هو مطابق لقواعد الكتابة اللغة العربية الفصحى و هل به أخطاء فى قواعد الكتابة باللغة العربية الفصحى أو به كلمات لا تنتمى للغة العربية الفصحى أم لا (وأجب بنعم أو لا) ثم اذهب للخطوة الثالثة
3- أعد النص  الغير مصحح كما هو فى إجابتك النهائية إذا كانت إجابتك فى الخطوة الأولى ب (نعم النص مكتوب صحيح وفقًا لقواعد اللغة العربية الفصحى) ثم اذهب للخطوة الرابعة
4- قم بإعادة كتابة النص الغير مصحح المعطى لك ليكون مكتوب طبقًا لقواعد اللغة العربية الفصحى وأعد النص المصحح فى إجابتك النهائية إذا كانت إجابتك فى الخطوة الأولى ب (لا لا ليس مكتوب وفقًا لقواعد اللغة العربية الفصحى) ثم اذهب للخطوة الخامسة
5- قم بالإمعان فى فهم النص المصحح ثم قسمه إلى جمل رئيسية وجمل فرعية ثم اضبط علامات الترقيم بين الجمل بناءً على فهمك ثم أعطى إجابتك النهائية

تأكد من عدم وجود تكرار فى الكلمات تخل بالمعنى بين النص  المصحح السابق المصحح المعطى لك و النص المصحح النهائى   
                                                                                                                                          
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

(أعط نصين على أية حالة حتى إذا كان النصين متطابقين ) اجعل إجابتك النهائية تتضمن نصين. الأول: النص المعطى لك  من المستخدم (بدون النص المصحح السابق) و الثانى: النص المصححة
هذا هو النص المصحح السابق المعطى لك من المستخدم:                         
{past_sentence}
وهذا هو النص الغير مصصح المعطى لك من المستخدم:
{sentence}

الآن قم بالخطوات المطلوبة
[/INST]
""",
input_variables=['sentence'])

correct_parser_prompt_text = PromptTemplate(template="""
أنت سوف تعطى إجابة بها نصين (نص مدخل من المستخدم ونص مصحح
قد يكون النصين متطابقين  
النص المدخل = input_text
النص المصحح = corrected_text
                        
give your final answer as JSON with keys as 'input_text' and 'corrected_text' with this structre:
'input_text': 'valid string content of the input_text (النص المدخل) given to you after making it organized for display but not changed in content',
'corrected_text': 'valid string content of the corrected_text (النص المصحح) given to you after making it organized for display but not changed in content'

هذه هى الإجابة المعطاة لك:
{answer}
                                           
make sure to return the final answer as a valid JSON with keys [input_text,corrected_text]
                                           
So Important: If the values (values only not the keys) of the JSON  contains the symbol `"` replace it with `“`.
""",
input_variables=['answer'])


critic_prompt_text = PromptTemplate(template="""
<s> [INST]
قم بفحص النصين المعطيين لك (نص مدخل من المستخدم و نص مصحح ليكون باللغة العربية الفصحى) ثم قم بالأربع خطوات القادمة على  الترتيب:
1- تأكد من أن النص المصحح لا يخالف قواعد اللغة العربية الفصحى وليس به كلمات لا تنتمى للغة العربية الفصحى (مثل: مش عارف , أنا واخد بالى ,... وغيرها من الكلمات التى لا تنتمى للغة العربية الفصحى) وأعط إجابتك ب (تخالف أو لا تخالف) ثم اذهب للخطوة الثانية
2- أعد تصحيح النص المصحح إذا كانت إجابتك فى الخطوة السابقة ب (تخالف). وإذا كانت إجابتك  فى الخطوة السابقة ب (لا تخالف) انتقل للخطوة الثالثة
3- قم بتصحيح الأخطاء فى النحو أو الصرف أو الإملاء إذا وجدت أخطاء ثم انتقل للخطوة الرابعة
4- قم بجعل النص متناسق من حيث البعد الزمانى والمكانى والمعنوى حتى يسهل قراءته. ثم انتقل للخطوة الخامسة
5- قم بإمعان بجعل النص المصحح النهائي قصير على قدر الإمكان وتجنب التكرار بدون فقدان معلومات أو فقدان العلاقة بالنص المدخل من المستخدم

(أعط ثلاث نصوص على أية حالة حتى إذا كان نصين من الثلاث متطابقين أو الثلاث نصوص متطابقين).أعط إجابتك النهائية كثلاث نصوص (النص المدخل من المستخدم و النص المصحح الأولي والنص بعد تنفيذ الثلاث خطوات) بعد القيام بالأربع خطوات
هذان هما النصان المعطايين لك (النص المدخل من المستخدم والنص المصصح الأولي):
{sentence}
                                    
الآن قم بالخطوات المطلوبة
[/INST]
""",
input_variables=['sentence'])

critic_parser_prompt_text = PromptTemplate(template="""
أنت سوف تعطى إجابة بها ثلاث نصوص (نص مدخل من المستخدم ونص مصحح أولي ونص مصحح نهائي
قد يكون الثلاث نصوص متطابقين  
النص المدخل = input_text
النص المصحح الأولى = primary_corrected_text
النص المصحح النهائى = finally_corrected_text
                                           
give your final answer as JSON with keys as 'input_text' and 'primary_corrected_text' and 'finally_corrected_text' with this structre:
'input_text': 'valid string content of the input_text (النص المدخل) given to you after making it organized for display but not changed in content',
'primary_corrected_text': 'valid string content of the primary_corrected_text (النص المصحح الأولى) given to you after making it organized for display but not changed in content', 
'finally_corrected_text': 'valid string content of the finally_corrected_text (النص المصحح النهائى) given to you after making it organized for display but not changed in content'

هذه هى الإجابة المعطاة لك:
{answer}
                                           
make sure to return the final answer as a valid JSON with keys [input_text, primary_corrected_text, finally_corrected_text]
                                           
So Important: If the values (values only not the keys) of the JSON  contains the symbol `"` replace it with `“`.
""",
input_variables=['answer'])




new_correct_prompt_text = PromptTemplate(template="""
<s>
[INST]
قم بدورك الأساسى وهو تصحيح النص المعطى لك لتجعله مطابق لقواعد اللغة العربية الفصحى ال MSA من حيث:
اجعل إجابتك النهائية تتضمن نصين اثنين على أية حال (النص المعطى لك فى الأساس و النص بعد التصحيح من غير تأويل وإذا كان النص المعطى صحيح لا تصححه) حتى إذا كان النصان متطابقين أو كان النص المعطى قصير. 

1- استبدال الكلمات التى لا تنتمى للغة العربية الفصحى (مثل: النهاردة, نسولف, هاى, مش عاوز, بتوع, بتاعك .... الخ) بأقصر كلمة ممكنة معبرة
2- تصحيح النص من حيث الأخطاء الإملائية أو النحوية أو الأخطاء فى الصرف.

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
الجملة : "أريد الذهاب للمنزل"
التصحيح: "أريد الذهاب للمنزل"
                             
هذا هو النص المعطى لك من المستخدم:
{sentence}

[/INST]
""", input_variables=['sentence'])

new_correct_parser_prompt_text = PromptTemplate(template="""
أنت سوف تعطى إجابة بها نصين (نص مدخل من المستخدم ونص مصحح
قد يكون النصين متطابقين  
النص المعطى = input_text
النص المصحح = corrected_text
                        
give your final answer as JSON with keys as 'input_text' and 'corrected_text' with this structre:
'input_text': 'valid string content of the input_text (النص المعطى) given to you after making it organized for display but not changed in content',
'corrected_text': 'valid string content of the corrected_text (النص المصحح) given to you after making it organized for display but not changed in content'

هذه هى الإجابة المعطاة لك:
{answer}
                                           
make sure to return the final answer as a valid JSON with keys [input_text,corrected_text]
                                           
So Important: If the values (values only not the keys) of the JSON  contains the symbol `"` replace it with `“`.
""",
input_variables=['answer'])



whole_paragraph_organizer_prompt = PromptTemplate(template="""
You will be given chunks of Arabic texts. Each chunk has a corrected_text of this chunk (النص المصحح).
Your job is to combine all the corrected_text of all the chunks in one paragraph and return this paragraph.
Try to organize the paragraph for being displayed.
                                                 
here is the text given to you:                    
{text}                             
                                                 
return you answer as JSON with the key 'combined_corrected_text'.
So Important: If the values (values only not the keys) of the JSON  contains the symbol `"` replace it with `“`.

""", input_variables=['text'])