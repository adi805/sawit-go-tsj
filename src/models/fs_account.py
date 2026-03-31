"""
Sawit Go - TSJ - Financial Statement Models
FS Account and FS Element
"""

from sqlalchemy import String, Integer, ForeignKey, Boolean, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from src.models.base import Base


class FSElement(Base):
    """Financial Statement Element model"""
    
    __tablename__ = "fs_element"
    
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(10), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    statement_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    position: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<FSElement(id={self.id}, code='{self.code}')>"


class FSAccount(Base):
    """Financial Statement Account model"""
    
    __tablename__ = "fs_account"
    
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    fs_element_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    statement_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<FSAccount(id={self.id}, code='{self.code}')>"
