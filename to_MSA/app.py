# import libraries
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chain import ToMSAChain
import uvicorn

# Initialize the FastAPI app
app = FastAPI(
    title="ToMSA API",
    version="1.0",
    description="API for converting Arabic dialects to Modern Standard Arabic",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the ToMSAChain
tomsa_chain = ToMSAChain(cares_about_requests=True)


# Define input and output models
class ToMSAInput(BaseModel):
    sentence: str


class ToMSAOutput(BaseModel):
    input_sentence: str
    primary_corrected_sentence: str
    finally_corrected_sentence: str


@app.post("/api/tomsa", response_model=ToMSAOutput)
async def tomsa_endpoint(input: ToMSAInput):
    try:
        # Use `ainvoke` for asynchronous invocation
        result = await tomsa_chain.to_MSA_chain.ainvoke({"sentence": input.sentence})
        return ToMSAOutput(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Add a simple health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Add API documentation
@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Welcome to the ToMSA API. Visit /docs for the API documentation."
    }


@app.post("/api/test")
async def test_route(input: ToMSAInput):
    return {"message": "Test route working", "received": input.sentence}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8111)
