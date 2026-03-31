"""
Sawit Go - TSJ - Application Settings Model
"""

from sqlalchemy import String, Integer, ForeignKey, Text, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from src.models.base import Base


class AppSettings(Base):
    """Application Settings model (key-value store)"""
    
    __tablename__ = "app_settings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"), nullable=False)
    setting_key: Mapped[str] = mapped_column(String(100), nullable=False)
    setting_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<AppSettings(key='{self.setting_key}')>"
