"""
Sawit Go - TSJ - Journal Service
Journal CRUD operations with debit=credit validation
"""

from typing import List, Optional, Dict, Any, Tuple
from decimal import Decimal
from datetime import date, datetime
from dataclasses import dataclass

from src.database.session import DatabaseSession


@dataclass
class JournalValidationError:
    """Journal validation error details"""
    field: str
    message: str


@dataclass
class JournalValidationResult:
    """Journal validation result"""
    is_valid: bool
    errors: List[JournalValidationError]
    total_debit: Decimal = Decimal("0")
    total_credit: Decimal = Decimal("0")


@dataclass
class JournalCreateResult:
    """Journal creation result"""
    success: bool
    journal_id: Optional[int] = None
    journal_no: Optional[str] = None
    message: str = ""
    validation_errors: Optional[JournalValidationResult] = None


class JournalService:
    """Handle journal entry operations"""

    def __init__(self):
        pass

    def _validate_journal(
        self,
        lines: List[Dict[str, Any]]
    ) -> JournalValidationResult:
        """
        Validate journal entry - debit must equal credit.
        
        Args:
            lines: List of journal line dictionaries
            
        Returns:
            JournalValidationResult with validation status
        """
        errors: List[JournalValidationError] = []
        total_debit = Decimal("0")
        total_credit = Decimal("0")

        if not lines or len(lines) < 2:
            errors.append(JournalValidationError(
                field="lines",
                message="Minimal harus ada 2 baris jurnal"
            ))
            return JournalValidationResult(
                is_valid=False,
                errors=errors,
                total_debit=Decimal("0"),
                total_credit=Decimal("0")
            )

        for idx, line in enumerate(lines):
            debit = line.get('debit', Decimal("0")) or Decimal("0")
            credit = line.get('credit', Decimal("0")) or Decimal("0")

            if debit and credit:
                errors.append(JournalValidationError(
                    field=f"line_{idx}",
                    message=f"Baris {idx + 1}: Tidak boleh mengisi debit dan credit sekaligus"
                ))

            if not debit and not credit:
                errors.append(JournalValidationError(
                    field=f"line_{idx}",
                    message=f"Baris {idx + 1}: Harus mengisi debit atau credit"
                ))

            if 'account_id' not in line or not line['account_id']:
                errors.append(JournalValidationError(
                    field=f"line_{idx}",
                    message=f"Baris {idx + 1}: Akun harus dipilih"
                ))

            total_debit += debit
            total_credit += credit

        if total_debit != total_credit:
            errors.append(JournalValidationError(
                field="balance",
                message=f"Total debit ({total_debit:,.4f}) tidak sama dengan total credit ({total_credit:,.4f})"
            ))

        return JournalValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            total_debit=total_debit,
            total_credit=total_credit
        )

    def _generate_journal_no(
        self,
        session,
        company_id: int,
        period_id: int
    ) -> str:
        """Generate next journal number"""
        from src.models import JournalHeader
        
        prefix = datetime.now().strftime("%Y%m")
        
        last_journal = session.query(JournalHeader).filter(
            JournalHeader.company_id == company_id,
            JournalHeader.period_id == period_id
        ).order_by(JournalHeader.id.desc()).first()
        
        if last_journal and last_journal.journal_no:
            try:
                last_num = int(last_journal.journal_no.split("-")[-1])
                next_num = last_num + 1
            except (ValueError, IndexError):
                next_num = 1
        else:
            next_num = 1
        
        return f"JV-{prefix}-{next_num:04d}"

    def create_journal(
        self,
        company_id: int,
        period_id: int,
        journal_date: date,
        description: str,
        lines: List[Dict[str, Any]],
        reference: Optional[str] = None,
        notes: Optional[str] = None,
        created_by: int = 1,
        source_type: Optional[str] = None,
        source_id: Optional[int] = None
    ) -> JournalCreateResult:
        """
        Create a new journal entry with validation.
        
        Args:
            company_id: Company ID
            period_id: Period ID
            journal_date: Journal date
            description: Journal description
            lines: List of journal lines [{account_id, debit, credit, description}]
            reference: Optional reference number
            notes: Optional notes
            created_by: User ID who created
            source_type: Optional source type (e.g., 'INVOICE', 'RECEIPT')
            source_id: Optional source document ID
            
        Returns:
            JournalCreateResult with creation status
        """
        from src.models import JournalHeader, JournalLine, Period
        
        validation = self._validate_journal(lines)
        if not validation.is_valid:
            return JournalCreateResult(
                success=False,
                message="Validasi gagal",
                validation_errors=validation
            )
        
        session = DatabaseSession.get_session()
        try:
            period = session.query(Period).filter(Period.id == period_id).first()
            if not period:
                return JournalCreateResult(success=False, message="Period tidak ditemukan")
            
            if period.is_closed:
                return JournalCreateResult(success=False, message="Period sudah ditutup")
            
            if journal_date < period.start_date or journal_date > period.end_date:
                return JournalCreateResult(
                    success=False,
                    message=f"Tanggal harus dalam range period ({period.start_date} - {period.end_date})"
                )
            
            journal_no = self._generate_journal_no(session, company_id, period_id)
            
            header = JournalHeader(
                company_id=company_id,
                period_id=period_id,
                journal_no=journal_no,
                date=journal_date,
                reference=reference,
                description=description,
                notes=notes,
                status="POSTED",
                source_type=source_type,
                source_id=source_id,
                created_by=created_by
            )
            session.add(header)
            session.flush()
            
            for line_data in lines:
                line = JournalLine(
                    header_id=header.id,
                    account_id=line_data['account_id'],
                    sl_account_id=line_data.get('sl_account_id'),
                    debit=line_data.get('debit', Decimal("0")),
                    credit=line_data.get('credit', Decimal("0")),
                    description=line_data.get('description')
                )
                session.add(line)
            
            session.commit()
            
            return JournalCreateResult(
                success=True,
                journal_id=header.id,
                journal_no=journal_no,
                message=f"Jurnal {journal_no} berhasil dibuat"
            )
            
        except Exception as e:
            session.rollback()
            return JournalCreateResult(success=False, message=f"Error: {str(e)}")
        finally:
            session.close()

    def get_journal(self, journal_id: int) -> Optional[Dict[str, Any]]:
        """Get journal header with lines"""
        from src.models import JournalHeader, JournalLine, GLAccount, User
        
        session = DatabaseSession.get_session()
        try:
            header = session.query(JournalHeader).filter(
                JournalHeader.id == journal_id
            ).first()
            
            if not header:
                return None
            
            lines = session.query(JournalLine).filter(
                JournalLine.header_id == journal_id
            ).all()
            
            creator = session.query(User).filter(User.id == header.created_by).first()
            
            result = {
                "id": header.id,
                "company_id": header.company_id,
                "period_id": header.period_id,
                "journal_no": header.journal_no,
                "date": header.date.isoformat() if header.date else None,
                "reference": header.reference,
                "description": header.description,
                "notes": header.notes,
                "status": header.status,
                "source_type": header.source_type,
                "source_id": header.source_id,
                "created_by": header.created_by,
                "created_by_name": creator.full_name if creator else None,
                "created_at": header.created_at.isoformat() if header.created_at else None,
                "lines": []
            }
            
            for line in lines:
                account = session.query(GLAccount).filter(
                    GLAccount.id == line.account_id
                ).first()
                
                result["lines"].append({
                    "id": line.id,
                    "account_id": line.account_id,
                    "account_code": account.code if account else None,
                    "account_name": account.name if account else None,
                    "sl_account_id": line.sl_account_id,
                    "debit": float(line.debit) if line.debit else 0,
                    "credit": float(line.credit) if line.credit else 0,
                    "description": line.description
                })
            
            return result
            
        finally:
            session.close()

    def get_journals(
        self,
        company_id: int,
        period_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get list of journals with optional filters"""
        from src.models import JournalHeader
        
        session = DatabaseSession.get_session()
        try:
            query = session.query(JournalHeader).filter(
                JournalHeader.company_id == company_id
            )
            
            if period_id:
                query = query.filter(JournalHeader.period_id == period_id)
            
            if start_date:
                query = query.filter(JournalHeader.date >= start_date)
            
            if end_date:
                query = query.filter(JournalHeader.date <= end_date)
            
            if status:
                query = query.filter(JournalHeader.status == status)
            
            journals = query.order_by(JournalHeader.date.desc(), JournalHeader.id.desc()).all()
            
            result = []
            for j in journals:
                result.append({
                    "id": j.id,
                    "journal_no": j.journal_no,
                    "date": j.date.isoformat() if j.date else None,
                    "reference": j.reference,
                    "description": j.description,
                    "status": j.status,
                    "created_at": j.created_at.isoformat() if j.created_at else None
                })
            
            return result
            
        finally:
            session.close()

    def update_journal(
        self,
        journal_id: int,
        journal_date: Optional[date] = None,
        description: Optional[str] = None,
        reference: Optional[str] = None,
        notes: Optional[str] = None,
        lines: Optional[List[Dict[str, Any]]] = None
    ) -> Tuple[bool, str]:
        """Update existing journal"""
        from src.models import JournalHeader, JournalLine, Period
        
        session = DatabaseSession.get_session()
        try:
            header = session.query(JournalHeader).filter(
                JournalHeader.id == journal_id
            ).first()
            
            if not header:
                return False, "Jurnal tidak ditemukan"
            
            if header.status == "POSTED" and lines is not None:
                return False, "Tidak bisa mengubah jurnal yang sudah diposting"
            
            if journal_date:
                period = session.query(Period).filter(
                    Period.id == header.period_id
                ).first()
                
                if period and period.is_closed:
                    return False, "Period sudah ditutup"
                
                if period and (journal_date < period.start_date or journal_date > period.end_date):
                    return False, f"Tanggal harus dalam range period"
                
                header.date = journal_date
            
            if description is not None:
                header.description = description
            
            if reference is not None:
                header.reference = reference
            
            if notes is not None:
                header.notes = notes
            
            if lines is not None:
                validation = self._validate_journal(lines)
                if not validation.is_valid:
                    return False, "Validasi gagal: " + "; ".join(
                        [e.message for e in validation.errors]
                    )
                
                session.query(JournalLine).filter(
                    JournalLine.header_id == journal_id
                ).delete()
                
                for line_data in lines:
                    line = JournalLine(
                        header_id=header.id,
                        account_id=line_data['account_id'],
                        sl_account_id=line_data.get('sl_account_id'),
                        debit=line_data.get('debit', Decimal("0")),
                        credit=line_data.get('credit', Decimal("0")),
                        description=line_data.get('description')
                    )
                    session.add(line)
            
            session.commit()
            return True, "Jurnal berhasil diupdate"
            
        except Exception as e:
            session.rollback()
            return False, f"Error: {str(e)}"
        finally:
            session.close()

    def delete_journal(self, journal_id: int) -> Tuple[bool, str]:
        """Delete journal (only if not posted)"""
        from src.models import JournalHeader, Period
        
        session = DatabaseSession.get_session()
        try:
            header = session.query(JournalHeader).filter(
                JournalHeader.id == journal_id
            ).first()
            
            if not header:
                return False, "Jurnal tidak ditemukan"
            
            if header.status == "POSTED":
                return False, "Tidak bisa menghapus jurnal yang sudah diposting"
            
            period = session.query(Period).filter(
                Period.id == header.period_id
            ).first()
            
            if period and period.is_closed:
                return False, "Period sudah ditutup"
            
            session.query(JournalHeader).filter(
                JournalHeader.id == journal_id
            ).delete()
            
            session.commit()
            return True, "Jurnal berhasil dihapus"
            
        except Exception as e:
            session.rollback()
            return False, f"Error: {str(e)}"
        finally:
            session.close()

    def get_account_balances(
        self,
        company_id: int,
        period_id: int
    ) -> List[Dict[str, Any]]:
        """Get all account balances for a period"""
        from src.models import GLAccount, JournalHeader, JournalLine
        
        session = DatabaseSession.get_session()
        try:
            period = session.query(Period).filter(Period.id == period_id).first()
            if not period:
                return []
            
            accounts = session.query(GLAccount).filter(
                GLAccount.company_id == company_id,
                GLAccount.show_in_trial_balance == True,
                GLAccount.is_active == True,
                GLAccount.account_type == "DETAIL"
            ).order_by(GLAccount.code).all()
            
            result = []
            for account in accounts:
                balance = account.initial_balance or Decimal("0")
                
                journal_lines = session.query(JournalLine).join(
                    JournalHeader
                ).filter(
                    JournalLine.account_id == account.id,
                    JournalHeader.date <= period.end_date,
                    JournalHeader.status == "POSTED"
                ).all()
                
                total_debit = Decimal("0")
                total_credit = Decimal("0")
                
                for line in journal_lines:
                    total_debit += line.debit or Decimal("0")
                    total_credit += line.credit or Decimal("0")
                
                if account.normal_balance == "DEBIT":
                    balance = balance + total_debit - total_credit
                else:
                    balance = balance + total_credit - total_debit
                
                result.append({
                    "account_id": account.id,
                    "account_code": account.code,
                    "account_name": account.name,
                    "normal_balance": account.normal_balance,
                    "initial_balance": float(account.initial_balance) if account.initial_balance else 0,
                    "total_debit": float(total_debit),
                    "total_credit": float(total_credit),
                    "balance": float(balance)
                })
            
            return result
            
        finally:
            session.close()

    def get_journal_lines_by_account(
        self,
        account_id: int,
        company_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get all journal lines for a specific account"""
        from src.models import JournalHeader, JournalLine
        
        session = DatabaseSession.get_session()
        try:
            query = session.query(JournalLine).join(
                JournalHeader
            ).filter(
                JournalLine.account_id == account_id,
                JournalHeader.company_id == company_id,
                JournalHeader.status == "POSTED"
            )
            
            if start_date:
                query = query.filter(JournalHeader.date >= start_date)
            
            if end_date:
                query = query.filter(JournalHeader.date <= end_date)
            
            lines = query.order_by(JournalHeader.date, JournalHeader.id).all()
            
            result = []
            for line in lines:
                header = line.header
                result.append({
                    "line_id": line.id,
                    "header_id": header.id,
                    "journal_no": header.journal_no,
                    "date": header.date.isoformat() if header.date else None,
                    "description": header.description,
                    "reference": header.reference,
                    "debit": float(line.debit) if line.debit else 0,
                    "credit": float(line.credit) if line.credit else 0,
                    "line_description": line.description
                })
            
            return result
            
        finally:
            session.close()


journal_service = JournalService()
