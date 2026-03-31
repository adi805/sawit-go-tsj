"""
Sawit Go - TSJ - Settings
Application settings and configuration
"""

from pathlib import Path
import json


class Settings:
    """Application settings"""
    
    APP_NAME = "Sawit Go - TSJ"
    APP_VERSION = "1.0.0"
    APP_AUTHOR = "Syafriadi"
    APP_COMPANY = "PT Tulas Sakti Jaya"
    
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOG_DIR = BASE_DIR / "logs"
    CONFIG_DIR = BASE_DIR / "config"
    RESOURCES_DIR = BASE_DIR / "resources"
    
    DATABASE_FILE = DATA_DIR / "gl.db"
    
    DATE_FORMAT = "%d/%m/%Y"
    DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
    DECIMAL_PLACES = 2
    THOUSAND_SEPARATOR = "."
    DECIMAL_SEPARATOR = ","
    CURRENCY_SYMBOL = "Rp"
    
    SESSION_TIMEOUT = 24 * 60 * 60
    
    @classmethod
    def get_log_dir(cls) -> Path:
        """Get or create log directory"""
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)
        return cls.LOG_DIR
    
    @classmethod
    def get_data_dir(cls) -> Path:
        """Get or create data directory"""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        return cls.DATA_DIR
    
    @classmethod
    def get_database_path(cls) -> Path:
        """Get database path"""
        cls.get_data_dir()
        return cls.DATABASE_FILE
    
    @classmethod
    def format_currency(cls, amount: float) -> str:
        """Format amount as currency"""
        formatted = f"{amount:,.{cls.DECIMAL_PLACES}f}"
        formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{cls.CURRENCY_SYMBOL} {formatted}"
    
    @classmethod
    def parse_currency(cls, value: str) -> float:
        """Parse currency string to float"""
        cleaned = value.replace(cls.CURRENCY_SYMBOL, "").strip()
        cleaned = cleaned.replace(cls.THOUSAND_SEPARATOR, "").replace(cls.DECIMAL_SEPARATOR, ".")
        return float(cleaned)
