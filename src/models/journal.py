"""
Sawit Go - TSJ - Journal Models
Journal Header and Journal Line
"""

from sqlalchemy import String, Integer, ForeignKey, DECIMAL, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, date
from decimal import Decimal

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.company import Company
    from src.models.period import Period
    from src.models.user import User
    from src.models.gl_account import GLAccount


class JournalHeader(BaseModel):
    """Journal Header model"""
    
    __tablename__ = "journal_header"
    
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"), nullable=False)
    period_id: Mapped[int] = mapped_column(Integer, ForeignKey("period.id"), nullable=False)
    journal_no: Mapped[str] = mapped_column(String(20), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    reference: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="POSTED")
    source_type: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    source_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    
    company: Mapped["Company"] = relationship("Company", back_populates="journals")
    period: Mapped["Period"] = relationship("Period", back_populates="journals")
    creator: Mapped["User"] = relationship("User")
    lines: Mapped[list["JournalLine"]] = relationship("JournalLine", back_populates="header", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<JournalHeader(id={self.id}, no='{self.journal_no}', date={self.date})>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "period_id": self.period_id,
            "journal_no": self.journal_no,
            "date": self.date.isoformat() if self.date else None,
            "reference": self.reference,
            "description": self.description,
            "notes": self.notes,
            "status": self.status,
            "created_by": self.created_by,
        }
    
    @property
    def total_debit(self) -> Decimal:
        """Calculate total debit"""
        return sum(line.debit or Decimal("0") for line in self.lines)
    
    @property
    def total_credit(self) -> Decimal:
        """Calculate total credit"""
        return sum(line.credit or Decimal("0") for line in self.lines)
    
    @property
    def is_balanced(self) -> bool:
        """Check if journal is balanced"""
        return self.total_debit == self.total_credit


class JournalLine(BaseModel):
    """Journal Line model"""
    
    __tablename__ = "journal_line"
    
    header_id: Mapped[int] = mapped_column(Integer, ForeignKey("journal_header.id", ondelete="CASCADE"), nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("gl_account.id"), nullable=False)
    sl_account_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("sl_account.id"), nullable=True)
    debit: Mapped[Decimal] = mapped_column(DECIMAL(18, 4), default=Decimal("0"))
    credit: Mapped[Decimal] = mapped_column(DECIMAL(18, 4), default=Decimal("0"))
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    
    header: Mapped["JournalHeader"] = relationship("JournalHeader", back_populates="lines")
    account: Mapped["GLAccount"] = relationship("GLAccount")
    
    def __repr__(self) -> str:
        return f"<JournalLine(id={self.id}, account_id={self.account_id}, debit={self.debit}, credit={self.credit})>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "header_id": self.header_id,
            "account_id": self.account_id,
            "sl_account_id": self.sl_account_id,
            "debit": float(self.debit) if self.debit else 0,
            "credit": float(self.credit) if self.credit else 0,
            "description": self.description,
        }
