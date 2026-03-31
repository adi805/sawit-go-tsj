"""
Sawit Go - TSJ - GL Accounts View
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QDialog, QFormLayout, QLineEdit, QComboBox, QCheckBox, QLabel,
    QDialogButtonBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class GLAccountsView(QWidget):
    """GL Accounts management view"""
    
    def __init__(self, user_info, parent=None):
        super().__init__(parent)
        self.user_info = user_info
        self.company_id = user_info.get('company_id', 1)
        self._setup_ui()
        self._load_accounts()
    
    def _setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        
        header = QHBoxLayout()
        title = QLabel("Chart of Accounts (Buku Besar Umum)")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.addWidget(title)
        header.addStretch()
        
        self.add_button = QPushButton("+ Tambah Akun")
        self.add_button.clicked.connect(self._on_add_account)
        header.addWidget(self.add_button)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self._load_accounts)
        header.addWidget(self.refresh_button)
        
        layout.addLayout(header)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Kode", "Nama Akun", "Tipe", "Saldo Normal", "Saldo", "Aktif"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.itemDoubleClicked.connect(self._on_edit_account)
        layout.addWidget(self.table)
        
        footer = QHBoxLayout()
        self.status_label = QLabel("Total: 0 akun")
        footer.addWidget(self.status_label)
        footer.addStretch()
        layout.addLayout(footer)
    
    def _load_accounts(self):
        """Load accounts from database"""
        from src.services.gl_account_service import gl_account_service
        
        accounts = gl_account_service.get_all(self.company_id)
        
        self.table.setRowCount(len(accounts))
        
        for row, acc in enumerate(accounts):
            self.table.setItem(row, 0, QTableWidgetItem(acc.get('code', '')))
            self.table.setItem(row, 1, QTableWidgetItem(acc.get('name', '')))
            self.table.setItem(row, 2, QTableWidgetItem(acc.get('account_type', '')))
            self.table.setItem(row, 3, QTableWidgetItem(acc.get('normal_balance', '')))
            
            balance = gl_account_service.get_balance(acc['id'])
            self.table.setItem(row, 4, QTableWidgetItem(f"Rp {balance:,.2f}"))
            
            active = "Ya" if acc.get('is_active', True) else "Tidak"
            self.table.setItem(row, 5, QTableWidgetItem(active))
        
        self.status_label.setText(f"Total: {len(accounts)} akun")
    
    def _on_add_account(self):
        """Handle add account button click"""
        dialog = AccountDialog(self.company_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._load_accounts()
    
    def _on_edit_account(self, item):
        """Handle edit account"""
        row = item.row()
        account_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        if account_id is None:
            account_id = row + 1
        
        dialog = AccountDialog(self.company_id, account_id=account_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._load_accounts()


class AccountDialog(QDialog):
    """Account add/edit dialog"""
    
    def __init__(self, company_id, account_id=None, parent=None):
        super().__init__(parent)
        self.company_id = company_id
        self.account_id = account_id
        self.is_edit = account_id is not None
        
        self.setWindowTitle("Edit Akun" if self.is_edit else "Tambah Akun")
        self.setModal(True)
        self.setMinimumWidth(500)
        self._setup_ui()
        
        if self.is_edit:
            self._load_account()
    
    def _setup_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(10)
        
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Contoh: 1-1000")
        layout.addRow("Kode Akun *", self.code_input)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nama akun")
        layout.addRow("Nama Akun *", self.name_input)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["DETAIL", "HEADER"])
        layout.addRow("Tipe Akun", self.type_combo)
        
        self.balance_combo = QComboBox()
        self.balance_combo.addItems(["DEBIT", "CREDIT"])
        layout.addRow("Saldo Normal", self.balance_combo)
        
        self.active_check = QCheckBox("Akun Aktif")
        self.active_check.setChecked(True)
        layout.addRow("Status", self.active_check)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._on_save)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
    
    def _load_account(self):
        """Load account data for editing"""
        from src.services.gl_account_service import gl_account_service
        
        acc = gl_account_service.get_by_id(self.account_id)
        if acc:
            self.code_input.setText(acc.get('code', ''))
            self.name_input.setText(acc.get('name', ''))
            self.type_combo.setCurrentText(acc.get('account_type', 'DETAIL'))
            self.balance_combo.setCurrentText(acc.get('normal_balance', 'DEBIT'))
            self.active_check.setChecked(acc.get('is_active', True))
    
    def _on_save(self):
        """Handle save button"""
        code = self.code_input.text().strip()
        name = self.name_input.text().strip()
        
        if not code or not name:
            QMessageBox.warning(self, "Error", "Kode dan Nama akun harus diisi!")
            return
        
        from src.services.gl_account_service import gl_account_service
        
        data = {
            'account_type': self.type_combo.currentText(),
            'normal_balance': self.balance_combo.currentText(),
            'is_active': self.active_check.isChecked(),
            'allow_entry': self.type_combo.currentText() == 'DETAIL',
            'show_in_trial_balance': True,
        }
        
        if self.is_edit:
            success = gl_account_service.update(self.account_id, code=code, name=name, **data)
        else:
            success = gl_account_service.create(self.company_id, code, name, **data)
        
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Gagal menyimpan akun!")
