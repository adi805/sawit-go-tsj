"""
Sawit Go - TSJ - Subsidiary Ledger Account Model
"""

from sqlalchemy import String, Integer, ForeignKey, Boolean, DECIMAL, Text, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from decimal import Decimal

from src.models.base import Base


class SLAccount(Base):
    """Subsidiary Ledger Account model"""
    
    __tablename__ = "sl_account"
    
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"), nullable=False)
    gl_account_id: Mapped[int] = mapped_column(Integer, ForeignKey("gl_account.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    contact_person: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tax_id: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    credit_limit: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(18, 4), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<SLAccount(id={self.id}, code='{self.code}')>"
