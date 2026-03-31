"""
Sawit Go - TSJ - Database Session Management
"""

import sys
sys.setrecursionlimit(10000)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
from pathlib import Path

from src.config.settings import Settings
from src.models.base import Base


class DatabaseSession:
    """Database session manager"""
    
    _engine = None
    _session_factory = None
    _initialized = False
    
    @classmethod
    def initialize(cls) -> None:
        """Initialize database connection"""
        if cls._initialized:
            return
        
        cls._initialized = True
        
        db_path = Settings.get_database_path()
        db_url = f"sqlite:///{db_path}"
        
        cls._engine = create_engine(
            db_url,
            echo=False,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        
        cls._session_factory = sessionmaker(
            bind=cls._engine,
            autoflush=False,
            autocommit=False,
        )
        
        cls._create_tables()
        cls._seed_default_data()
    
    @classmethod
    def _create_tables(cls) -> None:
        """Create all database tables"""
        Base.metadata.create_all(cls._engine)
    
    @classmethod
    def _seed_default_data(cls) -> None:
        """Seed default data if database is empty"""
        from src.models import Company, User
        import bcrypt
        
        session = cls._session_factory()
        try:
            company_count = session.query(Company).count()
            
            if company_count == 0:
                default_company = Company(
                    code="TSJ",
                    name="PT Tulas Sakti Jaya",
                    address="Indonesia",
                    fiscal_year_start=1,
                    currency_code="IDR",
                    decimal_places=2,
                    is_active=True,
                )
                session.add(default_company)
                session.flush()
                
                password_hash = bcrypt.hashpw(
                    "admin123".encode(),
                    bcrypt.gensalt()
                ).decode()
                
                admin_user = User(
                    company_id=default_company.id,
                    username="admin",
                    password_hash=password_hash,
                    full_name="Administrator",
                    email="admin@tsj.co.id",
                    role="ADMIN",
                    is_active=True,
                )
                session.add(admin_user)
                session.commit()
        finally:
            session.close()
    
    @classmethod
    def get_session(cls):
        """Get a new database session"""
        if not cls._initialized:
            cls.initialize()
        return cls._session_factory()
    
    @classmethod
    @contextmanager
    def session_scope(cls):
        """Provide a transactional scope for database operations"""
        session = cls.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    @classmethod
    def close(cls) -> None:
        """Close database connection"""
        if cls._engine:
            cls._engine.dispose()
            cls._initialized = False
