"""
Sawit Go - TSJ - Period Model
Accounting Period Management
"""

from sqlalchemy import Integer, ForeignKey, Boolean, Date, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from src.models.base import Base


class Period(Base):
    """Accounting Period model"""
    
    __tablename__ = "period"
    
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False)
    closed_by: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    closed_at: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<Period(id={self.id}, year={self.year}, month={self.month})>"
