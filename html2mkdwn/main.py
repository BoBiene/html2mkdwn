from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import trafilatura

app = FastAPI()


class TextExtractionRequest(BaseModel):
    html_content: str


@app.post("/html/")
async def extract_markdown(request: TextExtractionRequest):
    try:
        markdown = trafilatura.extract(
            filecontent=request.html_content, output_format="markdown"
        )
        if markdown:
            return {"markdown": markdown}
        else:
            raise HTTPException(
                status_code=404, detail="Extraction failed: No content extracted"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction error: {str(e)}")


class URLExtractionRequest(BaseModel):
    url: str


@app.post("/url/")
async def extract_markdown_from_url(request: URLExtractionRequest):
    try:
        html_content = trafilatura.fetch_url(request.url)
        markdown = trafilatura.extract(
            filecontent=html_content, output_format="markdown"
        )
        if markdown:
            return {"markdown": markdown}
        else:
            raise HTTPException(status_code=404, detail="Extraction failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
