# Import necessary libraries
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any
from chain import (
    ToMSAParagraphChain,
)  # Assuming your chain class is ToMSAParagraphChain
import uvicorn
import logging
import os


app = FastAPI(
    title="ToMSA API",
    version="1.0.1",
    description="API for converting Arabic dialects to Modern Standard Arabic (MSA)",
    contact={
        "name": "Support Team",
        "email": "support@msa-converter.com",
    },
)


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Allow cross-origin requests from any domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize the ToMSAParagraphChain class
# We can toggle whether to care about requests, like in the init method of the class
tomsa_chain = ToMSAParagraphChain(cares_about_requests=True)


# Define input and output models using Pydantic for validation
# Define input and output models using Pydantic for validation
class ToMSAInput(BaseModel):
    sentence: str


class ToMSAOutput(BaseModel):
    input_sentence: str
    primary_corrected_sentence: str
    finally_corrected_sentence: str


# Define input model for paragraph processing
class ToMSAParagraphInput(BaseModel):
    paragraph: str


class ToMSAParagraphOutput(BaseModel):
    processed_paragraph: str


# Health check route for basic monitoring
@app.get("/health", tags=["Health"])
async def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "healthy"}, status_code=200)


# API documentation landing page
@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Welcome to the ToMSA API. Visit /docs for the API documentation."
    }


# Test endpoint (for testing purposes, not to be used in production)
@app.post("/api/test", tags=["Testing"])
async def test_route(input: ToMSAInput) -> Any:
    logger.info(f"Test route received input: {input.sentence}")
    return {"message": "Test route working", "received": input.sentence}


# Endpoint for processing entire paragraphs
@app.post(
    "/api/tomsa-paragraph", response_model=ToMSAParagraphOutput, tags=["Processing"]
)
def tomsa_paragraph_endpoint(input: ToMSAParagraphInput) -> ToMSAParagraphOutput:
    try:
        processed_paragraph = tomsa_chain._process_paragraph(
            tomsa_chain.to_MSA_chain, input.paragraph
        )
        return ToMSAParagraphOutput(processed_paragraph=processed_paragraph)
    except Exception as e:
        logger.error(f"Error processing paragraph: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process paragraph.")


# Run the server using uvicorn (FastAPI’s recommended ASGI server)
if __name__ == "__main__":
    port = 8112
    uvicorn.run(app, host="localhost", port=port)
