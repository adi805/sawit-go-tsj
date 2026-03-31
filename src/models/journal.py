"""
Sawit Go - TSJ - Journal Models
Journal Header and Journal Line
"""

from sqlalchemy import String, Integer, ForeignKey, DECIMAL, Date, Text, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from decimal import Decimal

from src.models.base import Base


class JournalHeader(Base):
    """Journal Header model"""
    
    __tablename__ = "journal_header"
    
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"), nullable=False)
    period_id: Mapped[int] = mapped_column(Integer, ForeignKey("period.id"), nullable=False)
    journal_no: Mapped[str] = mapped_column(String(20), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    reference: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="POSTED")
    source_type: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    source_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<JournalHeader(id={self.id}, no='{self.journal_no}')>"


class JournalLine(Base):
    """Journal Line model"""
    
    __tablename__ = "journal_line"
    
    header_id: Mapped[int] = mapped_column(Integer, ForeignKey("journal_header.id", ondelete="CASCADE"), nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("gl_account.id"), nullable=False)
    sl_account_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    debit: Mapped[Decimal] = mapped_column(DECIMAL(18, 4), default=Decimal("0"))
    credit: Mapped[Decimal] = mapped_column(DECIMAL(18, 4), default=Decimal("0"))
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<JournalLine(id={self.id}, account_id={self.account_id})>"
