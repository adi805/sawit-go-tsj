"""
Sawit Go - TSJ - Application Settings Model
"""

from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.company import Company


class Settings(BaseModel):
    """Application Settings model (key-value store)"""
    
    __tablename__ = "app_settings"
    
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"), nullable=False)
    setting_key: Mapped[str] = mapped_column(String(100), nullable=False)
    setting_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    company: Mapped["Company"] = relationship("Company")
    
    def __repr__(self) -> str:
        return f"<Settings(key='{self.setting_key}', value='{self.setting_value}')>"
    
    @property
    def value(self) -> Optional[str]:
        """Get setting value"""
        return self.setting_value
    
    @value.setter
    def value(self, val: str):
        """Set setting value"""
        self.setting_value = val
