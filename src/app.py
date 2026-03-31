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
    
    def run_with_login(self):
        """Run app with login dialog"""
        from src.ui.login_dialog import LoginDialog
        from src.ui.main_window import MainWindow
        
        login = LoginDialog()
        if login.exec() == LoginDialog.DialogCode.Accepted:
            user_info = login.get_user_info()
            self.main_window = MainWindow(user_info)
            self.main_window.show()
            return self.exec()
        return 0
    
    def run(self):
        """Run the application - shows login first"""
        return self.run_with_login()
