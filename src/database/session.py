"""
Sawit Go - TSJ - Database Session Management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
from loguru import logger
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
        
        db_path = Settings.get_database_path()
        db_url = f"sqlite:///{db_path}"
        
        logger.info(f"Initializing database at: {db_path}")
        
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
        
        cls._initialized = True
        logger.info("Database initialized successfully")
    
    @classmethod
    def _create_tables(cls) -> None:
        """Create all database tables"""
        logger.info("Creating database tables...")
        Base.metadata.create_all(cls._engine)
        logger.info("Database tables created")
    
    @classmethod
    def _seed_default_data(cls) -> None:
        """Seed default data if database is empty"""
        from src.models import Company, User
        import bcrypt
        
        with cls.get_session() as session:
            company_count = session.query(Company).count()
            
            if company_count == 0:
                logger.info("Seeding default company and user...")
                
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
                
                logger.info("Default data seeded successfully")
    
    @classmethod
    def get_session(cls) -> Session:
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
        except Exception as e:
            session.rollback()
            logger.error(f"Database transaction failed: {e}")
            raise
        finally:
            session.close()
    
    @classmethod
    def close(cls) -> None:
        """Close database connection"""
        if cls._engine:
            cls._engine.dispose()
            cls._initialized = False
            logger.info("Database connection closed")
