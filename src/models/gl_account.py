"""
Sawit Go - TSJ - GL Account Model
General Ledger Chart of Accounts
"""

from sqlalchemy import String, Integer, ForeignKey, Boolean, DECIMAL, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from decimal import Decimal

from src.models.base import Base


class GLAccount(Base):
    """General Ledger Account model"""
    
    __tablename__ = "gl_account"
    
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("gl_account.id"), nullable=True)
    level: Mapped[int] = mapped_column(Integer, default=0)
    account_type: Mapped[str] = mapped_column(String(20), default="DETAIL")
    normal_balance: Mapped[str] = mapped_column(String(10), default="DEBIT")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    allow_entry: Mapped[bool] = mapped_column(Boolean, default=True)
    show_in_trial_balance: Mapped[bool] = mapped_column(Boolean, default=True)
    fs_account_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    initial_balance: Mapped[Decimal] = mapped_column(DECIMAL(18, 4), default=Decimal("0"))
    currency_code: Mapped[str] = mapped_column(String(3), default="IDR")
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<GLAccount(id={self.id}, code='{self.code}', name='{self.name}')>"
