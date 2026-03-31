"""
Sawit Go - TSJ - GL Account Model
General Ledger Chart of Accounts
"""

from sqlalchemy import String, Integer, ForeignKey, Boolean, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
from decimal import Decimal

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.company import Company
    from src.models.fs_account import FSAccount


class GLAccount(BaseModel):
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
    fs_account_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("fs_account.id"), nullable=True)
    initial_balance: Mapped[Decimal] = mapped_column(DECIMAL(18, 4), default=Decimal("0"))
    currency_code: Mapped[str] = mapped_column(String(3), default="IDR")
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    company: Mapped["Company"] = relationship("Company", back_populates="gl_accounts")
    parent: Mapped[Optional["GLAccount"]] = relationship("GLAccount", remote_side="GLAccount.id", back_populates="children")
    children: Mapped[list["GLAccount"]] = relationship("GLAccount", back_populates="parent")
    fs_account: Mapped[Optional["FSAccount"]] = relationship("FSAccount", back_populates="gl_accounts")
    
    def __repr__(self) -> str:
        return f"<GLAccount(id={self.id}, code='{self.code}', name='{self.name}')>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "code": self.code,
            "name": self.name,
            "parent_id": self.parent_id,
            "level": self.level,
            "account_type": self.account_type,
            "normal_balance": self.normal_balance,
            "is_active": self.is_active,
            "allow_entry": self.allow_entry,
            "show_in_trial_balance": self.show_in_trial_balance,
            "fs_account_id": self.fs_account_id,
            "initial_balance": float(self.initial_balance) if self.initial_balance else 0,
        }
    
    @property
    def is_header(self) -> bool:
        """Check if account is a header (parent) account"""
        return self.account_type == "HEADER"
    
    @property
    def is_detail(self) -> bool:
        """Check if account is a detail account"""
        return self.account_type == "DETAIL"
