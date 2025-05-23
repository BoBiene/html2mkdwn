"""
Main module for the HTML to Markdown extraction service.
Provides an API endpoint to convert HTML content to Markdown.
"""

import logging  # Standard library imports
from typing import Optional  # Add if needed

from fastapi import FastAPI, HTTPException  # Third-party imports
from pydantic import BaseModel
import trafilatura
import html2text
from bs4 import BeautifulSoup

# Initialize logger and FastAPI app
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
app = FastAPI()

class TextExtractionRequest(BaseModel):
    """Request model for text extraction."""
    html_content: Optional[str]

class URLExtractionRequest(BaseModel):
    url: str

def fallback_html2text(html: str) -> str:
    """Fallback function to convert HTML to plain text."""
    try:
        handler = html2text.HTML2Text()
        handler.ignore_links = False
        markdown = handler.handle(html)
        if markdown and markdown.strip():
            return markdown
    except Exception as e:
        logger.error("html2text fallback failed: %s", str(e), exc_info=True)
    # Last fallback: plain text extraction with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n")

@app.post("/html/")
async def extract_markdown(request: TextExtractionRequest):
    """
    Extract markdown from HTML content. Always returns markdown or plain text.

    Args:
        request (TextExtractionRequest): The request containing HTML content.

    Returns:
        dict: A dictionary containing the extracted markdown.
    """
    logger.info("Received extraction request.")

    html = request.html_content
    if not html or not html.strip():
        logger.warning("Empty html_content received.")
        raise HTTPException(status_code=400, detail="No HTML content provided.")

    try:
        markdown = trafilatura.extract(
            filecontent=html, output_format="markdown"
        )
        if markdown and markdown.strip():
            logger.info("Extraction via trafilatura successful. Content length: %d", len(markdown))
            return {"markdown": markdown}
        # Fallback if trafilatura fails
        logger.warning("trafilatura.extract() returned None or empty, using fallback.")
        markdown = fallback_html2text(html)
        logger.info("Fallback extraction successful. Content length: %d", len(markdown))
        return {"markdown": markdown}
    except ValueError as e:  # Replace with a more specific exception if applicable
        logger.error("Error during markdown extraction: %s", str(e))
        raise HTTPException(status_code=500, detail="Error during markdown extraction.")

@app.post("/url/")
async def extract_markdown_from_url(request: URLExtractionRequest):
    """Extract markdown from a URL. Always returns markdown or plain text."""
    logger.info("Received URL extraction request: %s", request.url)
    try:
        html_content = trafilatura.fetch_url(request.url)
        if not html_content or not html_content.strip():
            logger.warning("Fetching URL failed or empty content.")
            raise HTTPException(status_code=404, detail="Failed to fetch URL content.")

        markdown = trafilatura.extract(
            filecontent=html_content, output_format="markdown"
        )
        if markdown and markdown.strip():
            logger.info("Extraction via trafilatura successful. Content length: %d", len(markdown))
            return {"markdown": markdown}
        # Fallback if trafilatura fails
        logger.warning("trafilatura.extract() returned None or empty for URL, using fallback.")
        markdown = fallback_html2text(html_content)
        logger.info("Fallback extraction successful. Content length: %d", len(markdown))
        return {"markdown": markdown}
    except Exception as e:
        logger.error("Extraction error (url): %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Extraction error: {str(e)}"
        ) from e

@app.get("/healthz")
def healthcheck():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
