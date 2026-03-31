"""
Sawit Go - TSJ - Financial Statement Models
FS Account and FS Element
"""

from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.company import Company
    from src.models.gl_account import GLAccount


class FSElement(BaseModel):
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
    
    company: Mapped["Company"] = relationship("Company")
    fs_accounts: Mapped[list["FSAccount"]] = relationship("FSAccount", back_populates="fs_element")
    
    def __repr__(self) -> str:
        return f"<FSElement(id={self.id}, code='{self.code}', name='{self.name}')>"


class FSAccount(BaseModel):
    """Financial Statement Account model"""
    
    __tablename__ = "fs_account"
    
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    fs_element_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("fs_element.id"), nullable=True)
    statement_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    company: Mapped["Company"] = relationship("Company")
    fs_element: Mapped[Optional["FSElement"]] = relationship("FSElement", back_populates="fs_accounts")
    gl_accounts: Mapped[list["GLAccount"]] = relationship("GLAccount", back_populates="fs_account")
    
    def __repr__(self) -> str:
        return f"<FSAccount(id={self.id}, code='{self.code}', name='{self.name}')>"
