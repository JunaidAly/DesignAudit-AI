"""
Database Models for DesignAudit AI
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    audits = relationship("Audit", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Audit(Base):
    __tablename__ = "audits"

    id = Column(String(255), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    image_url = Column(Text, nullable=False)
    image_path = Column(Text, nullable=True)
    status = Column(String(50), default="pending")  # pending, inspecting, analyzing, advising, completed, failed
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="audits")
    results = relationship("AuditResult", back_populates="audit", uselist=False)

    def __repr__(self):
        return f"<Audit(id={self.id}, status={self.status})>"


class AuditResult(Base):
    __tablename__ = "audit_results"

    id = Column(Integer, primary_key=True)
    audit_id = Column(String(255), ForeignKey("audits.id"), nullable=False)
    inspector_json = Column(JSON, nullable=True)
    analyst_json = Column(JSON, nullable=True)
    advisor_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    audit = relationship("Audit", back_populates="results")

    def __repr__(self):
        return f"<AuditResult(audit_id={self.audit_id})>"
