from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from HolyQuran.chain import HolyQuranChain
from Mo3gam_Search.chain import Mo3gamSearchChain
from diacratization.chain import DiacratizeChain
from irab.chain import IrabChain
from syntax_enhancer.chain import SyntaxEnhancerChain
from to_MSA.chain import ToMSAChain

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
    helper_sentence: str


class SyntaxEnhancerInput(BaseModel):
    sentence: str


class ToMSAInput(BaseModel):
    paragraph: str


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
        result = quran_chain(input.query)
        return QuranOutput(answer=result)
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


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8113)