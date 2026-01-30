"""
API routes for audit operations
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Audit
from backend.services.audit import AuditService
from backend.services.storage import StorageService
from backend.tasks import run_audit_pipeline
from pydantic import BaseModel

router = APIRouter(prefix="/audits", tags=["audits"])


@router.post("/upload")
async def upload_design(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload a design image for analysis"""

    # Validate file type
    if file.content_type not in ["image/png", "image/jpeg", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Supported: PNG, JPG, WebP")

    try:
        # Save file
        file_path, storage_url = await StorageService.save_upload(file)

        # Create audit record
        audit = AuditService.create_audit(db, storage_url, file_path)

        # Queue async task
        run_audit_pipeline.delay(audit.id, storage_url)

        return {
            "audit_id": audit.id,
            "status": "pending",
            "created_at": audit.created_at.isoformat(),
            "message": "Design analysis started",
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/{audit_id}")
async def get_audit(audit_id: str, db: Session = Depends(get_db)):
    """Get audit results"""
    audit = AuditService.get_audit(db, audit_id)

    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")

    return AuditService.get_audit_with_results(db, audit_id)


@router.get("")
async def list_audits(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    """List all audits"""
    return AuditService.list_audits(db, limit, offset)


class ChatMessage(BaseModel):
    question: str


@router.post("/{audit_id}/chat")
async def ask_question(audit_id: str, message: ChatMessage, db: Session = Depends(get_db)):
    """Ask a follow-up question about the audit"""
    audit = AuditService.get_audit(db, audit_id)

    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")

    if audit.status != "completed":
        raise HTTPException(status_code=400, detail="Audit not yet completed")

    try:
        from agents.advisor.feedback_generator import FeedbackGenerator

        generator = FeedbackGenerator()
        context = AuditService.get_audit_with_results(db, audit_id)

        answer = await generator.answer_question(message.question, context)

        return {
            "answer": answer,
            "sources": ["Audit Analysis", "Design Guidelines"],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to answer question: {str(e)}")
