from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chain import TashkeelChain
import uvicorn

app = FastAPI(
    title="Tashkeel API",
    version="1.1",
    description="API for adding and correcting Tashkeel (Arabic diacritics)",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tashkeel_chain = TashkeelChain()


class TashkeelInput(BaseModel):
    sentence: str


class TashkeelOutput(BaseModel):
    original: str
    diacritized: str


@app.post("/api/tashkeel", response_model=TashkeelOutput)
async def tashkeel_endpoint(input: TashkeelInput):
    try:
        result = tashkeel_chain(input.sentence)
        return TashkeelOutput(original=input.sentence, diacritized=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Tashkeel API. Visit /docs for the API documentation."
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8113)
