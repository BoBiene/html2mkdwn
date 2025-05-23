"""
This is the main file for the FastAPI application.
It contains the logic for extracting markdown from HTML content and URLs.
The application uses the trafilatura library to extract markdown from HTML content.
"""

import trafilatura
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

# Logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("html2markdown")

app = FastAPI()


class TextExtractionRequest(BaseModel):
    html_content: str


@app.post("/html/")
async def extract_markdown(request: TextExtractionRequest):
    """Extract markdown from html content."""
    logger.info("Received extraction request.")
    html = request.html_content

    if not html or not html.strip():
        logger.warning("Empty html_content received.")
        raise HTTPException(status_code=400, detail="No HTML content provided.")

    try:
        markdown = trafilatura.extract(
            filecontent=html, output_format="markdown"
        )
        if markdown:
            logger.info("Extraction successful. Content length: %d", len(markdown))
            return {"markdown": markdown}
        else:
            logger.warning("Extraction failed: No content extracted.")
            raise HTTPException(
                status_code=404, detail="Extraction failed: No content extracted"
            )
    except Exception as e:
        logger.error("Extraction error: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Extraction error: {str(e)}"
        ) from e


class URLExtractionRequest(BaseModel):
    url: str


@app.post("/url/")
async def extract_markdown_from_url(request: URLExtractionRequest):
    """Extract markdown from a URL."""
    logger.info("Received URL extraction request: %s", request.url)
    try:
        html_content = trafilatura.fetch_url(request.url)
        if not html_content:
            logger.warning("Fetching URL failed or no content.")
            raise HTTPException(status_code=404, detail="Failed to fetch URL content.")

        markdown = trafilatura.extract(
            filecontent=html_content, output_format="markdown"
        )
        if markdown:
            logger.info("Extraction from URL successful. Content length: %d", len(markdown))
            return {"markdown": markdown}
        else:
            logger.warning("Extraction failed: No content extracted from URL.")
            raise HTTPException(status_code=404, detail="Extraction failed")

    except Exception as e:
        logger.error("Extraction error: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Extraction error: {str(e)}"
        ) from e


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    logger.error("HTTPException: %s", exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
