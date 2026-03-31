"""
Sawit Go - TSJ - Application Class
Main PyQt6 Application
"""

import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from loguru import logger

from src.ui.main_window import MainWindow
from src.database.session import DatabaseSession
from src.config.settings import Settings


class SawitGoApp(QApplication):
    """Main application class"""
    
    def __init__(self):
        super().__init__(sys.argv)
        self.setApplicationName("Sawit Go - TSJ")
        self.setApplicationVersion("1.0.0")
        self.setOrganizationName("PT Tulas Sakti Jaya")
        
        self._setup_logging()
        self._init_database()
        self._create_main_window()
        
        logger.info("Sawit Go - TSJ started successfully")
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logger.remove()
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="DEBUG"
        )
        
        log_dir = Settings.get_log_dir()
        logger.add(
            log_dir / "sawitgo_{time}.log",
            rotation="10 MB",
            retention="7 days",
            level="DEBUG"
        )
    
    def _init_database(self):
        """Initialize database connection"""
        try:
            DatabaseSession.initialize()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            QMessageBox.critical(
                None,
                "Database Error",
                f"Failed to initialize database:\n{e}"
            )
            sys.exit(1)
    
    def _create_main_window(self):
        """Create and show main window"""
        self.main_window = MainWindow()
        self.main_window.show()
    
    def run(self):
        """Run the application"""
        return self.exec()
