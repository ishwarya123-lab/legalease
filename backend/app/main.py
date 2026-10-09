from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import base64

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"))

from app.schemas import GenerateRequest, GenerateResponse, ExportRequest
from app.services.gemini_service import generate_document
from app.services.export_service import generate_pdf, generate_docx, generate_txt
from app.services.analytics_service import get_analytics

app = FastAPI(title="LegalEase API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/generate", response_model=GenerateResponse)
def generate_endpoint(request: GenerateRequest):
    try:
        doc, terms = generate_document(request.document_type, request.data)
        return GenerateResponse(markdown_content=doc, term_table=terms)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/preview")
def preview_endpoint(request: ExportRequest):
    return {"preview_text": request.markdown_content}

@app.post("/api/v1/analytics")
def analytics_endpoint(request: GenerateRequest):
    """Returns NumPy-computed financial metrics and a Matplotlib-generated chart (base64 PNG)."""
    try:
        metrics, chart_buf = get_analytics(request.document_type, request.data)
        chart_b64 = base64.b64encode(chart_buf.read()).decode('utf-8')
        return {"metrics": metrics, "chart_base64": chart_b64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/export/pdf")
def export_pdf(request: ExportRequest):
    try:
        chart_bytes = base64.b64decode(request.chart_base64) if request.chart_base64 else None
        pdf_buffer = generate_pdf(request.markdown_content, chart_bytes)
        return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=document.pdf"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/export/docx")
def export_docx(request: ExportRequest):
    try:
        chart_bytes = base64.b64decode(request.chart_base64) if request.chart_base64 else None
        docx_buffer = generate_docx(request.markdown_content, chart_bytes)
        return StreamingResponse(docx_buffer, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers={"Content-Disposition": "attachment; filename=document.docx"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/export/txt")
def export_txt(request: ExportRequest):
    try:
        txt_buffer = generate_txt(request.markdown_content)
        return StreamingResponse(txt_buffer, media_type="text/plain", headers={"Content-Disposition": "attachment; filename=document.txt"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
