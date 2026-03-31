"""
Sawit Go - TSJ - Trial Balance View
Trial balance report display widget
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QDialog, QComboBox, QLabel, QFrame, QGridLayout,
    QCheckBox, QDateEdit, QLineEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor
from decimal import Decimal
from typing import Dict, Any, List, Optional
from datetime import datetime, date


class TrialBalanceView(QWidget):
    """Trial Balance report view widget"""
    
    def __init__(self, user_info: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.user_info = user_info
        self.company_id = user_info.get('company_id', 1)
        self.current_period_id = None
        self.report_data = None
        
        self._setup_ui()
        self._load_periods()
    
    def _setup_ui(self):
        """Setup UI components"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        
        header_layout = QHBoxLayout()
        
        title = QLabel("Neraca Saldo (Trial Balance)")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        self.export_button = QPushButton("Export Excel")
        self.export_button.clicked.connect(self._on_export)
        header_layout.addWidget(self.export_button)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self._load_report)
        header_layout.addWidget(self.refresh_button)
        
        main_layout.addLayout(header_layout)
        
        filter_layout = QGridLayout()
        filter_layout.setSpacing(10)
        
        filter_layout.addWidget(QLabel("Period:"), 0, 0)
        self.period_combo = QComboBox()
        self.period_combo.currentIndexChanged.connect(self._on_period_changed)
        filter_layout.addWidget(self.period_combo, 0, 1, 1, 2)
        
        self.zero_balance_check = QCheckBox("Tampilkan saldo nol")
        self.zero_balance_check.stateChanged.connect(self._load_report)
        filter_layout.addWidget(self.zero_balance_check, 1, 0)
        
        filter_layout.addWidget(QLabel("Tanggal:"), 0, 3)
        self.date_label = QLabel("-")
        filter_layout.addWidget(self.date_label, 0, 4)
        
        main_layout.addLayout(filter_layout)
        
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.Shape.StyledPanel)
        info_frame.setStyleSheet("QFrame { background-color: #e8f4f8; padding: 10px; border-radius: 5px; }")
        info_layout = QGridLayout(info_frame)
        info_layout.setSpacing(15)
        
        self.company_label = QLabel("Perusahaan: -")
        self.company_label.setFont(QFont("Arial", 10))
        info_layout.addWidget(self.company_label, 0, 0)
        
        self.period_label = QLabel("Period: -")
        self.period_label.setFont(QFont("Arial", 10))
        info_layout.addWidget(self.period_label, 0, 1)
        
        self.status_label = QLabel("Status: -")
        self.status_label.setFont(QFont("Arial", 10))
        info_layout.addWidget(self.status_label, 0, 2)
        
        main_layout.addWidget(info_frame)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Kode Akun",
            "Nama Akun",
            "Saldo Awal",
            "Debit Period Ini",
            "Kredit Period Ini",
            "Saldo Akhir"
        ])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        main_layout.addWidget(self.table)
        
        totals_frame = QFrame()
        totals_frame.setFrameShape(QFrame.Shape.StyledPanel)
        totals_frame.setStyleSheet("QFrame { background-color: #f0f0f0; padding: 15px; }")
        totals_layout = QGridLayout(totals_frame)
        totals_layout.setSpacing(20)
        
        debit_total_label = QLabel("Total Debit:")
        debit_total_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        totals_layout.addWidget(debit_total_label, 0, 0)
        
        self.debit_total_value = QLabel("Rp 0.00")
        self.debit_total_value.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.debit_total_value.setStyleSheet("color: #1976D2;")
        totals_layout.addWidget(self.debit_total_value, 0, 1)
        
        credit_total_label = QLabel("Total Kredit:")
        credit_total_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        totals_layout.addWidget(credit_total_label, 0, 2)
        
        self.credit_total_value = QLabel("Rp 0.00")
        self.credit_total_value.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.credit_total_value.setStyleSheet("color: #388E3C;")
        totals_layout.addWidget(self.credit_total_value, 0, 3)
        
        balance_label = QLabel("Status:")
        balance_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        totals_layout.addWidget(balance_label, 0, 4)
        
        self.balance_status = QLabel("-")
        self.balance_status.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        totals_layout.addWidget(self.balance_status, 0, 5)
        
        main_layout.addWidget(totals_frame)
        
        footer_layout = QHBoxLayout()
        self.count_label = QLabel("Total: 0 akun")
        footer_layout.addWidget(self.count_label)
        footer_layout.addStretch()
        
        self.print_button = QPushButton("Cetak")
        self.print_button.clicked.connect(self._on_print)
        footer_layout.addWidget(self.print_button)
        
        main_layout.addLayout(footer_layout)
    
    def _load_periods(self):
        """Load periods for selection"""
        from src.services.report_service import report_service
        
        self.period_combo.clear()
        periods = report_service.get_period_list(self.company_id)
        
        if not periods:
            QMessageBox.information(
                self,
                "Info",
                "Tidak ada period. Membuat period baru..."
            )
            
            year = datetime.now().year
            month = datetime.now().month
            
            for m in range(1, 13):
                period_id = report_service.create_period(self.company_id, year, m)
            
            periods = report_service.get_period_list(self.company_id)
        
        for p in periods:
            self.period_combo.addItem(p['period_name'], p['id'])
        
        if self.period_combo.count() > 0:
            self.current_period_id = self.period_combo.itemData(0)
            self._load_report()
    
    def _on_period_changed(self, index: int):
        """Handle period selection change"""
        if index >= 0:
            self.current_period_id = self.period_combo.itemData(index)
            self._load_report()
    
    def _load_report(self):
        """Load trial balance report"""
        if not self.current_period_id:
            return
        
        from src.services.report_service import report_service
        
        include_zero = self.zero_balance_check.isChecked()
        
        self.report_data = report_service.generate_trial_balance(
            company_id=self.company_id,
            period_id=self.current_period_id,
            include_zero_balances=include_zero
        )
        
        if not self.report_data:
            QMessageBox.critical(
                self,
                "Error",
                "Gagal generate laporan Neraca Saldo!"
            )
            return
        
        self._update_display()
    
    def _update_display(self):
        """Update table display with report data"""
        if not self.report_data:
            return
        
        self.company_label.setText(f"Perusahaan: {self.report_data.company_name}")
        self.period_label.setText(f"Period: {self.report_data.period_name}")
        
        period_text = f"{self.report_data.start_date} s/d {self.report_data.end_date}"
        self.date_label.setText(period_text)
        
        is_balanced = self.report_data.is_balanced
        status_text = "SEIMBANG" if is_balanced else "TIDAK SEIMBANG"
        status_color = "#4CAF50" if is_balanced else "#F44336"
        
        self.status_label.setText(f"Status: {status_text}")
        self.status_label.setStyleSheet(f"color: {status_color}; font-weight: bold;")
        
        self.table.setRowCount(len(self.report_data.items))
        
        row = 0
        for item in self.report_data.items:
            code_item = QTableWidgetItem(item.get('account_code', ''))
            code_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, code_item)
            
            self.table.setItem(row, 1, QTableWidgetItem(item.get('account_name', '')))
            
            initial = item.get('initial_balance', Decimal("0"))
            initial_item = QTableWidgetItem(f"{float(initial):,.4f}")
            initial_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.table.setItem(row, 2, initial_item)
            
            debit = item.get('total_debit', Decimal("0"))
            debit_item = QTableWidgetItem(f"{float(debit):,.4f}")
            debit_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.table.setItem(row, 3, debit_item)
            
            credit = item.get('total_credit', Decimal("0"))
            credit_item = QTableWidgetItem(f"{float(credit):,.4f}")
            credit_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.table.setItem(row, 4, credit_item)
            
            balance = item.get('ending_balance', Decimal("0"))
            balance_item = QTableWidgetItem(f"{float(balance):,.4f}")
            balance_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            
            if float(balance) < 0:
                balance_item.setForeground(QColor(255, 0, 0))
            elif float(balance) > 0:
                balance_item.setForeground(QColor(0, 100, 0))
            
            self.table.setItem(row, 5, balance_item)
            
            row += 1
        
        total_debit = self.report_data.total_debit
        total_credit = self.report_data.total_credit
        
        self.debit_total_value.setText(f"Rp {float(total_debit):,.2f}")
        self.credit_total_value.setText(f"Rp {float(total_credit):,.2f}")
        
        diff = abs(total_debit - total_credit)
        if self.report_data.is_balanced:
            self.balance_status.setText("SEIMBANG")
            self.balance_status.setStyleSheet("color: #4CAF50; font-weight: bold;")
        else:
            self.balance_status.setText(f"SELISIH: Rp {float(diff):,.2f}")
            self.balance_status.setStyleSheet("color: #F44336; font-weight: bold;")
        
        self.count_label.setText(f"Total: {len(self.report_data.items)} akun")
    
    def _on_export(self):
        """Handle export button click"""
        if not self.report_data:
            QMessageBox.information(self, "Info", "Tidak ada data untuk di-export!")
            return
        
        from src.ui.export_dialog import ExportDialog
        
        dialog = ExportDialog(
            report_type="trial_balance",
            report_data=self.report_data,
            parent=self
        )
        dialog.exec()
    
    def _on_print(self):
        """Handle print button click"""
        QMessageBox.information(
            self,
            "Info",
            "Fitur cetak belum diimplementasikan"
        )
    
    def set_period(self, period_id: int):
        """Set current period programmatically"""
        for i in range(self.period_combo.count()):
            if self.period_combo.itemData(i) == period_id:
                self.period_combo.setCurrentIndex(i)
                break
    
    def refresh(self):
        """Refresh the report"""
        self._load_report()


class TrialBalancePreviewDialog(QDialog):
    """Trial balance preview dialog"""
    
    def __init__(self, report_data, parent=None):
        super().__init__(parent)
        self.report_data = report_data
        
        self.setWindowTitle(f"Neraca Saldo - Preview")
        self.setModal(True)
        self.setMinimumSize(800, 600)
        
        self._setup_ui()
        self._populate_data()
    
    def _setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        
        header = QLabel("NERACA SALDO (TRIAL BALANCE)")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        info = QLabel(
            f"{self.report_data.company_name}\n"
            f"Periode: {self.report_data.period_name}\n"
            f"Tanggal: {self.report_data.start_date} s/d {self.report_data.end_date}"
        )
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Kode", "Nama Akun", "Debit", "Kredit"
        ])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        
        totals_frame = QFrame()
        totals_frame.setFrameShape(QFrame.Shape.StyledPanel)
        totals_layout = QHBoxLayout(totals_frame)
        
        self.total_debit_label = QLabel("Total Debit: Rp 0")
        self.total_debit_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        totals_layout.addWidget(self.total_debit_label)
        
        totals_layout.addStretch()
        
        self.total_credit_label = QLabel("Total Kredit: Rp 0")
        self.total_credit_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        totals_layout.addWidget(self.total_credit_label)
        
        layout.addWidget(totals_frame)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_button = QPushButton("Tutup")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def _populate_data(self):
        """Populate table with report data"""
        self.table.setRowCount(len(self.report_data.items))
        
        row = 0
        for item in self.report_data.items:
            self.table.setItem(row, 0, QTableWidgetItem(item.get('account_code', '')))
            self.table.setItem(row, 1, QTableWidgetItem(item.get('account_name', '')))
            
            debit = item.get('total_debit', Decimal("0"))
            self.table.setItem(row, 2, QTableWidgetItem(f"Rp {float(debit):,.2f}"))
            
            credit = item.get('total_credit', Decimal("0"))
            self.table.setItem(row, 3, QTableWidgetItem(f"Rp {float(credit):,.2f}"))
            
            row += 1
        
        self.total_debit_label.setText(
            f"Total Debit: Rp {float(self.report_data.total_debit):,.2f}"
        )
        self.total_credit_label.setText(
            f"Total Kredit: Rp {float(self.report_data.total_credit):,.2f}"
        )


class JournalBookView(QWidget):
    """Journal Book report view widget"""
    
    def __init__(self, user_info: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.user_info = user_info
        self.company_id = user_info.get('company_id', 1)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        
        header = QLabel("Buku Jurnal Umum")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(header)
        
        filter_layout = QGridLayout()
        
        filter_layout.addWidget(QLabel("Dari Tanggal:"), 0, 0)
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate().addMonths(-1))
        filter_layout.addWidget(self.start_date_edit, 0, 1)
        
        filter_layout.addWidget(QLabel("Sampai Tanggal:"), 0, 2)
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())
        filter_layout.addWidget(self.end_date_edit, 0, 3)
        
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self._generate_report)
        filter_layout.addWidget(self.generate_button, 0, 4)
        
        layout.addLayout(filter_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "No Jurnal", "Tanggal", "Referensi", "Keterangan", "Total"
        ])
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        
        footer = QHBoxLayout()
        footer.addWidget(QLabel("Total: 0 entri"))
        footer.addStretch()
        
        self.export_btn = QPushButton("Export")
        self.export_btn.clicked.connect(self._on_export)
        footer.addWidget(self.export_btn)
        
        layout.addLayout(footer)
    
    def _generate_report(self):
        """Generate journal book report"""
        start_date = self.start_date_edit.date().toPyDate()
        end_date = self.end_date_edit.date().toPyDate()
        
        from src.services.report_service import report_service
        
        report = report_service.generate_journal_book(
            company_id=self.company_id,
            start_date=start_date,
            end_date=end_date
        )
        
        if not report:
            QMessageBox.critical(self, "Error", "Gagal generate laporan!")
            return
        
        self.table.setRowCount(len(report.entries))
        
        for row, entry in enumerate(report.entries):
            self.table.setItem(row, 0, QTableWidgetItem(entry.get('journal_no', '')))
            self.table.setItem(row, 1, QTableWidgetItem(entry.get('date', '')))
            self.table.setItem(row, 2, QTableWidgetItem(entry.get('reference', '')))
            self.table.setItem(row, 3, QTableWidgetItem(entry.get('description', '')))
            
            total = entry.get('total_debit', 0)
            self.table.setItem(row, 4, QTableWidgetItem(f"Rp {total:,.2f}"))
    
    def _on_export(self):
        """Handle export button"""
        QMessageBox.information(self, "Info", "Export Buku Jurnal")
