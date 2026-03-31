"""
Sawit Go - TSJ - Subsidiary Ledger Account Model
"""

from sqlalchemy import String, Integer, ForeignKey, Boolean, DECIMAL, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
from decimal import Decimal

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.company import Company
    from src.models.gl_account import GLAccount


class SLAccount(BaseModel):
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
    
    company: Mapped["Company"] = relationship("Company")
    gl_account: Mapped["GLAccount"] = relationship("GLAccount")
    
    def __repr__(self) -> str:
        return f"<SLAccount(id={self.id}, code='{self.code}', name='{self.name}')>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "gl_account_id": self.gl_account_id,
            "code": self.code,
            "name": self.name,
            "contact_person": self.contact_person,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "tax_id": self.tax_id,
            "credit_limit": float(self.credit_limit) if self.credit_limit else None,
            "is_active": self.is_active,
        }
