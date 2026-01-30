"""
Audit service for managing audit lifecycle
"""
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from backend.models import Audit, AuditResult


class AuditService:
    """Service for managing audit operations"""

    @staticmethod
    def create_audit(db: Session, image_url: str, image_path: str = None) -> Audit:
        """Create a new audit record"""
        audit_id = f"audit_{uuid.uuid4().hex[:12]}"
        audit = Audit(
            id=audit_id,
            image_url=image_url,
            image_path=image_path,
            status="pending",
        )
        db.add(audit)
        db.commit()
        db.refresh(audit)
        return audit

    @staticmethod
    def get_audit(db: Session, audit_id: str) -> Audit:
        """Get audit by ID"""
        return db.query(Audit).filter(Audit.id == audit_id).first()

    @staticmethod
    def update_audit_status(db: Session, audit_id: str, status: str, error: str = None):
        """Update audit status"""
        audit = db.query(Audit).filter(Audit.id == audit_id).first()
        if audit:
            audit.status = status
            audit.error_message = error
            audit.updated_at = datetime.utcnow()
            db.commit()

    @staticmethod
    def save_audit_results(
        db: Session,
        audit_id: str,
        inspector_json: dict = None,
        analyst_json: dict = None,
        advisor_json: dict = None,
    ):
        """Save audit results"""
        result = db.query(AuditResult).filter(AuditResult.audit_id == audit_id).first()

        if result:
            result.inspector_json = inspector_json or result.inspector_json
            result.analyst_json = analyst_json or result.analyst_json
            result.advisor_json = advisor_json or result.advisor_json
            result.updated_at = datetime.utcnow()
        else:
            result = AuditResult(
                audit_id=audit_id,
                inspector_json=inspector_json,
                analyst_json=analyst_json,
                advisor_json=advisor_json,
            )
            db.add(result)

        db.commit()
        return result

    @staticmethod
    def get_audit_with_results(db: Session, audit_id: str):
        """Get audit with all results"""
        audit = db.query(Audit).filter(Audit.id == audit_id).first()
        if audit and audit.results:
            return {
                "id": audit.id,
                "status": audit.status,
                "created_at": audit.created_at.isoformat(),
                "updated_at": audit.updated_at.isoformat(),
                "error": audit.error_message,
                "inspector": audit.results.inspector_json,
                "analyst": audit.results.analyst_json,
                "advisor": audit.results.advisor_json,
            }
        return {
            "id": audit.id if audit else None,
            "status": audit.status if audit else "not_found",
            "created_at": audit.created_at.isoformat() if audit else None,
        }

    @staticmethod
    def list_audits(db: Session, limit: int = 20, offset: int = 0):
        """List all audits with pagination"""
        audits = db.query(Audit).order_by(Audit.created_at.desc()).limit(limit).offset(offset).all()
        total = db.query(Audit).count()

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "audits": [
                {
                    "id": a.id,
                    "status": a.status,
                    "created_at": a.created_at.isoformat(),
                    "violation_count": len(a.results.analyst_json.get("violations", [])) if a.results else 0,
                }
                for a in audits
            ],
        }
