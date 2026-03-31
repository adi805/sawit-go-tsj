"""
Sawit Go - TSJ - Authentication Service
"""

import bcrypt
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass

from src.database.session import DatabaseSession


@dataclass
class LoginResult:
    success: bool
    user_id: Optional[int] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    company_id: Optional[int] = None
    message: str = ""


class AuthService:
    """Handle user authentication"""
    
    def __init__(self):
        self.current_user: Optional[Dict[str, Any]] = None
    
    def login(self, username: str, password: str) -> LoginResult:
        """
        Authenticate user with username and password.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            LoginResult with success status and user info
        """
        from src.models import User, Company
        
        session = DatabaseSession.get_session()
        try:
            user = session.query(User).filter(
                User.username == username,
                User.is_active == True
            ).first()
            
            if not user:
                return LoginResult(
                    success=False,
                    message="Username tidak ditemukan"
                )
            
            if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
                return LoginResult(
                    success=False,
                    message="Password salah"
                )
            
            user.last_login = datetime.now()
            session.commit()
            
            company = session.query(Company).filter(
                Company.id == user.company_id
            ).first()
            
            self.current_user = {
                "user_id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "role": user.role,
                "company_id": user.company_id,
                "company_name": company.name if company else "Unknown"
            }
            
            return LoginResult(
                success=True,
                user_id=user.id,
                username=user.username,
                full_name=user.full_name,
                role=user.role,
                company_id=user.company_id,
                message="Login berhasil"
            )
            
        except Exception as e:
            session.rollback()
            return LoginResult(
                success=False,
                message=f"Error: {str(e)}"
            )
        finally:
            session.close()
    
    def logout(self) -> bool:
        """Logout current user"""
        self.current_user = None
        return True
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current logged in user"""
        return self.current_user
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.current_user is not None
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """
        Change user password.
        
        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password
            
        Returns:
            True if successful
        """
        from src.models import User
        
        session = DatabaseSession.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                return False
            
            if not bcrypt.checkpw(old_password.encode(), user.password_hash.encode()):
                return False
            
            user.password_hash = bcrypt.hashpw(
                new_password.encode(),
                bcrypt.gensalt()
            ).decode()
            session.commit()
            return True
            
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()


auth_service = AuthService()
