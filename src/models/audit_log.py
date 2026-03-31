"""
Sawit Go - TSJ - Audit Log Model
"""

from sqlalchemy import String, Integer, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from src.models.base import Base


class AuditLog(Base):
    """Audit Log model for tracking changes"""
    
    __tablename__ = "audit_log"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    table_name: Mapped[str] = mapped_column(String(50), nullable=False)
    record_id: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[str] = mapped_column(String(20), nullable=False)
    old_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    new_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, table='{self.table_name}', action='{self.action}')>"
