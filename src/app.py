"""
Sawit Go - TSJ - Application Class
Main PyQt6 Application
"""

import sys
sys.setrecursionlimit(10000)

from PyQt6.QtWidgets import QApplication, QMessageBox


class SawitGoApp(QApplication):
    """Main application class"""
    
    def __init__(self):
        super().__init__(sys.argv)
        self.setApplicationName("Sawit Go - TSJ")
        self.setApplicationVersion("1.0.0")
        self.setOrganizationName("PT Tulas Sakti Jaya")
        
        self._init_database()
        self._create_main_window()
    
    def _init_database(self):
        """Initialize database connection"""
        try:
            from src.database.session import DatabaseSession
            DatabaseSession.initialize()
        except Exception as e:
            QMessageBox.critical(
                None,
                "Database Error",
                f"Failed to initialize database:\n{e}"
            )
            sys.exit(1)
    
    def _create_main_window(self):
        """Create and show main window"""
        from src.ui.main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
    
    def run(self):
        """Run the application"""
        return self.exec()
