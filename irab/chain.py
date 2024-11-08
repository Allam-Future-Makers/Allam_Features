import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from importlib import reload
from irab import prompts

reload(prompts)
irab_prompt = prompts.irab_prompt
split_prompt = prompts.split_prompt
json_parse_prompt = prompts.json_parse_prompt
critic_prompt = prompts.critic_prompt
helper_prompt = prompts.helper_prompt
small_irab_prompt = prompts.small_irab_prompt
small_critic_prompt = prompts.small_critic_prompt

from langchain_core.prompts import PromptTemplate  # noqa: E402, F401
from langchain_ibm import WatsonxLLM  # noqa: E402
from langchain_google_genai import ChatGoogleGenerativeAI  # noqa: E402, F401
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser  # noqa: E402, F401
from langchain_core.runnables import RunnableLambda, RunnableParallel  # noqa: E402
import os, time  # noqa: E402, F401


class IrabChain:
    def __init__(self, instance):
        # Set up variables
        self.instance = instance

        # Initialize models
        self.model_params = {
            "max_new_tokens": 600,
            "min_new_tokens": 0,
            "temperature": 0.00,
            "top_p": 0.88,
            "top_k": 30,
        }

    def log(self, x):
        print(x, end="\n" + "-" * 70 + "\n")
        return x

    def log1(self, x):
        print("\n" + "=" * 50 + "\n")
        return x

    def split_sentence(self, sentence):
        # Chain to split the sentence
        split_chain = split_prompt | self.allam_model | StrOutputParser()
        split_results = split_chain.invoke({"sentence": sentence})
        sentences = split_results.replace("-", "").split("\n")
        try:
            sentences = list(
                set(
                    [
                        sentence.strip()
                        for sentence in sentences[sentences.index("Output:") + 1 :]
                    ]
                )
            )
        except:
            sentences = list(
                set(
                    [
                        sentence.strip()
                        for sentence in sentences[sentences.index(" Output:") + 1 :]
                    ]
                )
            )
        return sentences

    def build_mini_chain(self, sentence, original_sentence):
        i_rab_chain = irab_prompt | self.allam_model | StrOutputParser()
        critic_chain = critic_prompt | self.allam_model | StrOutputParser()
        # i_rab_chain = small_irab_prompt | self.allam_model | StrOutputParser()
        # critic_chain = small_critic_prompt | self.allam_model | StrOutputParser()

        llm_chain = (
            RunnableLambda(
                lambda x: {"sentence": sentence, "original_sentence": original_sentence}
            )
            | i_rab_chain
            # | RunnableLambda(self.log)
            | RunnableLambda(
                lambda result: {"sentence": sentence, "irab_results": result}
            )
            | critic_chain
            # | RunnableLambda(self.log)
            # | RunnableLambda((self.log1))
            | RunnableLambda(
                lambda critic_result: {
                    "sentence": sentence,
                    "critic_results": critic_result,
                }
            )
        )
        return llm_chain

    def build_parallel_chain(self, sentences, original_sentence):
        tasks = {
            f"sentence_{idx}": self.build_mini_chain(sentence, original_sentence)
            for idx, sentence in enumerate(sentences)
        }
        parallel_chain = RunnableParallel(**tasks)
        return parallel_chain

    def process_sentences_parallel(self, sentences, original_sentence):
        parallel_chain = self.build_parallel_chain(sentences, original_sentence)
        result = parallel_chain.invoke({})
        return result

    def process_irab(self, paragraph):
        # Initialize models
        self.allam_model = WatsonxLLM(
            project_id=self.instance.watsons["project_id"],
            apikey=self.instance.watsons["key"],
            model_id="sdaia/allam-1-13b-instruct",
            url="https://eu-de.ml.cloud.ibm.com",
            params=self.model_params,
        )
        self.gemini_model = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            max_output_tokens=None,
            temperature=0.18,
            api_key=self.instance.gemini_keys[
                self.instance.iterator % (len(self.instance.gemini_keys))
            ],
        )

        self.paragraph = paragraph

        # Step 1: Split sentences
        split_sentences = self.split_sentence(self.paragraph)

        # Step 2: Use helper chain with Gemini model
        helper_chain = helper_prompt | self.gemini_model
        sentences = eval(
            helper_chain.invoke({"sentence": split_sentences}).content.replace("\n", "")
        )
        # Pretty print the sentences
        # print(sentences, end="\n" + "-" * 50 + "\n")

        # Step 3: Process sentences in parallel
        results = self.process_sentences_parallel(sentences, self.paragraph)
        # Pretty print the results
        # print(json.dumps(results, indent=4, ensure_ascii=False))
        # print("\n" + "#" * 50 + "\n")
        # Step 4: Parse results using the Gemini model

        json_parse_chain = json_parse_prompt | self.gemini_model | JsonOutputParser()
        gemini_result = json_parse_chain.invoke(
            {"sentence": self.paragraph, "irab_results": results}
        )

        self.instance.iterator += 1

        self.output_as_text = " ".join(
             [
                 f'كلمة "{item["word"]}" هي {item["irab"]}.'
                 for item in gemini_result["irab_results"]
             ]
        )

        return gemini_result

    def __call__(self, paragraph):
        _ = self.process_irab(paragraph)  
        return self.output_as_text


# Usage
# processor = IrabProcessor()
# long_sentence = "إنَّ العلمَ نورٌ يهتدي به الإنسانُ في ظلماتِ الجهلِ، ولن ينالَ المجدَ من لم يسع إليه بجدٍّ وإصرارٍ"
# long_sentence = "ذهبَ الطِّفلُ إلى المدرسةِ صباحًا. قرأَ في الكتابِ الجديدِ. شرحَ المعلمُ الدرسَ بوضوحٍ. استمعَ الطُّلابُ بانتباهٍ. وعادَ الجميعُ إلى منازلِهم بعد انتهاءِ الدرسِ."
# final_result = processor.process_irab(long_sentence)
