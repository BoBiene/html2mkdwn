"""This is the main file for the FastAPI application. It contains the logic for extracting markdown from HTML content and URLs. The application uses the trafilatura library to extract markdown from HTML content. """

import trafilatura
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class TextExtractionRequest(BaseModel):
    """Request model for extracting markdown from html content"""

    html_content: str


@app.post("/html/")
async def extract_markdown(request: TextExtractionRequest):
    """Extract markdown from html content"""
    try:
        markdown = trafilatura.extract(
            filecontent=request.html_content, output_format="markdown"
        )
        if markdown:
            return {"markdown": markdown}

        raise HTTPException(
            status_code=404, detail="Extraction failed: No content extracted"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Extraction error: {str(e)}"
        ) from e


class URLExtractionRequest(BaseModel):
    """Request model for extracting markdown from a URL"""

    url: str


@app.post("/url/")
async def extract_markdown_from_url(request: URLExtractionRequest):
    """Extract markdown from a URL"""
    try:
        html_content = trafilatura.fetch_url(request.url)
        markdown = trafilatura.extract(
            filecontent=html_content, output_format="markdown"
        )
        if markdown:
            return {"markdown": markdown}

        raise HTTPException(status_code=404, detail="Extraction failed")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Extraction error: {str(e)}"
        ) from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
