"""
Sawit Go - TSJ - Journal Entry View
Journal entry dialog with debit=credit validation
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QDialog, QComboBox, QLineEdit, QDateEdit,
    QLabel, QDialogButtonBox, QFrame, QGridLayout, QDoubleSpinBox,
    QCompleter, QStyledItemDelegate
)
from PyQt6.QtCore import Qt, QDate, QTimer
from PyQt6.QtGui import QFont, QColor
from decimal import Decimal
from typing import Dict, Any, List, Optional


class AccountCompleterDelegate(QStyledItemDelegate):
    """Custom delegate for account combo in table"""
    
    def __init__(self, accounts: List[Dict[str, Any]], parent=None):
        super().__init__(parent)
        self.accounts = accounts


class JournalEntryDialog(QDialog):
    """Journal entry dialog for creating/editing journal entries"""
    
    def __init__(
        self,
        company_id: int,
        period_id: int,
        user_info: Dict[str, Any],
        journal_id: Optional[int] = None,
        parent=None
    ):
        super().__init__(parent)
        self.company_id = company_id
        self.period_id = period_id
        self.user_info = user_info
        self.journal_id = journal_id
        self.is_edit = journal_id is not None
        
        self.accounts = []
        self.journal_lines = []
        
        self.setWindowTitle("Edit Jurnal" if self.is_edit else "Entri Jurnal Baru")
        self.setModal(True)
        self.setMinimumSize(900, 600)
        
        self._load_accounts()
        self._setup_ui()
        
        if self.is_edit:
            self._load_journal()
        
        self._update_totals()
    
    def _load_accounts(self):
        """Load GL accounts for selection"""
        from src.services.gl_account_service import gl_account_service
        
        all_accounts = gl_account_service.get_all(self.company_id, include_inactive=False)
        self.accounts = [
            acc for acc in all_accounts
            if acc.get('allow_entry', True) and acc.get('account_type') == 'DETAIL'
        ]
    
    def _setup_ui(self):
        """Setup UI components"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        
        header_layout = QFormLayout()
        header_layout.setSpacing(15)
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        header_layout.addRow("Tanggal *", self.date_edit)
        
        self.reference_input = QLineEdit()
        self.reference_input.setPlaceholderText("Nomor referensi...")
        header_layout.addRow("Referensi", self.reference_input)
        
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Keterangan jurnal...")
        header_layout.addRow("Keterangan *", self.description_input)
        
        self.period_label = QLabel()
        self._update_period_label()
        header_layout.addRow("Period", self.period_label)
        
        main_layout.addLayout(header_layout)
        
        lines_label = QLabel("Detail Jurnal")
        lines_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        main_layout.addWidget(lines_label)
        
        self.lines_table = QTableWidget()
        self.lines_table.setColumnCount(5)
        self.lines_table.setHorizontalHeaderLabels([
            "Akun", "Debit", "Kredit", "Keterangan", "Hapus"
        ])
        self.lines_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.lines_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.lines_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.lines_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.lines_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.lines_table.setColumnWidth(1, 130)
        self.lines_table.setColumnWidth(2, 130)
        self.lines_table.setColumnWidth(4, 60)
        self.lines_table.setAlternatingRowColors(True)
        self.lines_table.setMinimumHeight(250)
        main_layout.addWidget(self.lines_table)
        
        button_layout = QHBoxLayout()
        
        self.add_line_btn = QPushButton("+ Tambah Baris")
        self.add_line_btn.clicked.connect(self._add_line)
        button_layout.addWidget(self.add_line_btn)
        
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        totals_frame = QFrame()
        totals_frame.setFrameShape(QFrame.Shape.StyledPanel)
        totals_frame.setStyleSheet("QFrame { background-color: #f5f5f5; padding: 10px; }")
        totals_layout = QGridLayout(totals_frame)
        totals_layout.setSpacing(15)
        
        self.debit_label = QLabel("Total Debit: Rp 0.00")
        self.debit_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        totals_layout.addWidget(self.debit_label, 0, 0)
        
        self.credit_label = QLabel("Total Kredit: Rp 0.00")
        self.credit_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        totals_layout.addWidget(self.credit_label, 0, 1)
        
        self.balance_label = QLabel("Selisih: Rp 0.00")
        self.balance_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        totals_layout.addWidget(self.balance_label, 0, 2)
        
        main_layout.addWidget(totals_frame)
        
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._on_save)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)
        
        self._add_line()
        self._add_line()
    
    def _update_period_label(self):
        """Update period display label"""
        from src.services.report_service import report_service
        
        periods = report_service.get_period_list(self.company_id)
        for p in periods:
            if p['id'] == self.period_id:
                self.period_label.setText(p['period_name'])
                return
        self.period_label.setText(f"Period ID: {self.period_id}")
    
    def _add_line(self, account_id: Optional[int] = None, debit: float = 0,
                  credit: float = 0, description: str = ""):
        """Add a new journal line row"""
        row = self.lines_table.rowCount()
        self.lines_table.insertRow(row)
        
        account_combo = QComboBox()
        account_combo.addItem("-- Pilih Akun --", None)
        for acc in self.accounts:
            display = f"{acc['code']} - {acc['name']}"
            account_combo.addItem(display, acc['id'])
        
        if account_id:
            idx = account_combo.findData(account_id)
            if idx >= 0:
                account_combo.setCurrentIndex(idx)
        
        self.lines_table.setCellWidget(row, 0, account_combo)
        
        debit_spin = QDoubleSpinBox()
        debit_spin.setRange(0, 999999999999)
        debit_spin.setDecimals(4)
        debit_spin.setValue(debit)
        debit_spin.valueChanged.connect(self._update_totals)
        self.lines_table.setCellWidget(row, 1, debit_spin)
        
        credit_spin = QDoubleSpinBox()
        credit_spin.setRange(0, 999999999999)
        credit_spin.setDecimals(4)
        credit_spin.setValue(credit)
        credit_spin.valueChanged.connect(self._update_totals)
        self.lines_table.setCellWidget(row, 2, credit_spin)
        
        desc_input = QLineEdit(description)
        self.lines_table.setCellWidget(row, 3, desc_input)
        
        delete_btn = QPushButton("X")
        delete_btn.setFixedSize(40, 30)
        delete_btn.clicked.connect(lambda: self._delete_line(row))
        self.lines_table.setCellWidget(row, 4, delete_btn)
    
    def _delete_line(self, row: int):
        """Delete a journal line row"""
        if self.lines_table.rowCount() > 2:
            self.lines_table.removeRow(row)
            self._update_totals()
        else:
            QMessageBox.warning(
                self,
                "Peringatan",
                "Minimal harus ada 2 baris jurnal!"
            )
    
    def _update_totals(self):
        """Update debit/credit totals"""
        total_debit = Decimal("0")
        total_credit = Decimal("0")
        
        for row in range(self.lines_table.rowCount()):
            debit_widget = self.lines_table.cellWidget(row, 1)
            credit_widget = self.lines_table.cellWidget(row, 2)
            
            if debit_widget:
                total_debit += Decimal(str(debit_widget.value()))
            if credit_widget:
                total_credit += Decimal(str(credit_widget.value()))
        
        diff = total_debit - total_credit
        
        self.debit_label.setText(f"Total Debit: Rp {total_debit:,.4f}")
        self.credit_label.setText(f"Total Kredit: Rp {total_credit:,.4f}")
        self.balance_label.setText(f"Selisih: Rp {diff:,.4f}")
        
        if diff == 0:
            self.balance_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.balance_label.setStyleSheet("color: red; font-weight: bold;")
    
    def _load_journal(self):
        """Load existing journal for editing"""
        from src.services.journal_service import journal_service
        
        journal = journal_service.get_journal(self.journal_id)
        if not journal:
            QMessageBox.critical(self, "Error", "Jurnal tidak ditemukan!")
            self.reject()
            return
        
        if journal.get('date'):
            from datetime import datetime
            date_obj = datetime.strptime(journal['date'], '%Y-%m-%d').date()
            self.date_edit.setDate(QDate(date_obj.year, date_obj.month, date_obj.day))
        
        self.reference_input.setText(journal.get('reference') or "")
        self.description_input.setText(journal.get('description') or "")
        
        for row in range(self.lines_table.rowCount()):
            self.lines_table.removeRow(0)
        
        for line in journal.get('lines', []):
            self._add_line(
                account_id=line.get('account_id'),
                debit=line.get('debit', 0),
                credit=line.get('credit', 0),
                description=line.get('description') or ""
            )
    
    def _validate(self) -> tuple:
        """
        Validate journal entry.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        from datetime import datetime
        
        date_qdate = self.date_edit.date()
        journal_date = datetime(
            date_qdate.year(),
            date_qdate.month(),
            date_qdate.day()
        ).date()
        
        description = self.description_input.text().strip()
        if not description:
            return False, "Keterangan harus diisi!"
        
        lines = []
        has_error = False
        
        for row in range(self.lines_table.rowCount()):
            account_combo = self.lines_table.cellWidget(row, 0)
            debit_widget = self.lines_table.cellWidget(row, 1)
            credit_widget = self.lines_table.cellWidget(row, 2)
            desc_widget = self.lines_table.cellWidget(row, 3)
            
            account_id = account_combo.currentData() if account_combo else None
            debit = Decimal(str(debit_widget.value())) if debit_widget else Decimal("0")
            credit = Decimal(str(credit_widget.value())) if credit_widget else Decimal("0")
            line_desc = desc_widget.text() if desc_widget else ""
            
            if not account_id:
                has_error = True
                QMessageBox.warning(
                    self, "Validasi",
                    f"Baris {row + 1}: Akun harus dipilih!"
                )
                return False, f"Baris {row + 1}: Akun harus dipilih"
            
            if debit > 0 and credit > 0:
                has_error = True
                QMessageBox.warning(
                    self, "Validasi",
                    f"Baris {row + 1}: Tidak boleh mengisi debit dan kredit sekaligus!"
                )
                return False, f"Baris {row + 1}: Tidak boleh mengisi debit dan kredit sekaligus"
            
            if debit == 0 and credit == 0:
                has_error = True
                QMessageBox.warning(
                    self, "Validasi",
                    f"Baris {row + 1}: Harus mengisi debit atau kredit!"
                )
                return False, f"Baris {row + 1}: Harus mengisi debit atau kredit"
            
            lines.append({
                'account_id': account_id,
                'debit': debit,
                'credit': credit,
                'description': line_desc
            })
        
        if len(lines) < 2:
            return False, "Minimal harus ada 2 baris jurnal!"
        
        total_debit = sum(line['debit'] for line in lines)
        total_credit = sum(line['credit'] for line in lines)
        
        if total_debit != total_credit:
            return False, f"Total debit ({total_debit}) tidak sama dengan total kredit ({total_credit})!"
        
        return True, ""
    
    def _on_save(self):
        """Handle save button click"""
        is_valid, error_msg = self._validate()
        
        if not is_valid:
            QMessageBox.critical(self, "Validasi Gagal", error_msg)
            return
        
        from datetime import datetime
        
        date_qdate = self.date_edit.date()
        journal_date = datetime(
            date_qdate.year(),
            date_qdate.month(),
            date_qdate.day()
        ).date()
        
        lines = []
        for row in range(self.lines_table.rowCount()):
            account_combo = self.lines_table.cellWidget(row, 0)
            debit_widget = self.lines_table.cellWidget(row, 1)
            credit_widget = self.lines_table.cellWidget(row, 2)
            desc_widget = self.lines_table.cellWidget(row, 3)
            
            lines.append({
                'account_id': account_combo.currentData(),
                'debit': Decimal(str(debit_widget.value())) if debit_widget else Decimal("0"),
                'credit': Decimal(str(credit_widget.value())) if credit_widget else Decimal("0"),
                'description': desc_widget.text() if desc_widget else ""
            })
        
        from src.services.journal_service import journal_service
        
        if self.is_edit:
            success, message = journal_service.update_journal(
                journal_id=self.journal_id,
                journal_date=journal_date,
                description=self.description_input.text().strip(),
                reference=self.reference_input.text().strip() or None,
                lines=lines
            )
        else:
            result = journal_service.create_journal(
                company_id=self.company_id,
                period_id=self.period_id,
                journal_date=journal_date,
                description=self.description_input.text().strip(),
                reference=self.reference_input.text().strip() or None,
                lines=lines,
                created_by=self.user_info.get('user_id', 1)
            )
            success = result.success
            message = result.message
            if success:
                self.journal_id = result.journal_id
        
        if success:
            QMessageBox.information(self, "Berhasil", message)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", message)
    
    def get_journal_id(self) -> Optional[int]:
        """Get created/updated journal ID"""
        return self.journal_id


class JournalListView(QWidget):
    """Journal list view widget"""
    
    def __init__(self, user_info: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.user_info = user_info
        self.company_id = user_info.get('company_id', 1)
        self.period_id = 1
        
        self._setup_ui()
        self._load_journals()
    
    def _setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        header_layout = QHBoxLayout()
        
        title = QLabel("Daftar Jurnal")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        self.new_button = QPushButton("+ Entri Jurnal Baru")
        self.new_button.clicked.connect(self._on_new_journal)
        header_layout.addWidget(self.new_button)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self._load_journals)
        header_layout.addWidget(self.refresh_button)
        
        layout.addLayout(header_layout)
        
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Filter:"))
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Semua", "Tanggal", "Period"])
        self.filter_combo.currentIndexChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.filter_combo)
        
        self.filter_label = QLabel("Period:")
        self.filter_label.setVisible(False)
        filter_layout.addWidget(self.filter_label)
        
        self.period_combo = QComboBox()
        self._load_periods()
        self.period_combo.setVisible(False)
        self.period_combo.currentIndexChanged.connect(self._load_journals)
        filter_layout.addWidget(self.period_combo)
        
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "No Jurnal", "Tanggal", "Referensi", "Keterangan", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.doubleClicked.connect(self._on_edit_journal)
        layout.addWidget(self.table)
        
        footer_layout = QHBoxLayout()
        self.status_label = QLabel("Total: 0 jurnal")
        footer_layout.addWidget(self.status_label)
        footer_layout.addStretch()
        
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self._on_edit_journal)
        footer_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Hapus")
        self.delete_button.clicked.connect(self._on_delete_journal)
        footer_layout.addWidget(self.delete_button)
        
        layout.addLayout(footer_layout)
    
    def _load_periods(self):
        """Load periods for filter"""
        from src.services.report_service import report_service
        
        self.period_combo.clear()
        periods = report_service.get_period_list(self.company_id)
        
        for p in periods:
            self.period_combo.addItem(p['period_name'], p['id'])
    
    def _on_filter_changed(self, index: int):
        """Handle filter combo change"""
        show_period = index == 2
        self.filter_label.setVisible(show_period)
        self.period_combo.setVisible(show_period)
        
        if index == 1:
            pass
        else:
            self._load_journals()
    
    def _load_journals(self):
        """Load journals from database"""
        from src.services.journal_service import journal_service
        
        period_id = self.period_combo.currentData() if self.period_combo.currentIndex() >= 0 else None
        
        journals = journal_service.get_journals(
            company_id=self.company_id,
            period_id=period_id
        )
        
        self.table.setRowCount(len(journals))
        
        for row, journal in enumerate(journals):
            self.table.setItem(row, 0, QTableWidgetItem(str(journal.get('id', ''))))
            self.table.setItem(row, 1, QTableWidgetItem(journal.get('journal_no', '')))
            self.table.setItem(row, 2, QTableWidgetItem(journal.get('date', '')))
            self.table.setItem(row, 3, QTableWidgetItem(journal.get('reference', '')))
            self.table.setItem(row, 4, QTableWidgetItem(journal.get('description', '')))
            self.table.setItem(row, 5, QTableWidgetItem(journal.get('status', '')))
        
        self.status_label.setText(f"Total: {len(journals)} jurnal")
    
    def _on_new_journal(self):
        """Handle new journal button click"""
        dialog = JournalEntryDialog(
            company_id=self.company_id,
            period_id=self.period_id,
            user_info=self.user_info,
            parent=self
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._load_journals()
    
    def _on_edit_journal(self):
        """Handle edit journal button click"""
        selected = self.table.selectedIndexes()
        if not selected:
            QMessageBox.information(self, "Info", "Pilih jurnal yang akan diedit!")
            return
        
        row = selected[0].row()
        journal_id = int(self.table.item(row, 0).text())
        
        dialog = JournalEntryDialog(
            company_id=self.company_id,
            period_id=self.period_id,
            user_info=self.user_info,
            journal_id=journal_id,
            parent=self
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._load_journals()
    
    def _on_delete_journal(self):
        """Handle delete journal button click"""
        selected = self.table.selectedIndexes()
        if not selected:
            QMessageBox.information(self, "Info", "Pilih jurnal yang akan dihapus!")
            return
        
        row = selected[0].row()
        journal_id = int(self.table.item(row, 0).text())
        journal_no = self.table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self,
            "Konfirmasi",
            f"Yakin ingin menghapus jurnal {journal_no}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            from src.services.journal_service import journal_service
            success, message = journal_service.delete_journal(journal_id)
            
            if success:
                QMessageBox.information(self, "Berhasil", message)
                self._load_journals()
            else:
                QMessageBox.critical(self, "Error", message)
    
    def set_period(self, period_id: int):
        """Set current period"""
        self.period_id = period_id
        self._load_periods()
        
        for i in range(self.period_combo.count()):
            if self.period_combo.itemData(i) == period_id:
                self.period_combo.setCurrentIndex(i)
                break
