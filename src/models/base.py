"""
Sawit Go - TSJ - Base Model
SQLAlchemy base model configuration
"""

from datetime import datetime
from sqlalchemy import Integer, DateTime, Boolean, func
from sqlalchemy.orm import DeclarativeBase
from typing import Optional


class Base(DeclarativeBase):
    """Base class for all database models"""
    pass
