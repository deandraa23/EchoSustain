import io
import uuid
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pypdf

from backend.services.audit_service import AuditService
from backend.services.s3_service import S3Service
from backend.database import init_db, save_audit, get_audit, get_all_audits

app = FastAPI(title="EchoSustain Enterprise ESG Engine")

# Initialize database table
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

audit_service = AuditService()
s3_service = S3Service()

class ChatRequest(BaseModel):
    audit_id: str
    question: str

@app.get("/")
def root():
    return {"status": "EchoSustain API Operational"}

@app.get("/audits")
def fetch_audits():
    return {"audits": get_all_audits()}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        content = await file.read()
        file_size = len(content)

        # 1. Extract text from PDF
        pdf_reader = pypdf.PdfReader(io.BytesIO(content))
        raw_text = "".join([page.extract_text() or "" for page in pdf_reader.pages])
        if not raw_text.strip():
            raw_text = "No extractable text found."

        audit_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        s3_key = f"{audit_id}/{file.filename}"

        # 2. Upload to S3 (LocalStack or AWS)
        s3_path = s3_service.upload_file_bytes(content, s3_key)

        # 3. Deterministic Gemini Audit
        audit_results = audit_service.analyze_report(raw_text)

        # 4. Save to SQLite database
        save_audit(
            audit_id=audit_id,
            filename=file.filename,
            file_size_bytes=file_size,
            s3_path=s3_path,
            timestamp=timestamp,
            raw_text=raw_text,
            results=audit_results
        )

        return {
            "success": True,
            "audit_id": audit_id,
            "filename": file.filename,
            "s3_path": s3_path,
            "timestamp": timestamp,
            "audit_results": audit_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat_endpoint(payload: ChatRequest):
    record = get_audit(payload.audit_id)
    if not record:
        raise HTTPException(status_code=404, detail="Audit context not found.")

    context = (
        f"Document: {record['filename']}\n"
        f"Score: {record['audit_results'].get('transparency_score')}/100\n"
        f"Summary: {record['audit_results'].get('summary')}\n"
        f"Flagged Claims: {record['audit_results'].get('claims_analyzed')}\n"
        f"Text excerpt: {record.get('raw_text', '')[:6000]}"
    )

    prompt = (
        f"You are the EchoSustain Senior ESG Lead Auditor.\n"
        f"Answer the user's question accurately using only this audit context:\n{context}\n\n"
        f"User Question: {payload.question}"
    )

    try:
        response = audit_service.model.generate_content(prompt)
        return {"answer": response.text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))