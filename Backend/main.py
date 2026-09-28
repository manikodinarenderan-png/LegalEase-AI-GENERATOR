from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="LegalEase API")


class DocumentRequest(BaseModel):
    document_type: str = Field(
        ...,
        min_length=2,
        max_length=120
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=5000
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=10000
    )

    effective_date: str = Field(
        ...,
        min_length=2,
        max_length=100
    )


class DocumentResponse(BaseModel):
    document_type: str
    content: str


@app.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest) -> DocumentResponse:
    content = f"""DRAFT {request.document_type.upper()}

Effective date: {request.effective_date}

1. PARTIES
{request.parties}

2. TERMS AND CONDITIONS
{request.terms}

3. EFFECTIVE DATE
This draft takes effect on {request.effective_date}.

4. SIGNATURES

Party 1: ______________________________    Date: ______________

Party 2: ______________________________    Date: ______________

For informational use only. Have this draft reviewed by a qualified legal professional before signing or relying on it."""

    return DocumentResponse(
        document_type=request.document_type,
        content=content,
    )