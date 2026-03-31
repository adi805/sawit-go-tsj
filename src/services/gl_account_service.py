"""
Sawit Go - TSJ - GL Account Service
"""

from typing import List, Optional, Dict, Any
from decimal import Decimal

from src.database.session import DatabaseSession


class GLAccountService:
    """Handle GL Account operations"""
    
    def get_all(self, company_id: int, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Get all GL accounts for a company"""
        from src.models import GLAccount
        
        session = DatabaseSession.get_session()
        try:
            query = session.query(GLAccount).filter(GLAccount.company_id == company_id)
            if not include_inactive:
                query = query.filter(GLAccount.is_active == True)
            
            accounts = query.order_by(GLAccount.code).all()
            return [acc.to_dict() for acc in accounts]
        finally:
            session.close()
    
    def get_by_id(self, account_id: int) -> Optional[Dict[str, Any]]:
        """Get account by ID"""
        from src.models import GLAccount
        
        session = DatabaseSession.get_session()
        try:
            account = session.query(GLAccount).filter(GLAccount.id == account_id).first()
            return account.to_dict() if account else None
        finally:
            session.close()
    
    def create(self, company_id: int, code: str, name: str, **kwargs) -> Optional[int]:
        """Create new GL account"""
        from src.models import GLAccount
        
        session = DatabaseSession.get_session()
        try:
            account = GLAccount(
                company_id=company_id,
                code=code,
                name=name,
                **kwargs
            )
            session.add(account)
            session.commit()
            return account.id
        except Exception:
            session.rollback()
            return None
        finally:
            session.close()
    
    def update(self, account_id: int, **kwargs) -> bool:
        """Update GL account"""
        from src.models import GLAccount
        
        session = DatabaseSession.get_session()
        try:
            account = session.query(GLAccount).filter(GLAccount.id == account_id).first()
            if not account:
                return False
            
            for key, value in kwargs.items():
                if hasattr(account, key):
                    setattr(account, key, value)
            
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def delete(self, account_id: int) -> bool:
        """Delete GL account (soft delete)"""
        return self.update(account_id, is_active=False)
    
    def get_account_tree(self, company_id: int) -> List[Dict[str, Any]]:
        """Get accounts in tree structure"""
        from src.models import GLAccount
        
        session = DatabaseSession.get_session()
        try:
            accounts = session.query(GLAccount).filter(
                GLAccount.company_id == company_id,
                GLAccount.is_active == True
            ).order_by(GLAccount.code).all()
            
            tree = []
            for acc in accounts:
                acc_dict = acc.to_dict()
                acc_dict['children'] = []
                tree.append(acc_dict)
            
            return tree
        finally:
            session.close()
    
    def get_balance(self, account_id: int) -> Decimal:
        """Calculate account balance"""
        from src.models import GLAccount, JournalLine, JournalHeader
        
        session = DatabaseSession.get_session()
        try:
            account = session.query(GLAccount).filter(
                GLAccount.id == account_id
            ).first()
            
            if not account:
                return Decimal("0")
            
            balance = account.initial_balance or Decimal("0")
            
            result = session.query(
                JournalLine
            ).join(
                JournalHeader
            ).filter(
                JournalLine.account_id == account_id
            ).all()
            
            for line in result:
                balance += (line.debit or Decimal("0")) - (line.credit or Decimal("0"))
            
            return balance
        finally:
            session.close()
    
    def to_dict(self, account) -> Dict[str, Any]:
        """Convert account to dict"""
        return {
            "id": account.id,
            "company_id": account.company_id,
            "code": account.code,
            "name": account.name,
            "parent_id": account.parent_id,
            "level": account.level,
            "account_type": account.account_type,
            "normal_balance": account.normal_balance,
            "is_active": account.is_active,
            "allow_entry": account.allow_entry,
            "show_in_trial_balance": account.show_in_trial_balance,
            "initial_balance": float(account.initial_balance) if account.initial_balance else 0,
        }


gl_account_service = GLAccountService()
