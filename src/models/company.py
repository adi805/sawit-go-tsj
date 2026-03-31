"""
Sawit Go - TSJ - Company Model
"""

from sqlalchemy import String, Integer, Boolean, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.gl_account import GLAccount
    from src.models.period import Period
    from src.models.journal import JournalHeader


class Company(Base):
    """Company model for multi-company support"""
    
    __tablename__ = "company"
    
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    npwp: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    fiscal_year_start: Mapped[int] = mapped_column(Integer, default=1)
    currency_code: Mapped[str] = mapped_column(String(3), default="IDR")
    decimal_places: Mapped[int] = mapped_column(Integer, default=2)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    users: Mapped[list["User"]] = relationship("User", back_populates="company")
    gl_accounts: Mapped[list["GLAccount"]] = relationship("GLAccount", back_populates="company")
    periods: Mapped[list["Period"]] = relationship("Period", back_populates="company")
    journals: Mapped[list["JournalHeader"]] = relationship("JournalHeader", back_populates="company")
    
    def __repr__(self) -> str:
        return f"<Company(id={self.id}, code='{self.code}', name='{self.name}')>"
