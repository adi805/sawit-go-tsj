"""
Sawit Go - TSJ - Main Window
Main application window with menu and navigation
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QToolBar, QStatusBar, QLabel,
    QTreeWidget, QTreeWidgetItem, QSplitter, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QCloseEvent
from loguru import logger

from src.config.settings import Settings


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, user_info=None):
        super().__init__()
        self.user_info = user_info or {}
        self.setWindowTitle(f"{Settings.APP_NAME} v{Settings.APP_VERSION}")
        self.setMinimumSize(1024, 768)
        self.resize(1280, 800)
        
        self._create_menu_bar()
        self._create_toolbar()
        self._create_central_widget()
        self._create_status_bar()
        
        logger.info(f"Main window created for user: {self.user_info.get('username', 'unknown')}")
    
    def _create_menu_bar(self) -> None:
        """Create menu bar"""
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("&File")
        
        new_company_action = QAction("&New Company", self)
        new_company_action.setShortcut("Ctrl+Shift+N")
        new_company_action.triggered.connect(self._on_new_company)
        file_menu.addAction(new_company_action)
        
        open_db_action = QAction("&Open Database", self)
        open_db_action.setShortcut("Ctrl+O")
        open_db_action.triggered.connect(self._on_open_database)
        file_menu.addAction(open_db_action)
        
        file_menu.addSeparator()
        
        backup_action = QAction("&Backup Database", self)
        backup_action.setShortcut("Ctrl+B")
        backup_action.triggered.connect(self._on_backup)
        file_menu.addAction(backup_action)
        
        restore_action = QAction("&Restore Database", self)
        restore_action.setShortcut("Ctrl+R")
        restore_action.triggered.connect(self._on_restore)
        file_menu.addAction(restore_action)
        
        file_menu.addSeparator()
        
        settings_action = QAction("Se&ttings", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self._on_settings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        master_menu = menubar.addMenu("&Master")
        
        org_action = QAction("&Organization", self)
        org_action.triggered.connect(self._on_organization)
        master_menu.addAction(org_action)
        
        master_menu.addSeparator()
        
        gl_action = QAction("&GL Accounts", self)
        gl_action.setShortcut("Ctrl+G")
        gl_action.triggered.connect(self._on_gl_accounts)
        master_menu.addAction(gl_action)
        
        sl_action = QAction("&SL Accounts", self)
        sl_action.setShortcut("Ctrl+L")
        sl_action.triggered.connect(self._on_sl_accounts)
        master_menu.addAction(sl_action)
        
        fs_action = QAction("&FS Accounts", self)
        fs_action.setShortcut("Ctrl+F")
        fs_action.triggered.connect(self._on_fs_accounts)
        master_menu.addAction(fs_action)
        
        journal_menu = menubar.addMenu("&Transaksi")
        
        journal_entry_action = QAction("&Journal Entry", self)
        journal_entry_action.setShortcut("Ctrl+J")
        journal_entry_action.triggered.connect(self._on_journal_entry)
        journal_menu.addAction(journal_entry_action)
        
        journal_list_action = QAction("&Journal List", self)
        journal_list_action.setShortcut("Ctrl+Shift+J")
        journal_list_action.triggered.connect(self._on_journal_list)
        journal_menu.addAction(journal_list_action)
        
        report_menu = menubar.addMenu("&Laporan")
        
        trial_balance_action = QAction("&Trial Balance", self)
        trial_balance_action.setShortcut("Ctrl+T")
        trial_balance_action.triggered.connect(self._on_trial_balance)
        report_menu.addAction(trial_balance_action)
        
        general_ledger_action = QAction("&General Ledger", self)
        general_ledger_action.setShortcut("Ctrl+Shift+G")
        general_ledger_action.triggered.connect(self._on_general_ledger)
        report_menu.addAction(general_ledger_action)
        
        journal_report_action = QAction("&Journal Report", self)
        journal_report_action.setShortcut("Ctrl+Shift+R")
        journal_report_action.triggered.connect(self._on_journal_report)
        report_menu.addAction(journal_report_action)
        
        help_menu = menubar.addMenu("&Help")
        
        user_guide_action = QAction("&User Guide", self)
        user_guide_action.triggered.connect(self._on_user_guide)
        help_menu.addAction(user_guide_action)
        
        shortcuts_action = QAction("&Keyboard Shortcuts", self)
        shortcuts_action.triggered.connect(self._on_shortcuts)
        help_menu.addAction(shortcuts_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)
    
    def _create_toolbar(self) -> None:
        """Create toolbar"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        new_action = QAction("New", self)
        new_action.setToolTip("New Record (Ctrl+N)")
        new_action.triggered.connect(self._on_new)
        toolbar.addAction(new_action)
        
        save_action = QAction("Save", self)
        save_action.setToolTip("Save (Ctrl+S)")
        save_action.triggered.connect(self._on_save)
        toolbar.addAction(save_action)
        
        delete_action = QAction("Delete", self)
        delete_action.setToolTip("Delete (Ctrl+D)")
        delete_action.triggered.connect(self._on_delete)
        toolbar.addAction(delete_action)
        
        toolbar.addSeparator()
        
        refresh_action = QAction("Refresh", self)
        refresh_action.setToolTip("Refresh (F5)")
        refresh_action.triggered.connect(self._on_refresh)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        company_name = self.user_info.get('company_name', 'PT Tulas Sakti Jaya')
        self.company_label = QLabel(f"Company: {company_name}")
        toolbar.addWidget(self.company_label)
        
        toolbar.addSeparator()
        
        username = self.user_info.get('full_name', 'Admin')
        self.user_label = QLabel(f"User: {username}")
        toolbar.addWidget(self.user_label)
    
    def _create_central_widget(self) -> None:
        """Create central widget with navigation and content area"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        nav_widget = self._create_navigation()
        splitter.addWidget(nav_widget)
        
        content_widget = QLabel("Welcome to Sawit Go - TSJ\n\nSelect a menu from the menu bar or use the navigation panel on the left.")
        content_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_widget.setStyleSheet("font-size: 16px; color: #666; padding: 50px;")
        splitter.addWidget(content_widget)
        
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([250, 800])
    
    def _create_navigation(self) -> QWidget:
        """Create navigation tree widget"""
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(5, 5, 5, 5)
        
        tree = QTreeWidget()
        tree.setHeaderLabel("Navigation")
        tree.setStyleSheet("""
            QTreeWidget {
                border: none;
                background-color: #f5f5f5;
            }
            QTreeWidget::item {
                padding: 5px;
            }
            QTreeWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
        """)
        
        master_item = QTreeWidgetItem(tree, ["Master Data"])
        master_item.setExpanded(True)
        
        QTreeWidgetItem(master_item, ["GL Accounts"])
        QTreeWidgetItem(master_item, ["SL Accounts"])
        QTreeWidgetItem(master_item, ["FS Accounts"])
        
        transaction_item = QTreeWidgetItem(tree, ["Transaksi"])
        transaction_item.setExpanded(True)
        
        QTreeWidgetItem(transaction_item, ["Journal Entry"])
        QTreeWidgetItem(transaction_item, ["Journal List"])
        
        report_item = QTreeWidgetItem(tree, ["Laporan"])
        report_item.setExpanded(False)
        
        QTreeWidgetItem(report_item, ["Trial Balance"])
        QTreeWidgetItem(report_item, ["General Ledger"])
        QTreeWidgetItem(report_item, ["Journal Report"])
        
        tree.itemClicked.connect(self._on_nav_item_clicked)
        
        nav_layout.addWidget(tree)
        return nav_widget
    
    def _create_status_bar(self) -> None:
        """Create status bar"""
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        
        statusbar.showMessage("Ready")
        statusbar.addPermanentWidget(QLabel(f"Company: PT Tulas Sakti Jaya | "))
        statusbar.addPermanentWidget(QLabel("User: Admin | "))
        statusbar.addPermanentWidget(QLabel(f"DB: {Settings.DATABASE_FILE.name}"))
    
    def _on_new_company(self) -> None:
        """Handle new company action"""
        logger.info("New company action triggered")
        QMessageBox.information(self, "Info", "New Company dialog would open here")
    
    def _on_open_database(self) -> None:
        """Handle open database action"""
        logger.info("Open database action triggered")
        QMessageBox.information(self, "Info", "Open Database dialog would open here")
    
    def _on_backup(self) -> None:
        """Handle backup action"""
        logger.info("Backup action triggered")
        QMessageBox.information(self, "Info", "Backup dialog would open here")
    
    def _on_restore(self) -> None:
        """Handle restore action"""
        logger.info("Restore action triggered")
        QMessageBox.information(self, "Info", "Restore dialog would open here")
    
    def _on_settings(self) -> None:
        """Handle settings action"""
        logger.info("Settings action triggered")
        QMessageBox.information(self, "Info", "Settings dialog would open here")
    
    def _on_organization(self) -> None:
        """Handle organization action"""
        logger.info("Organization action triggered")
    
    def _on_gl_accounts(self) -> None:
        """Handle GL accounts action"""
        logger.info("GL Accounts action triggered")
        QMessageBox.information(self, "Info", "GL Accounts view would open here")
    
    def _on_sl_accounts(self) -> None:
        """Handle SL accounts action"""
        logger.info("SL Accounts action triggered")
    
    def _on_fs_accounts(self) -> None:
        """Handle FS accounts action"""
        logger.info("FS Accounts action triggered")
    
    def _on_journal_entry(self) -> None:
        """Handle journal entry action"""
        logger.info("Journal Entry action triggered")
        QMessageBox.information(self, "Info", "Journal Entry view would open here")
    
    def _on_journal_list(self) -> None:
        """Handle journal list action"""
        logger.info("Journal List action triggered")
    
    def _on_trial_balance(self) -> None:
        """Handle trial balance action"""
        logger.info("Trial Balance action triggered")
        QMessageBox.information(self, "Info", "Trial Balance report would open here")
    
    def _on_general_ledger(self) -> None:
        """Handle general ledger action"""
        logger.info("General Ledger action triggered")
    
    def _on_journal_report(self) -> None:
        """Handle journal report action"""
        logger.info("Journal Report action triggered")
    
    def _on_user_guide(self) -> None:
        """Handle user guide action"""
        logger.info("User Guide action triggered")
    
    def _on_shortcuts(self) -> None:
        """Handle keyboard shortcuts action"""
        logger.info("Keyboard Shortcuts action triggered")
        shortcuts_text = """
Keyboard Shortcuts:

File Menu:
  Ctrl+Shift+N - New Company
  Ctrl+O       - Open Database
  Ctrl+B       - Backup Database
  Ctrl+R       - Restore Database
  Ctrl+,       - Settings
  Alt+F4       - Exit

Master Menu:
  Ctrl+G       - GL Accounts
  Ctrl+L       - SL Accounts
  Ctrl+F       - FS Accounts

Transaksi Menu:
  Ctrl+J       - Journal Entry
  Ctrl+Shift+J - Journal List

Laporan Menu:
  Ctrl+T       - Trial Balance
  Ctrl+Shift+G - General Ledger
  Ctrl+Shift+R - Journal Report

General:
  Ctrl+N       - New Record
  Ctrl+S       - Save
  Ctrl+D       - Delete
  Ctrl+F       - Find
  F5           - Refresh
  Esc          - Cancel/Close
        """
        QMessageBox.information(self, "Keyboard Shortcuts", shortcuts_text.strip())
    
    def _on_about(self) -> None:
        """Handle about action"""
        about_text = f"""
{Settings.APP_NAME}

Version: {Settings.APP_VERSION}

Developed by: {Settings.APP_AUTHOR}
Company: {Settings.APP_COMPANY}

Description:
Sistem Akuntansi Modern untuk Perkebunan Sawit
Ringan, Fleksibel, dan Bisa Jalan di Mana Saja

© 2026 {Settings.APP_AUTHOR}
        """
        QMessageBox.about(self, "About", about_text.strip())
    
    def _on_new(self) -> None:
        """Handle new action"""
        logger.info("New action triggered")
    
    def _on_save(self) -> None:
        """Handle save action"""
        logger.info("Save action triggered")
    
    def _on_delete(self) -> None:
        """Handle delete action"""
        logger.info("Delete action triggered")
    
    def _on_refresh(self) -> None:
        """Handle refresh action"""
        logger.info("Refresh action triggered")
    
    def _on_nav_item_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        """Handle navigation item click"""
        item_text = item.text(0)
        logger.info(f"Navigation item clicked: {item_text}")
        
        if item_text == "GL Accounts":
            self._on_gl_accounts()
        elif item_text == "SL Accounts":
            self._on_sl_accounts()
        elif item_text == "FS Accounts":
            self._on_fs_accounts()
        elif item_text == "Journal Entry":
            self._on_journal_entry()
        elif item_text == "Journal List":
            self._on_journal_list()
        elif item_text == "Trial Balance":
            self._on_trial_balance()
        elif item_text == "General Ledger":
            self._on_general_ledger()
        elif item_text == "Journal Report":
            self._on_journal_report()
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """Handle window close event"""
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            logger.info("Application closing")
            event.accept()
        else:
            event.ignore()
