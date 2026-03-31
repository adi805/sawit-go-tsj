"""
Sawit Go - TSJ - Report Service
Generate Trial Balance and other accounting reports
"""

from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import date
from dataclasses import dataclass
from collections import defaultdict

from src.database.session import DatabaseSession


@dataclass
class TrialBalanceItem:
    """Single item in trial balance"""
    account_id: int
    account_code: str
    account_name: str
    normal_balance: str
    initial_balance: Decimal
    total_debit: Decimal
    total_credit: Decimal
    ending_balance: Decimal
    level: int = 0
    is_header: bool = False


@dataclass
class TrialBalanceReport:
    """Complete trial balance report"""
    company_name: str
    company_code: str
    period_name: str
    start_date: date
    end_date: date
    currency_code: str
    items: List[Dict[str, Any]]
    total_debit: Decimal
    total_credit: Decimal
    is_balanced: bool
    generated_at: str


@dataclass
class JournalBookReport:
    """Journal book report"""
    company_name: str
    period_name: str
    start_date: date
    end_date: date
    entries: List[Dict[str, Any]]
    total_debit: Decimal
    total_credit: Decimal


class ReportService:
    """Generate accounting reports"""

    def __init__(self):
        pass

    def generate_trial_balance(
        self,
        company_id: int,
        period_id: int,
        include_zero_balances: bool = False
    ) -> Optional[TrialBalanceReport]:
        """
        Generate trial balance report for a period.
        
        Args:
            company_id: Company ID
            period_id: Period ID
            include_zero_balances: Include accounts with zero balance
            
        Returns:
            TrialBalanceReport or None if period not found
        """
        from src.models import Company, Period, GLAccount, JournalHeader, JournalLine
        
        session = DatabaseSession.get_session()
        try:
            company = session.query(Company).filter(Company.id == company_id).first()
            period = session.query(Period).filter(Period.id == period_id).first()
            
            if not company or not period:
                return None
            
            accounts = session.query(GLAccount).filter(
                GLAccount.company_id == company_id,
                GLAccount.is_active == True,
                GLAccount.account_type == "DETAIL"
            ).order_by(GLAccount.code).all()
            
            items = []
            total_debit = Decimal("0")
            total_credit = Decimal("0")
            
            for account in accounts:
                if not account.show_in_trial_balance:
                    continue
                
                initial_balance = account.initial_balance or Decimal("0")
                
                journal_lines = session.query(JournalLine).join(
                    JournalHeader
                ).filter(
                    JournalLine.account_id == account.id,
                    JournalHeader.date <= period.end_date,
                    JournalHeader.status == "POSTED"
                ).all()
                
                period_debit = Decimal("0")
                period_credit = Decimal("0")
                
                for line in journal_lines:
                    period_debit += line.debit or Decimal("0")
                    period_credit += line.credit or Decimal("0")
                
                if account.normal_balance == "DEBIT":
                    ending_balance = initial_balance + period_debit - period_credit
                else:
                    ending_balance = initial_balance + period_credit - period_debit
                
                if not include_zero_balances and ending_balance == Decimal("0"):
                    continue
                
                items.append({
                    "account_id": account.id,
                    "account_code": account.code,
                    "account_name": account.name,
                    "normal_balance": account.normal_balance,
                    "initial_balance": initial_balance,
                    "total_debit": period_debit,
                    "total_credit": period_credit,
                    "ending_balance": ending_balance,
                    "level": account.level,
                    "is_header": account.account_type == "HEADER"
                })
                
                if ending_balance >= Decimal("0"):
                    total_debit += ending_balance
                else:
                    total_credit += abs(ending_balance)
            
            period_name = f"{period.year}-{period.month:02d}"
            
            return TrialBalanceReport(
                company_name=company.name,
                company_code=company.code,
                period_name=period_name,
                start_date=period.start_date,
                end_date=period.end_date,
                currency_code=company.currency_code,
                items=items,
                total_debit=total_debit,
                total_credit=total_credit,
                is_balanced=total_debit == total_credit,
                generated_at=""
            )
            
        finally:
            session.close()

    def generate_trial_balance_summary(
        self,
        company_id: int,
        period_id: int
    ) -> Dict[str, Any]:
        """
        Generate a summary of trial balance.
        
        Returns:
            Dictionary with totals
        """
        from src.models import Company, Period, GLAccount, JournalHeader, JournalLine
        
        session = DatabaseSession.get_session()
        try:
            company = session.query(Company).filter(Company.id == company_id).first()
            period = session.query(Period).filter(Period.id == period_id).first()
            
            if not company or not period:
                return {}
            
            accounts = session.query(GLAccount).filter(
                GLAccount.company_id == company_id,
                GLAccount.is_active == True,
                GLAccount.account_type == "DETAIL",
                GLAccount.show_in_trial_balance == True
            ).all()
            
            total_assets = Decimal("0")
            total_liabilities = Decimal("0")
            total_equity = Decimal("0")
            total_revenue = Decimal("0")
            total_expenses = Decimal("0")
            
            asset_codes = ["1"]
            liability_codes = ["2"]
            equity_codes = ["3"]
            revenue_codes = ["4"]
            expense_codes = ["5", "6", "7", "8", "9"]
            
            for account in accounts:
                initial_balance = account.initial_balance or Decimal("0")
                
                journal_lines = session.query(JournalLine).join(
                    JournalHeader
                ).filter(
                    JournalLine.account_id == account.id,
                    JournalHeader.date <= period.end_date,
                    JournalHeader.status == "POSTED"
                ).all()
                
                period_debit = sum(line.debit or Decimal("0") for line in journal_lines)
                period_credit = sum(line.credit or Decimal("0") for line in journal_lines)
                
                if account.normal_balance == "DEBIT":
                    balance = initial_balance + period_debit - period_credit
                else:
                    balance = initial_balance + period_credit - period_debit
                
                code_prefix = account.code.split("-")[0] if "-" in account.code else account.code[0]
                
                if code_prefix in asset_codes:
                    total_assets += balance
                elif code_prefix in liability_codes:
                    total_liabilities += balance
                elif code_prefix in equity_codes:
                    total_equity += balance
                elif code_prefix in revenue_codes:
                    total_revenue += balance
                elif code_prefix in expense_codes:
                    total_expenses += balance
            
            return {
                "company_name": company.name,
                "period_name": f"{period.year}-{period.month:02d}",
                "total_assets": float(total_assets),
                "total_liabilities": float(total_liabilities),
                "total_equity": float(total_equity),
                "total_revenue": float(total_revenue),
                "total_expenses": float(total_expenses),
                "net_income": float(total_revenue - total_expenses),
                "accounting_equation_balanced": (
                    abs((total_liabilities + total_equity + total_revenue - total_expenses) - total_assets) < Decimal("0.01")
                )
            }
            
        finally:
            session.close()

    def generate_journal_book(
        self,
        company_id: int,
        start_date: date,
        end_date: date,
        period_id: Optional[int] = None
    ) -> Optional[JournalBookReport]:
        """
        Generate journal book report for a date range.
        
        Args:
            company_id: Company ID
            start_date: Start date
            end_date: End date
            period_id: Optional period filter
            
        Returns:
            JournalBookReport or None
        """
        from src.models import Company, Period, JournalHeader, JournalLine, GLAccount
        
        session = DatabaseSession.get_session()
        try:
            company = session.query(Company).filter(Company.id == company_id).first()
            
            if not company:
                return None
            
            query = session.query(JournalHeader).filter(
                JournalHeader.company_id == company_id,
                JournalHeader.date >= start_date,
                JournalHeader.date <= end_date,
                JournalHeader.status == "POSTED"
            )
            
            if period_id:
                query = query.filter(JournalHeader.period_id == period_id)
            
            headers = query.order_by(JournalHeader.date, JournalHeader.id).all()
            
            entries = []
            total_debit = Decimal("0")
            total_credit = Decimal("0")
            
            for header in headers:
                lines = session.query(JournalLine).filter(
                    JournalLine.header_id == header.id
                ).all()
                
                header_total_debit = Decimal("0")
                header_total_credit = Decimal("0")
                
                line_items = []
                for line in lines:
                    debit = line.debit or Decimal("0")
                    credit = line.credit or Decimal("0")
                    
                    header_total_debit += debit
                    header_total_credit += credit
                    
                    account = session.query(GLAccount).filter(
                        GLAccount.id == line.account_id
                    ).first()
                    
                    line_items.append({
                        "line_id": line.id,
                        "account_code": account.code if account else "",
                        "account_name": account.name if account else "",
                        "description": line.description or "",
                        "debit": float(debit),
                        "credit": float(credit)
                    })
                
                entries.append({
                    "journal_no": header.journal_no,
                    "date": header.date.isoformat() if header.date else "",
                    "reference": header.reference,
                    "description": header.description,
                    "lines": line_items,
                    "total_debit": float(header_total_debit),
                    "total_credit": float(header_total_credit)
                })
                
                total_debit += header_total_debit
                total_credit += header_total_credit
            
            period_name = "All Periods"
            if period_id:
                period = session.query(Period).filter(Period.id == period_id).first()
                if period:
                    period_name = f"{period.year}-{period.month:02d}"
            
            return JournalBookReport(
                company_name=company.name,
                period_name=period_name,
                start_date=start_date,
                end_date=end_date,
                entries=entries,
                total_debit=total_debit,
                total_credit=total_credit
            )
            
        finally:
            session.close()

    def get_period_list(self, company_id: int) -> List[Dict[str, Any]]:
        """Get all periods for a company"""
        from src.models import Period
        
        session = DatabaseSession.get_session()
        try:
            periods = session.query(Period).filter(
                Period.company_id == company_id
            ).order_by(Period.year.desc(), Period.month.desc()).all()
            
            return [
                {
                    "id": p.id,
                    "year": p.year,
                    "month": p.month,
                    "period_name": f"{p.year}-{p.month:02d}",
                    "start_date": p.start_date.isoformat() if p.start_date else "",
                    "end_date": p.end_date.isoformat() if p.end_date else "",
                    "is_closed": p.is_closed
                }
                for p in periods
            ]
            
        finally:
            session.close()

    def create_period(
        self,
        company_id: int,
        year: int,
        month: int
    ) -> Optional[int]:
        """Create a new accounting period"""
        from src.models import Period
        from datetime import date, timedelta
        import calendar
        
        session = DatabaseSession.get_session()
        try:
            existing = session.query(Period).filter(
                Period.company_id == company_id,
                Period.year == year,
                Period.month == month
            ).first()
            
            if existing:
                return existing.id
            
            start_day = 1
            _, last_day = calendar.monthrange(year, month)
            end_day = last_day
            
            start_date = date(year, month, start_day)
            end_date = date(year, month, end_day)
            
            period = Period(
                company_id=company_id,
                year=year,
                month=month,
                start_date=start_date,
                end_date=end_date,
                is_closed=False
            )
            session.add(period)
            session.commit()
            
            return period.id
            
        except Exception:
            session.rollback()
            return None
        finally:
            session.close()

    def close_period(self, period_id: int, closed_by: int) -> Tuple[bool, str]:
        """Close a period"""
        from src.models import Period
        
        session = DatabaseSession.get_session()
        try:
            period = session.query(Period).filter(Period.id == period_id).first()
            
            if not period:
                return False, "Period tidak ditemukan"
            
            if period.is_closed:
                return False, "Period sudah ditutup"
            
            period.is_closed = True
            period.closed_by = closed_by
            from datetime import date
            period.closed_at = date.today()
            
            session.commit()
            return True, f"Period {period.year}-{period.month:02d} berhasil ditutup"
            
        except Exception as e:
            session.rollback()
            return False, f"Error: {str(e)}"
        finally:
            session.close()


report_service = ReportService()
