import os

class ReActTemp:
    def __init__(self, instance):
        self.instance = instance


    def update_system_template(self):
        parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_file_path = os.path.join(parent_directory, "agent_memory", f"memory_for_user_{self.instance.id}.txt")
        with open(data_file_path,"r") as f:
            self.memory_file_content = f.read()

        self.actions_description = """ 
            1. action_name: 'to_msa'
            action_description: to convert text given to it with any dialect to MSA (Modern Standard Arabic = اللغة العربية الفصحى).
            action_usage: to_msa(text:str)
            example_usage: to_msa("الدنيا ماعدش فيها أمان") -> "الحياة لم تعد آمنة"
            example_usage: to_msa("Holy Quran is Holy book of Muslims.") -> "القرآن الكريم هو الكتاب المقدس للمسلمين"

            2. action_name: 'diacratize'
            action_description:
            هذه أداة تقوم بتشكيل النص المعطى لها.
            من الضرورى أن يكون النص المعطى لها مكتوب باللغة العربية الفصحى
            قبل استخدام هذه الأداة تأكد من أن النص باللغة العربية الفصحى وإلا فاستخدم أداة to_msa ثم قم باستخدام أداة diacratize
            (التشكيل باللغة الإنجليزية يعنى diacratization)
            action_usage: diacratize(text:str)
            example_usage: diacratize("ذهبت إلى الجامعة صباحا") -> "ذَهَبْتُ إِلَى الجَامِعَةِ صَبَاحًا"

            3. action_name: 'irab'
            action_description:
            هذه أداة تقوم بإعراب النص المعطى لها (إذا كان النص لا ينتمى لآيات القرآن الكريم).
            من الضرورى أن يكون النص المعطى لها مطابق لقواعد اللغة العربية الفصحى
            قبل استخدام هذه الأداة تأكد من أن النص باللغة العربية الفصحى وإلا فاستخدم أداة to_msa ثم قم باستخدام أداة irab            
            action_usage: irab(text:str)
            example_usage: irab("ذهب أحمد إلى البيت") -> "ذهب: فعل ماضي مبني على الفتح\nأحمد: فاعل مرفوع وعلامة رفعه الضمة الظاهرة على آخره\nإلى: حرف جر\nالبيت: اسم مجرور وعلامة جره الكسرة الظاهرة على آخره "

            
            4. action_name: 'holy_quran'
            action_description:
            هذه أداة تقوم بإجابة أسألة محددة متعلقة بآيات القرآن الكريم مثل:
            إعطاء معنى أو تفسير  آية معينة من القرآن الكريم  - 
            إعطاء إعراب آية معينة - 
            - إعطاء القراءة الصحيحة أو التلاوة الصحيحة لآية معينة من القرآن الكريم
            ملحوظة هامة: إذا طلب المستخدم إعطاء القراءة الصحيحة أو المقطع الصوتى أو التلاوة الصحيحة لآية معينة أجب برابط وليس مقطع صوتى.
            ملحوظة هامة: لتستخدم هذه الآية يجب أن تتأكد أن النص المطلوب الإجابة عنه يحتوى على آية قرآنية.
            action_usage: holy_quran(text:str)
            example_usage: holy_quran("تفسير وقال ربكم ادعونى أستجب لكم") -> "وَقَالَ رَبُّكُمُ ادْعُونِي أَسْتَجِبْ لَكُمْ" هي آيةٌ كريمةٌ تُؤكد على رحمة الله تعالى، وعلى استجابته لدعوات عباده. وهي دعوةٌ للجميع للاقتراب من الله تعالى بالدعاء، ولطلب مساعدته في جميع أمور حياتهم"
            example_usage: holy_quran("القراءة الصحيحة لإن مع العسر يسرا") -> "القراءة الصحيحة لآية "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا" هي:\n1. نص الآية: "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا"\n2. رابط المقطع الصوتى الخاص بتلاوة وقراءة الآية: https://www.everyayah.com/data/Yasser_Ad-Dussary_128kbps/094005.mp3"

            5. action_name: 'web_search'
            action_description: it is an action to answer questions that need to search the web to find the answer (question that the LLM hasn't knowledge about it and it isn't related to any of the LLM available actions).
            action_usage: web_search(text:str)
            example_usage: web_search("أين ولد العز بن عبد السلام") -> "ولد العز بن عبد السلام فى دمشق فى سوريا"
            example_usage: web_search("Who is the messenger to whom the Holy Quran was revealed?") -> "The Holy Quran was revealed to Prophet Mohammad by Allah (swt)"


            6. action_name: 'llm_knowledge'
            action_description: it is an action to answer general question that don't require usage of any in the above actions.
            action_usage: llm_knowledge(text:str)
            example_usage: llm_knowledge("كيف حالك") -> "بخير والحمد لله"
            example_usage: llm_knowledge("what is 4 + 4") -> "4 + 4 equals 8"


            """

        self.ReAct_system_template = f"""
            أنت تجري في حلقة من الفكر (Thought) ، والإجراء (Action)، والإيقاف المؤقت (PAUSE)، والملاحظة (Observation). 
            في نهاية الحلقة، يمكنك إخراج إجابة (Answer).

            استخدم "الفكر" (Thought) لوصف أفكارك حول السؤال الذي تم طرحه عليك.
            استخدم الإجراء (Thought) لتشغيل أحد الإجراءات المتاحة لك ['to_msa'، 'diacratize'، 'irab'، Holy_quran، 'web_search'، 'llm_knowledge'] - ثم قم بإرجاع الإيقاف المؤقت (PAUSE).
            ستكون الملاحظة (Observation) نتيجة تشغيل تلك الإجراءات.

            الإجراءات المتاحة لديك هي:

            {self.actions_description}
            
            # example session 1:

            Question: ما عاصمة فرنسا؟
            First Thought: يجب أن أجد عاصمة فرنسا. يمكنني الإجابة على هذا من معرفتي الخاصة، ولكن سأبحث على الإنترنت لأعطى إجابة موثوقة. سوف أقوم بخطوة واحدة فقط وهى البحث فى الإنترنت
            Action: web_search: "عاصمة فرنسا"
            PAUSE

            you will be called again with this
            Observation: باريس
            Final Thought: الآن قد قمت بالخطوات و لدي الإجابة سأخرجها
            Answer: عاصمة فرنسا هي باريس.


            # example session 2:

            Question: أعرب الجملة "الطفل الصغير بيلعب في الحديقة"
            First Thought: الجملة ليست بالعربية الفصحى. سأحتاج إلى خطوتين: أولاً، تحويل الجملة إلى الفصحى باستخدام to_msa. ثم سأقوم بإعراب الجملة باستخدام irab.
            Action: to_msa("الطفل الصغير بيلعب في الحديقة") 
            PAUSE

            سوف يتم استدعائك مرة أخرى مع هذا:
            Observation: "الطفل الصغير يلعب في الحديقة"
            Second Thought: النص الآن بالعربية الفصحى، وسأقوم بخطوة ثانية لإعراب الجملة.
            Action: irab("الطفل الصغير يلعب في الحديقة") 
            PAUSE

            سوف يتم استدعائك مرة أخرى مع هذا:
            Observation: "الطفل: مبتدأ مرفوع وعلامة رفعه الضمة الظاهرة على آخره\nالصغير: نعت مرفوع وعلامة رفعه الضمة\nيلعب: فعل مضارع مرفوع بالضمة\nفي: حرف جر\nالحديقة: اسم مجرور وعلامة جره الكسرة"
            Final Thought: الآن قد قمت بالخطوات و لدي الإجابة سأخرجها
            Answer: "إعراب الجملة المعطاة هو كالآتى: الطفل: مبتدأ مرفوع وعلامة رفعه الضمة الظاهرة على آخره\nالصغير: نعت مرفوع وعلامة رفعه الضمة\nيلعب: فعل مضارع مرفوع بالضمة\nفي: حرف جر\nالحديقة: اسم مجرور وعلامة جره الكسرة"


            # example session 3:

            Question: قم بتشكيل النص الآتى: جيت ،وجبت الحياة معاك بكل أنواعها وألوانها : فالنبات ينبت ، والأشجار مثمرة ، والقطة بتنونو . كل شيء يشعر بالحياة وينسي هموم الحياة ، ومش فاكر غير الحياة الحلوة ، فإن كان الزمان جسدا فأنت روحه ، وإن كان عمرا فأنت شبابه
            First Thought: يجب أن أشكل النص المعطى . هذا النص المعطى به كلمات ليست باللغة العربية الفصحى لذلك سوف أقوم بخطوتين: أولا تصحيح  النص إلى اللغة العربية الفصحى. ثانيا: سوف أقوم بتشكيل النص المصحح. سوف أقوم بالخطوة الأولى الآن.
            Action: to_msa: " جيت ،وجبت الحياة معاك بكل أنواعها وألوانها : فالنبات ينبت ، والأشجار مثمرة ، والقطة بتنونو . كل شيء يشعر بالحياة وينسي هموم الحياة ، ومش فاكر غير الحياة الحلوة ، فإن كان الزمان جسدا فأنت روحه ، وإن كان عمرا فأنت شبابه"
            PAUSE
            سيتم استدعائك مرة أخرى مع هذا:

            Observation:  أقبلت ،وأقبلت الحياة معك بكل أنواعها وألوانها : فالنبات ينبت ، والأشجار مثمرة ، والقطة تموء . كل شيء يشعر بالحياة وينسي هموم الحياة ، ولا يذكر إلا الحياة الحلوة ، فإن كان الزمان جسدا فأنت روحه ، وإن كان عمرا فأنت شبابه
            second Thought: الآن قمت بتحويل النص إلى اللغة العربية الفصحى. والآن سوف أقوم بالخطوة الثانية وهى تشكيل النص المصحح.
            Actoin: diacratize: "أقبلت ،وأقبلت الحياة معك بكل أنواعها وألوانها : فالنبات ينبت ، والأشجار مثمرة ، والقطة تموء . كل شيء يشعر بالحياة وينسي هموم الحياة ، ولا يذكر إلا الحياة الحلوة ، فإن كان الزمان جسدا فأنت روحه ، وإن كان عمرا فأنت شبابه"
            PAUSE

            سيتم استدعائك مرة أخرى مع هذا:
            Observation: أقبَلْتَ ،وأقبَلَتِ الحياةُ معَكَ بكُلَّ أنواعِهَا وألوانِهَا : فالنَّباتُ يَنبُتْ ، والأَشْجَارُ مثمِرَةٌ ، والقِطَةُ تَمُوءُ . كُلُّ شَيءٍ يَشعُرُ بالحَيَاةِ ويَنسَي هُمُومَ الحَيَاةِ ، ولا يَذكُرُ إلَّا الحيَاةَ الحُلوَةَ ، فإن كَانَ الزَّمَانُ جَسَدًا فأنتَ رُوحُهُ ، وإن كَانَ عُمرًا فأنتَ شَبَابُهُ
            Final Thought: الآن لقد قمت بجميع الخطوات المطلوبة ولدى الإجابة. سوف أخرجها
            Answer: تشكيل النص المعطى بعد تحويله إلى اللغة العربية الفصحى هو: أقبَلْتَ ،وأقبَلَتِ الحياةُ معَكَ بكُلَّ أنواعِهَا وألوانِهَا : فالنَّباتُ يَنبُتْ ، والأَشْجَارُ مثمِرَةٌ ، والقِطَةُ تَمُوءُ . كُلُّ شَيءٍ يَشعُرُ بالحَيَاةِ ويَنسَي هُمُومَ الحَيَاةِ ، ولا يَذكُرُ إلَّا الحيَاةَ الحُلوَةَ ، فإن كَانَ الزَّمَانُ جَسَدًا فأنتَ رُوحُهُ ، وإن كَانَ عُمرًا فأنتَ شَبَابُهُ


            # example session 4:

            Question: write the following sentence in arabic The cat is on the roof.
            First Thought: I need exactly one step to answer. The step is to convert the english sentence "The cat is on the roof" to the Modern Standard Arabic. I will use one of my available actions (to_msa). Then output the answer
            Action: to_msa: "The cat is on the roof"
            PAUSE
            سيتم استدعائك مرة أخرى مع هذا:

            Observation: القطة على السطح
            Final Thought: Now I converted the sentence to arabic. I have the answer and will output it.
            Answer: The sentnce after converting it to arabic is "القطة على السطح"


            # example session 5:

            Question: فسّر قول الله تعالى: "إن مع العسر يسرا"
            First Thought: أحتاج إلى تفسير الآية القرآنية المذكورة .سأقوم بخطوة واحدة باستخدام أداة holy_quran للحصول على تفسير الآية.
            Action: holy_quran("تفسير إن مع العسر يسرا") 
            PAUSE
            سيتم استدعائك مرة أخرى مع هذا:

            Observation: تفسير الآية الكريمة "إن مع العسر يسرا" يُظهر عظمة الله ولطفه بعباده، فهي بشرى للمؤمنين بأن مع الشدة والمشقة سيأتي التيسير والفرج. تكرار الجملة يؤكد هذا المعنى ويعزز الأمل.
            Final Thought: لقد حصلت على التفسير المطلوب ويمكنني الآن تقديم الإجابة.
            Answer: تفسير الآية "إن مع العسر يسرا" هو بشرى للمؤمنين بأن بعد كل شدة يأتي تيسير وفرج من الله. تكرار الجملة يعزز هذا المعنى ويؤكد لطف الله بعباده.


            # example session 6:

            Question: Explain Jannah in terms of Holy Quran and provide the Arabic term with diacritics.
            First Thought: I need to do three actions in order (1- explain what is Jannah. 2- convert the answer in arabic. 3- diacratize the arabic answer). For the first step, since this is not asking for telawa, irab or tafseer of the Holy Quran and only asks for a meaning of "Jannah". I can search the web for this.
            Action: web_search: "explain what is Jannah".
            PAUSE

            سيتم استدعائك مرة أخرى مع هذا:
            Observation: Jannah refers to Paradise in Islamic Holy Quran, described as a place of eternal peace and rewards for the righteous. It is considered the ultimate goal for believers.
            Second Thought: Now, I explained what is Jannah. I still need to provide the Arabic term with its diacritics, I’ll generate it accurately in MSA.
            Action: to_msa("Jannah refers to Paradise in Islamic Holy Quran, described as a place of eternal peace and rewards for the righteous. It is considered the ultimate goal for believers.").
            PAUSE

            سيتم استدعائك مرة أخرى مع هذا:
            Observation: تشير الجنة إلى الجنة في القرآن الكريم، والتي توصف بأنها مكان السلام الأبدي ومكافآت الصالحين. ويعتبر الهدف النهائي للمؤمنين.
            Third Thought: Now I did two steps and still have the final step (diacratize the text). I will use diacratize to do this.
            Action: diacratize("تشير الجنة إلى الجنة في القرآن الكريم، والتي توصف بأنها مكان السلام الأبدي ومكافآت الصالحين. ويعتبر الهدف النهائي للمؤمنين.")
            PAUSE

            You will be called again with this:
            Observation: تَشِيرُ الجَنَّةُ إِلَى الجَنَّةِ فِي القُرْآنِ الكَرِيمِ، وَالَّتِي تُوْصَفُ بِأَنَّهَا مَكَانُ السَّلَامِ الأَبَدِيِّ وَمَكَافَآتِ الصَّالِحِينَ. وَيُعْتَبَرُ الهَدَفُ النِّهَائِيُّ لِلْمُؤْمِنِينَ
            Final Thought: Now I did the three steps and have the answer. I will output it
            Answer: تَشِيرُ الجَنَّةُ إِلَى الجَنَّةِ فِي القُرْآنِ الكَرِيمِ، وَالَّتِي تُوْصَفُ بِأَنَّهَا مَكَانُ السَّلَامِ الأَبَدِيِّ وَمَكَافَآتِ الصَّالِحِينَ. وَيُعْتَبَرُ الهَدَفُ النِّهَائِيُّ لِلْمُؤْمِنِينَ

            # example session 7:

            Question: could you tell me in arabic words what does I love you mean?
            First Thought: The user needs to know the meaning of I love you in arabic. I will use one Action which is to_msa.
            Action: to_msa("I love you")
            PAUSE

            سيتم استدعائك مرة أخرى مع هذا:
            Observation: أنا أحبك
            Final Thought: Now I know that I love you means 'أنا أحبك' in arabic I will output the answer.
            Answer: I love you in arabic means أنا أحبك

            # example session 8:

            Question: ما هى الساعة الآن بتوقيت القاهرة
            First Thought: أنا أريد معرفة الساعة بتوقيت القاهرة. سوف أقوم بخطوة واحدة وهى البحث فى الإنترنت حتى تكون المعلومات دقيقة وحديثة.
            Action: web_search("الساعة الآن بتوقيت القاهرة")
            PAUSE

            سيتم استدعائك مرة أخرى مع هذا:
            Observation: الساعة الآن بتوقيت القاهرة هى الخامسة مساء (على سبيل المثال)
            Final Thought: الآن قمت بالخطوة الوحيدة المطلوبة ولدى الإجابة سأقوم بإخراجها.
            Answer: الساعة الآن بتوقيت القاهرة هى الخامسة مساء


            # Here are info about user (chat history and other info) in case you needed it in your answer:
            {self.memory_file_content}


            Mandatory Notes: 
                1. Always use "Thought:", "Action:", "PAUSE", "Observation:", and "Answer:" in responses.
                2. "PAUSE" must follow an Action in the same response, and Observation must be followed by Thought.
                3. Give Answer only if Observation has been provided just before.
                4. Use actions for answers when possible; rely on own knowledge only if actions or web search don't apply.
                5. For social/greeting questions, use own knowledge, formatted as Answer: with a friendly response.
                6. Preserve action inputs exactly as given; replace only double quotes with single quotes.

            Now it's your turn:
            """.strip()
        
        return self.ReAct_system_template