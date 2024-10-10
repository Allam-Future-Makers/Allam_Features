from importlib import reload
import Allam_Features.irab.prompts as prompts

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
import os  # noqa: E402, F401
import json  # noqa: E402, F401


class IrabProcessor:
    def __init__(self):
        # Set up environment variables
        os.environ["WATSONX_APIKEY"] = "I23GGOrvbVPdcG-MzPGPmxv8Cv7LezjfmmDQT2APmmet"
        os.environ["GOOGLE_API_KEY"] = "AIzaSyDzyMWZB82YyWKzf21k6qdiAn4JG6DXL-Q"
        os.environ["PROJECT_ID"] = "40481c96-7240-4b7d-8d44-08a21aea2013"
        os.environ["MODEL_ID"] = "sdaia/allam-1-13b-instruct"
        os.environ["CLOUD_URL"] = "https://eu-de.ml.cloud.ibm.com"

        # Initialize models
        model_params = {
            "max_new_tokens": 600,
            "min_new_tokens": 0,
            "temperature": 0.12,
            "top_p": 0.88,
            "top_k": 30,
        }

        # Initialize models
        self.allam_model = WatsonxLLM(
            project_id=os.getenv("PROJECT_ID"),
            model_id=os.getenv("MODEL_ID"),
            url=os.getenv("CLOUD_URL"),
            params=model_params,
        )
        self.gemini_model = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            max_output_tokens=None,
            temperature=0.18,
        )

    def log(self, x):
        print(x)
        return x

    def split_sentence(self, sentence):
        # Chain to split the sentence
        split_chain = split_prompt | self.allam_model | StrOutputParser()
        split_results = split_chain.invoke({"sentence": sentence})
        sentences = split_results.replace("-", "").split("\n")
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
            | RunnableLambda(self.log)
            | RunnableLambda(
                lambda result: {"sentence": sentence, "irab_results": result}
            )
            | critic_chain
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

    def process_irab(self, long_sentence):
        # Step 1: Split sentences
        split_sentences = self.split_sentence(long_sentence)

        # Step 2: Use helper chain with Gemini model
        helper_chain = helper_prompt | self.gemini_model
        sentences = eval(
            helper_chain.invoke({"sentence": split_sentences}).content.replace("\n", "")
        )
        print(sentences, end="\n" + "-" * 50 + "\n")

        # Step 3: Process sentences in parallel
        results = self.process_sentences_parallel(sentences, long_sentence)

        # Step 4: Parse results using the Gemini model
        json_parse_chain = json_parse_prompt | self.gemini_model | JsonOutputParser()
        gemini_result = json_parse_chain.invoke(
            {"sentence": long_sentence, "irab_results": results}
        )

        # Pretty print the final result
        print(json.dumps(gemini_result, indent=4, ensure_ascii=False))
        return gemini_result

    def __call__(self, long_sentence):
        return self.process_irab(long_sentence)

# Usage
#processor = IrabProcessor()
#long_sentence = "إنَّ العلمَ نورٌ يهتدي به الإنسانُ في ظلماتِ الجهلِ، ولن ينالَ المجدَ من لم يسع إليه بجدٍّ وإصرارٍ"
# long_sentence = "ذهبَ الطِّفلُ إلى المدرسةِ صباحًا. قرأَ في الكتابِ الجديدِ. شرحَ المعلمُ الدرسَ بوضوحٍ. استمعَ الطُّلابُ بانتباهٍ. وعادَ الجميعُ إلى منازلِهم بعد انتهاءِ الدرسِ."
# long_sentence = "'شرحَ المعلمُ الدرسَ بوضوحٍ.'"
#final_result = processor.process_irab(long_sentence)


# print(critic_prompt)
# %load_ext autoreload
# %autoreload 2
