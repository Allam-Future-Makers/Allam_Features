from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from HolyQuran.chain import HolyQuranChain
from Mo3gam_Search.chain import Mo3gamSearchChain
from agent.main import AgentMain
from diacratization.chain import DiacratizeChain
from irab.chain import IrabChain
from syntax_enhancer.chain import SyntaxEnhancerChain
from to_MSA.chain import ToMSAChain

from dotenv import load_dotenv

load_dotenv()

watsons = {
    "key": "tBmyiiTXb1TYJQPrYHOCjiek8iIQGZoqqZreZwrpSRCM",
    "project_id": "89b6a9d9-cb31-48fd-b5a4-9ed49fdaab52",
}
gemini_keys = [
    "AIzaSyA0WgVJxLelaY3fvIhq4XK8Av9udDfJ9rI",
    "AIzaSyDof2hE1nOYkSx3vslyRl696NVoBeXCKH8",
    "AIzaSyC57_NvRsktnNgLvtyutDclVkCS2I4MKDI",
    "AIzaSyDzyMWZB82YyWKzf21k6qdiAn4JG6DXL-Q",
    "AIzaSyC2YG-msSXWXOxnzaxSlEPnQE4scpNLOAc",
]


class DiacratizeInstance:
    def __init__(self):
        self.watsons = watsons
        self.gemini_keys = gemini_keys
        self.iterator = 0


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

diacratize_chain = DiacratizeChain(DiacratizeInstance())
quran_chain = HolyQuranChain(DiacratizeInstance())
irab_chain = IrabChain(DiacratizeInstance())
mo3gam_chain = Mo3gamSearchChain(DiacratizeInstance())
syntax_enhancer_chain = SyntaxEnhancerChain(DiacratizeInstance())
msa_chain = ToMSAChain(DiacratizeInstance())


class TashkeelInput(BaseModel):
    sentence: str


class TashkeelOutput(BaseModel):
    original: str
    diacritized: str


class QuranInput(BaseModel):
    query: str


class QuranOutput(BaseModel):
    answer: str


class IrabInput(BaseModel):
    paragraph: str


class Mo3gamInput(BaseModel):
    word: str
    helper_sentence: str | None = None


class SyntaxEnhancerInput(BaseModel):
    sentence: str


class ToMSAInput(BaseModel):
    paragraph: str


class AgentInput(BaseModel):
    id: str
    query: str
    voice_url: str | None = None
    image_url: str | None = None


@app.post("/api/tashkeel", response_model=TashkeelOutput)
async def tashkeel_endpoint(input: TashkeelInput):
    try:
        result = diacratize_chain(input.sentence)
        return TashkeelOutput(original=input.sentence, diacritized=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/quran", response_model=QuranOutput)
async def quran_endpoint(input: QuranInput):
    try:
        text_result, links = quran_chain.get_results(input.query)
        print(text_result)
        print(links)
        return QuranOutput(answer=text_result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/irab")
async def irab_endpoint(input: IrabInput):
    try:
        result = irab_chain.process_irab(input.paragraph)[0]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/mo3gam")
async def mo3gam_endpoint(input: Mo3gamInput):
    try:
        result = mo3gam_chain(input.word, input.helper_sentence)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/syntax_enhancer")
async def syntax_enhancer_endpoint(input: SyntaxEnhancerInput):
    try:
        result = syntax_enhancer_chain(input.sentence)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/to_msa")
async def to_msa_endpoint(input: ToMSAInput):
    try:
        result = msa_chain(input.paragraph)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


import requests
import os
import time


def download_file(url, filename):
    with open(filename, "wb") as f:
        response = requests.get(url)
        f.write(response.content)


# agent map by id to agent instance
agent_map = {}


def getOrCreateAgent(id):
    if id not in agent_map:
        agent_map[id] = AgentMain(id)
    return agent_map[id]


# agent
# takes query, optional voice_url, optional image_url
# returns the answer
@app.post("/api/agent")
async def agent_endpoint(input: AgentInput):
    try:
        # download voice and image if not none
        voice_path = None
        image_path = None
        timestamp = str(int(time.time()))

        if input.voice_url:
            voice_path = f"agent_inputs/voice_{timestamp}.wav"
            download_file(input.voice_url, voice_path)
        if input.image_url:
            image_path = f"agent_inputs/image_{timestamp}.png"
            download_file(input.image_url, image_path)

        agent = getOrCreateAgent(input.id)
        answer = agent(input.query, voice_path, image_path)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8113)
