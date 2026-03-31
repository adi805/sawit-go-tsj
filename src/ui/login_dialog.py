"""
Sawit Go - TSJ - Login Dialog
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QCheckBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class LoginDialog(QDialog):
    """Login dialog for user authentication"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login - Sawit Go - TSJ")
        self.setModal(True)
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #0078d7;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)
        
        title = QLabel("SAWIT GO - TSJ")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Sistem Akuntansi Perkebunan")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        username_label = QLabel("Username")
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Masukkan username")
        self.username_input.setText("admin")
        layout.addWidget(self.username_input)
        
        password_label = QLabel("Password")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Masukkan password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setText("admin123")
        self.password_input.returnPressed.connect(self._on_login)
        layout.addWidget(self.password_input)
        
        self.remember_checkbox = QCheckBox("Ingat saya")
        layout.addWidget(self.remember_checkbox)
        
        layout.addSpacing(10)
        
        self.login_button = QPushButton("LOGIN")
        self.login_button.clicked.connect(self._on_login)
        self.login_button.setFixedHeight(45)
        layout.addWidget(self.login_button)
        
        self.cancel_button = QPushButton("BATAL")
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        layout.addWidget(self.cancel_button)
        
        layout.addStretch()
        
        version = QLabel("Version 1.0.0-alpha")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version.setStyleSheet("color: #999; font-size: 10px;")
        layout.addWidget(version)
    
    def _on_login(self):
        """Handle login button click"""
        from src.services.auth_service import auth_service
        
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username:
            QMessageBox.warning(self, "Error", "Username tidak boleh kosong")
            return
        
        if not password:
            QMessageBox.warning(self, "Error", "Password tidak boleh kosong")
            return
        
        result = auth_service.login(username, password)
        
        if result.success:
            self.accept()
        else:
            QMessageBox.critical(self, "Login Gagal", result.message)
    
    def get_user_info(self):
        """Get logged in user info"""
        from src.services.auth_service import auth_service
        return auth_service.get_current_user()
