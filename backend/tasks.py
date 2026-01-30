"""
Celery task definitions for async audit processing
"""
import asyncio
from celery import Celery
from backend.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from backend.database import SessionLocal
from backend.services.audit import AuditService
from agents.orchestrator import AuditOrchestrator

# Initialize Celery
celery_app = Celery(
    "designaudit",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task(bind=True, max_retries=3)
def run_audit_pipeline(self, audit_id: str, image_url: str):
    """
    Run the complete audit pipeline asynchronously
    """
    db = SessionLocal()
    try:
        # Update status to inspecting
        AuditService.update_audit_status(db, audit_id, "inspecting")

        # Run orchestrator
        orchestrator = AuditOrchestrator()
        result = asyncio.run(orchestrator.run_audit(None, image_url))

        if result.get("status") == "completed":
            # Save results
            AuditService.save_audit_results(
                db,
                audit_id,
                inspector_json=result.get("inspector"),
                analyst_json=result.get("analyst"),
                advisor_json=result.get("advisor"),
            )
            # Update status
            AuditService.update_audit_status(db, audit_id, "completed")
        else:
            # Failed
            AuditService.update_audit_status(db, audit_id, "failed", result.get("error"))

        return result

    except Exception as exc:
        print(f"Audit pipeline failed: {exc}")
        AuditService.update_audit_status(db, audit_id, "failed", str(exc))
        # Retry after 60 seconds
        raise self.retry(exc=exc, countdown=60)

    finally:
        db.close()
