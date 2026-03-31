"""
Sawit Go - TSJ - Audit Log Model
"""

from sqlalchemy import String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.company import Company
    from src.models.user import User


class AuditLog(BaseModel):
    """Audit Log model for tracking changes"""
    
    __tablename__ = "audit_log"
    
    company_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("company.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    table_name: Mapped[str] = mapped_column(String(50), nullable=False)
    record_id: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[str] = mapped_column(String(20), nullable=False)
    old_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    new_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    user: Mapped["User"] = relationship("User")
    
    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, table='{self.table_name}', action='{self.action}')>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "user_id": self.user_id,
            "table_name": self.table_name,
            "record_id": self.record_id,
            "action": self.action,
            "old_data": self.old_data,
            "new_data": self.new_data,
            "ip_address": self.ip_address,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }
