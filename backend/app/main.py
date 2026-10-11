"""HTTP API for Menu Value. Run from the backend/ folder:

    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000/docs to try every endpoint in the browser.
"""

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.pipeline.analyze import analyze_menu_text
from app.pipeline.ocr import DEMO_MENU_TEXT, OCRNotImplemented, extract_text
from app.schemas import MenuAnalysis, TextAnalysisRequest

app = FastAPI(title="Menu Value API", version="0.1.0")

# The website's dev server proxies /api to this backend, so CORS isn't needed
# in development. When you deploy the site and API on different domains
# (week 6), add the site's URL here.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

NEIGHBORHOODS = [
    "Hyde Park",
    "Lincoln Park",
    "Logan Square",
    "Pilsen",
    "West Loop",
    "Wicker Park",
]

MAX_IMAGE_BYTES = 10 * 1024 * 1024


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/neighborhoods")
def neighborhoods() -> list[str]:
    return NEIGHBORHOODS


@app.post("/api/analyze/text", response_model=MenuAnalysis)
def analyze_text(req: TextAnalysisRequest) -> MenuAnalysis:
    return analyze_menu_text(req.text, req.neighborhood)


@app.get("/api/analyze/demo", response_model=MenuAnalysis)
def analyze_demo(neighborhood: str | None = None) -> MenuAnalysis:
    return analyze_menu_text(DEMO_MENU_TEXT, neighborhood)


@app.post("/api/analyze/image", response_model=MenuAnalysis)
async def analyze_image(
    image: UploadFile = File(...),
    neighborhood: str | None = Form(None),
) -> MenuAnalysis:
    if not (image.content_type or "").startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file.")
    data = await image.read()
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image is larger than 10 MB.")
    try:
        text = extract_text(data)
    except OCRNotImplemented as e:
        raise HTTPException(status_code=501, detail=str(e))
    return analyze_menu_text(text, neighborhood)
