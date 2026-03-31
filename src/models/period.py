"""
Sawit Go - TSJ - Period Model
Accounting Period Management
"""

from sqlalchemy import Integer, ForeignKey, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
from datetime import date

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.company import Company
    from src.models.user import User
    from src.models.journal import JournalHeader


class Period(BaseModel):
    """Accounting Period model"""
    
    __tablename__ = "period"
    
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False)
    closed_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    closed_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    company: Mapped["Company"] = relationship("Company", back_populates="periods")
    closed_by_user: Mapped[Optional["User"]] = relationship("User")
    journals: Mapped[list["JournalHeader"]] = relationship("JournalHeader", back_populates="period")
    
    def __repr__(self) -> str:
        return f"<Period(id={self.id}, year={self.year}, month={self.month}, closed={self.is_closed})>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "year": self.year,
            "month": self.month,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "is_closed": self.is_closed,
            "closed_by": self.closed_by,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
        }
    
    @property
    def period_name(self) -> str:
        """Get period name"""
        month_names = [
            "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]
        return f"{month_names[self.month]} {self.year}"
