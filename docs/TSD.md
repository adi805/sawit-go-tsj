# WISA-CLONE - Technical Specification Document (TSD)

**Versi:** 1.0  
**Tanggal:** 2026-03-31  
**Status:** Draft  
**Author:** AI Assistant  

---

## 1. Overview

### 1.1 Purpose
Dokumen ini menjelaskan spesifikasi teknis aplikasi WISA-CLONE, termasuk:
- Database Schema (SQLite)
- API/Service Layer Design
- Architecture Pattern
- Technology Stack Details

### 1.2 Architecture Pattern
**Layered Architecture** dengan Service-Oriented Design

```
┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                          │
│                        (PyQt6 GUI)                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  Views   │  │  Dialogs │  │  Widgets │  │  Menus   │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SERVICE LAYER                              │
│                    (Business Logic)                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │AuthService│  │GLService │  │RptService│  │ExpService│     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                 │
│                    (SQLAlchemy ORM)                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  Models  │  │ Queries  │  │ Migrations│ │ Repos    │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE (SQLite)                             │
│                         gl.db                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Database Schema

### 2.1 Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           WISA-CLONE DATABASE SCHEMA                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Company    │         │    User       │         │  GLAccount   │
├──────────────┤         ├──────────────┤         ├──────────────┤
│ PK id       │         │ PK id         │         │ PK id        │
│    name     │         │ FK company_id │         │ FK company_id│◄───┐
│    address  │         │    username   │         │    code      │    │
│    phone    │         │    password   │         │    name      │    │
│    email    │         │    role       │         │ FK parent_id │────┤
│    NPWP     │         │    is_active  │         │    level     │    │
│    logo     │         │    created   │         │    type      │    │
└──────┬───────┘         └──────┬───────┘         └──────┬───────┘    │
       │                          │                        │              │
       │ 1:N                      │ 1:N                    │ 1:N          │
       ▼                          ▼                        ▼              │
┌──────────────┐         ┌──────────────┐         ┌──────────────┐      │
│   Period     │         │    AuditLog  │         │ JournalHeader│──────┘
├──────────────┤         ├──────────────┤         ├──────────────┤
│ PK id        │         │ PK id        │         │ PK id        │
│ FK company_id │◄───────┤ FK user_id   │         │ FK company_id │◄───┐
│    year      │         │    table     │         │ FK period_id  │    │
│    month     │         │    record_id │         │    journal_no │    │
│    start_date│         │    action    │         │    date       │    │
│    end_date  │         │    old_data  │         │ FK reference  │    │
│    is_closed │         │    new_data  │         │    desc       │    │
└──────────────┘         │    timestamp │         │    notes      │    │
       │                  └──────────────┘         │    status     │    │
       │                                           └───────┬───────┘    │
       │                                                   │            │
       │                                                   │ 1:N        │
       │                                                   ▼            │
       │                                          ┌──────────────┐      │
       │                                          │ JournalLine  │      │
       │                                          ├──────────────┤      │
       └──────────────────────────────────────────│ PK id        │      │
                                                   │ FK header_id │◄─────┘
                                                   │ FK account_id│─────┘
                                                   │    debit     │
                                                   │    credit    │
                                                   │    desc      │
                                                   └──────────────┘

┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│  FSAccount   │         │ SLAccount    │         │ FSElement    │
├──────────────┤         ├──────────────┤         ├──────────────┤
│ PK id        │         │ PK id        │         │ PK id        │
│ FK company_id │◄───┐   │ FK company_id │◄───┐   │ FK company_id │◄───┐
│    code      │    │   │ FK GLAccountID│    │   │    code      │    │
│    name      │    │   │    name      │    │   │    name      │    │
│ FK element_id│────┘   │    type      │    │   │    category  │    │
│    position │         └──────────────┘    │   │    statement │    │
└──────────────┘                             │   └──────────────┘    │
       ▲                                     │           ▲           │
       │                                     │           │           │
       │         ┌──────────────┐            │           │           │
       └─────────┤AccountMapping│────────────┴───────────┘           │
                 ├──────────────┤                                             │
                 │ PK id        │                                             │
                 │FK gl_account │                                             │
                 │FK fs_account │                                             │
                 └──────────────┘                                             │
```

### 2.2 Database Schema (SQLite SQL)

```sql
-- ============================================================
-- WISA-CLONE Database Schema
-- SQLite 3.x compatible
-- Generated: 2026-03-31
-- ============================================================

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- ============================================================
-- TABLE: Company
-- Description: Multi-company support
-- ============================================================
CREATE TABLE company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    npwp VARCHAR(25),
    logo BLOB,
    fiscal_year_start INTEGER DEFAULT 1,
    currency_code VARCHAR(3) DEFAULT 'IDR',
    decimal_places INTEGER DEFAULT 2,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_company_code ON company(code);

-- ============================================================
-- TABLE: User
-- Description: Application users with role-based access
-- ============================================================
CREATE TABLE "user" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100),
    role VARCHAR(20) DEFAULT 'USER' CHECK(role IN ('ADMIN', 'USER', 'VIEWER')),
    is_active BOOLEAN DEFAULT 1,
    last_login DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
);

CREATE INDEX idx_user_company ON "user"(company_id);
CREATE INDEX idx_user_username ON "user"(username);

-- ============================================================
-- TABLE: GLAccount
-- Description: Chart of Accounts - General Ledger Accounts
-- ============================================================
CREATE TABLE gl_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    code VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,
    parent_id INTEGER,
    level INTEGER DEFAULT 0,
    account_type VARCHAR(20) DEFAULT 'DETAIL' CHECK(account_type IN ('HEADER', 'DETAIL')),
    normal_balance VARCHAR(10) DEFAULT 'DEBIT' CHECK(normal_balance IN ('DEBIT', 'CREDIT')),
    is_active BOOLEAN DEFAULT 1,
    allow_entry BOOLEAN DEFAULT 1,
    show_in_trial_balance BOOLEAN DEFAULT 1,
    fs_account_id INTEGER,
    initial_balance DECIMAL(18,4) DEFAULT 0,
    currency_code VARCHAR(3) DEFAULT 'IDR',
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES gl_account(id) ON DELETE SET NULL,
    FOREIGN KEY (fs_account_id) REFERENCES fs_account(id) ON DELETE SET NULL
);

CREATE UNIQUE INDEX idx_gl_account_code ON gl_account(company_id, code);
CREATE INDEX idx_gl_account_parent ON gl_account(parent_id);
CREATE INDEX idx_gl_account_type ON gl_account(account_type);

-- ============================================================
-- TABLE: FSAccount
-- Description: Financial Statement Account mapping
-- ============================================================
CREATE TABLE fs_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    code VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,
    fs_element_id INTEGER,
    statement_type VARCHAR(20) CHECK(statement_type IN ('BALANCE_SHEET', 'INCOME')),
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (fs_element_id) REFERENCES fs_element(id) ON DELETE SET NULL
);

CREATE UNIQUE INDEX idx_fs_account_code ON fs_account(company_id, code);

-- ============================================================
-- TABLE: FSElement
-- Description: Financial Statement Elements (Assets, Liabilities, etc.)
-- ============================================================
CREATE TABLE fs_element (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    code VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    statement_type VARCHAR(20) CHECK(statement_type IN ('BALANCE_SHEET', 'INCOME')),
    position VARCHAR(10) CHECK(position IN ('DEBIT', 'CREDIT', 'CALCULATE')),
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX idx_fs_element_code ON fs_element(company_id, code);

-- ============================================================
-- TABLE: SLAccount
-- Description: Subsidiary Ledger Accounts (Buku Pembantu)
-- ============================================================
CREATE TABLE sl_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    gl_account_id INTEGER NOT NULL,
    code VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100),
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    tax_id VARCHAR(25),
    credit_limit DECIMAL(18,4),
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (gl_account_id) REFERENCES gl_account(id) ON DELETE RESTRICT
);

CREATE UNIQUE INDEX idx_sl_account_code ON sl_account(company_id, gl_account_id, code);

-- ============================================================
-- TABLE: Period
-- Description: Accounting Period management
-- ============================================================
CREATE TABLE period (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL CHECK(month BETWEEN 1 AND 12),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_closed BOOLEAN DEFAULT 0,
    closed_by INTEGER,
    closed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (closed_by) REFERENCES "user"(id),
    UNIQUE(company_id, year, month)
);

CREATE INDEX idx_period_company ON period(company_id, year, month);

-- ============================================================
-- TABLE: JournalHeader
-- Description: Journal Entry Header
-- ============================================================
CREATE TABLE journal_header (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    journal_no VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    reference VARCHAR(50),
    description TEXT,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'POSTED' CHECK(status IN ('DRAFT', 'POSTED', 'VOID')),
    source_type VARCHAR(30),
    source_id INTEGER,
    created_by INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (period_id) REFERENCES period(id) ON DELETE RESTRICT,
    FOREIGN KEY (created_by) REFERENCES "user"(id)
);

CREATE UNIQUE INDEX idx_journal_no ON journal_header(company_id, journal_no);
CREATE INDEX idx_journal_date ON journal_header(company_id, date);
CREATE INDEX idx_journal_period ON journal_header(period_id);

-- ============================================================
-- TABLE: JournalLine
-- Description: Journal Entry Line Items
-- ============================================================
CREATE TABLE journal_line (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    header_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    sl_account_id INTEGER,
    debit DECIMAL(18,4) DEFAULT 0,
    credit DECIMAL(18,4) DEFAULT 0,
    description VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (header_id) REFERENCES journal_header(id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES gl_account(id) ON DELETE RESTRICT,
    FOREIGN KEY (sl_account_id) REFERENCES sl_account(id) ON DELETE SET NULL,
    CHECK (debit >= 0 AND credit >= 0),
    CHECK (debit = 0 OR credit = 0)
);

CREATE INDEX idx_journal_line_header ON journal_line(header_id);
CREATE INDEX idx_journal_line_account ON journal_line(account_id);

-- ============================================================
-- TABLE: AuditLog
-- Description: Audit trail for all database changes
-- ============================================================
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    user_id INTEGER NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(20) NOT NULL CHECK(action IN ('CREATE', 'UPDATE', 'DELETE')),
    old_data TEXT,
    new_data TEXT,
    ip_address VARCHAR(45),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);

CREATE INDEX idx_audit_company ON audit_log(company_id);
CREATE INDEX idx_audit_table ON audit_log(table_name, record_id);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp);

-- ============================================================
-- TABLE: Settings
-- Description: Application settings
-- ============================================================
CREATE TABLE settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    setting_key VARCHAR(100) NOT NULL,
    setting_value TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    UNIQUE(company_id, setting_key)
);

-- ============================================================
-- Default Settings
-- ============================================================
INSERT INTO settings (company_id, setting_key, setting_value) VALUES
    (1, 'COMPANY_NAME', 'Default Company'),
    (1, 'DATE_FORMAT', 'DD/MM/YYYY'),
    (1, 'DECIMAL_SEPARATOR', ','),
    (1, 'THOUSAND_SEPARATOR', '.'),
    (1, 'CURRENCY_SYMBOL', 'Rp');
```

---

## 3. Database Schema Diagram (DBML Format)

### 3.1 DBML Schema

```dbml
// WISA-CLONE Database Schema
// Generated: 2026-03-31

Table company {
  id integer [primary key, not null]
  code varchar(10) [unique, not null]
  name varchar(200) [not null]
  address text
  phone varchar(20)
  email varchar(100)
  npwp varchar(25)
  logo blob
  fiscal_year_start integer [default: 1]
  currency_code varchar(3) [default: 'IDR']
  decimal_places integer [default: 2]
  is_active boolean [default: true]
  created_at datetime
  updated_at datetime
}

Table "user" {
  id integer [primary key, not null]
  company_id integer [not null, ref: > company.id]
  username varchar(50) [unique, not null]
  password_hash varchar(255) [not null]
  full_name varchar(100)
  email varchar(100)
  role varchar(20) [default: 'USER']
  is_active boolean [default: true]
  last_login datetime
  created_at datetime
  updated_at datetime
}

Table gl_account {
  id integer [primary key, not null]
  company_id integer [not null, ref: > company.id]
  code varchar(20) [not null]
  name varchar(200) [not null]
  parent_id integer [ref: > gl_account.id]
  level integer [default: 0]
  account_type varchar(20) [default: 'DETAIL']
  normal_balance varchar(10) [default: 'DEBIT']
  is_active boolean [default: true]
  allow_entry boolean [default: true]
  show_in_trial_balance boolean [default: true]
  fs_account_id integer [ref: > fs_account.id]
  initial_balance decimal(18,4) [default: 0]
  currency_code varchar(3) [default: 'IDR']
  description text
  created_at datetime
  updated_at datetime
  
  indexes {
    (company_id, code) [unique]
    parent_id
  }
}

Table fs_account {
  id integer [primary key, not null]
  company_id integer [not null, ref: > company.id]
  code varchar(20) [not null]
  name varchar(200) [not null]
  fs_element_id integer [ref: > fs_element.id]
  statement_type varchar(20)
  display_order integer [default: 0]
  is_active boolean [default: true]
  created_at datetime
  updated_at datetime
  
  indexes {
    (company_id, code) [unique]
  }
}

Table fs_element {
  id integer [primary key, not null]
  company_id integer [not null, ref: > company.id]
  code varchar(10) [not null]
  name varchar(100) [not null]
  category varchar(50)
  statement_type varchar(20)
  position varchar(10)
  display_order integer [default: 0]
  is_active boolean [default: true]
  created_at datetime
  updated_at datetime
  
  indexes {
    (company_id, code) [unique]
  }
}

Table sl_account {
  id integer [primary key, not null]
  company_id integer [not null, ref: > company.id]
  gl_account_id integer [not null, ref: > gl_account.id]
  code varchar(20) [not null]
  name varchar(200) [not null]
  contact_person varchar(100)
  address text
  phone varchar(20)
  email varchar(100)
  tax_id varchar(25)
  credit_limit decimal(18,4)
  is_active boolean [default: true]
  created_at datetime
  updated_at datetime
  
  indexes {
    (company_id, gl_account_id, code) [unique]
  }
}

Table period {
  id integer [primary key, not null]
  company_id integer [not null, ref: > company.id]
  year integer [not null]
  month integer [not null]
  start_date date [not null]
  end_date date [not null]
  is_closed boolean [default: false]
  closed_by integer [ref: > user.id]
  closed_at datetime
  created_at datetime
  
  indexes {
    (company_id, year, month) [unique]
  }
}

Table journal_header {
  id integer [primary key, not null]
  company_id integer [not null, ref: > company.id]
  period_id integer [not null, ref: > period.id]
  journal_no varchar(20) [not null]
  date date [not null]
  reference varchar(50)
  description text
  notes text
  status varchar(20) [default: 'POSTED']
  source_type varchar(30)
  source_id integer
  created_by integer [not null, ref: > user.id]
  created_at datetime
  updated_at datetime
  
  indexes {
    (company_id, journal_no) [unique]
    date
    period_id
  }
}

Table journal_line {
  id integer [primary key, not null]
  header_id integer [not null, ref: > journal_header.id]
  account_id integer [not null, ref: > gl_account.id]
  sl_account_id integer [ref: > sl_account.id]
  debit decimal(18,4) [default: 0]
  credit decimal(18,4) [default: 0]
  description varchar(200)
  created_at datetime
  
  indexes {
    header_id
    account_id
  }
}

Table audit_log {
  id integer [primary key, not null]
  company_id integer [ref: > company.id]
  user_id integer [not null, ref: > user.id]
  table_name varchar(50) [not null]
  record_id integer [not null]
  action varchar(20) [not null]
  old_data text
  new_data text
  ip_address varchar(45)
  timestamp datetime
  
  indexes {
    company_id
    (table_name, record_id)
  }
}

Table settings {
  id integer [primary key, not null]
  company_id integer [not null, ref: > company.id]
  setting_key varchar(100) [not null]
  setting_value text
  updated_at datetime
  
  indexes {
    (company_id, setting_key) [unique]
  }
}
```

---

## 4. Service Layer Design

### 4.1 Service Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SERVICE LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    BaseService                             │  │
│  │  - Common CRUD operations                                 │  │
│  │  - Transaction management                                 │  │
│  │  - Audit logging                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│         ┌────────────────────┼────────────────────┐            │
│         │                    │                    │            │
│         ▼                    ▼                    ▼            │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐    │
│  │ AuthService │      │  GLService  │      │ReportService│    │
│  ├─────────────┤      ├─────────────┤      ├─────────────┤    │
│  │ login()     │      │get_accounts │      │trial_balance│    │
│  │ logout()   │      │create_acc() │      │general_ledger│    │
│  │ register()  │      │update_acc() │      │balance_sheet│    │
│  │ change_pwd()│      │delete_acc() │      │profit_loss  │    │
│  └─────────────┘      │get_balance()│      └─────────────┘    │
│                        └─────────────┘                            │
│                              │                                     │
│                              ▼                                     │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐    │
│  │JournalService│     │SLService    │      │ExportService│    │
│  ├─────────────┤      ├─────────────┤      ├─────────────┤    │
│  │create_journal│     │get_sl_acc() │      │to_excel()   │    │
│  │post_journal()│     │create_sl()  │      │to_csv()     │    │
│  │void_journal()│     │link_sl()    │      │to_pdf()     │    │
│  │get_journals()│     └─────────────┘      └─────────────┘    │
│  └─────────────┘                                                   │
│                              │                                     │
│                              ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                   BackupService                           │    │
│  │  - backup()                                              │    │
│  │  - restore()                                             │    │
│  │  - vacuum()                                              │    │
│  └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Service Interface Definitions

#### 4.2.1 AuthenticationService

```python
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class LoginResult:
    success: bool
    user_id: Optional[int] = None
    username: Optional[str] = None
    role: Optional[str] = None
    company_id: Optional[int] = None
    message: str = ""

class AuthenticationService:
    """Handles user authentication and session management"""
    
    def login(self, username: str, password: str) -> LoginResult:
        """
        Authenticate user with username and password.
        
        Args:
            username: User's username
            password: User's password (plain text, will be hashed)
            
        Returns:
            LoginResult with success status and user info
        """
        pass
    
    def logout(self, user_id: int) -> bool:
        """
        Logout user and clear session.
        
        Args:
            user_id: ID of user to logout
            
        Returns:
            True if successful
        """
        pass
    
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
        pass
    
    def create_user(self, company_id: int, username: str, password: str, 
                    full_name: str, role: str = "USER") -> Optional[int]:
        """
        Create new user account.
        
        Args:
            company_id: Company ID
            username: Username
            password: Password (will be hashed)
            full_name: Full name
            role: User role (ADMIN, USER, VIEWER)
            
        Returns:
            New user ID if successful
        """
        pass
    
    def validate_session(self, user_id: int, session_token: str) -> bool:
        """
        Validate user session token.
        
        Args:
            user_id: User ID
            session_token: Session token to validate
            
        Returns:
            True if valid
        """
        pass
```

#### 4.2.2 GLAccountService

```python
from typing import List, Optional, Dict, Any
from decimal import Decimal

@dataclass
class GLAccountDTO:
    id: int
    code: str
    name: str
    parent_id: Optional[int]
    level: int
    account_type: str
    normal_balance: str
    is_active: bool
    allow_entry: bool
    show_in_trial_balance: bool
    fs_account_id: Optional[int]
    initial_balance: Decimal
    balance: Decimal = Decimal('0')

class GLAccountService:
    """Handles General Ledger Account operations"""
    
    def get_accounts(self, company_id: int, 
                      include_inactive: bool = False,
                      parent_id: Optional[int] = None) -> List[GLAccountDTO]:
        """
        Get all GL accounts for a company.
        
        Args:
            company_id: Company ID
            include_inactive: Include inactive accounts
            parent_id: Filter by parent account
            
        Returns:
            List of GLAccountDTO
        """
        pass
    
    def get_account_by_id(self, account_id: int) -> Optional[GLAccountDTO]:
        """
        Get account by ID.
        
        Args:
            account_id: Account ID
            
        Returns:
            GLAccountDTO or None
        """
        pass
    
    def create_account(self, company_id: int, code: str, name: str,
                       parent_id: Optional[int] = None,
                       account_type: str = "DETAIL",
                       normal_balance: str = "DEBIT",
                       **kwargs) -> Optional[int]:
        """
        Create new GL account.
        
        Args:
            company_id: Company ID
            code: Account code
            name: Account name
            parent_id: Parent account ID
            account_type: HEADER or DETAIL
            normal_balance: DEBIT or CREDIT
            
        Returns:
            New account ID
        """
        pass
    
    def update_account(self, account_id: int, **kwargs) -> bool:
        """
        Update GL account.
        
        Args:
            account_id: Account ID
            **kwargs: Fields to update
            
        Returns:
            True if successful
        """
        pass
    
    def delete_account(self, account_id: int) -> bool:
        """
        Delete GL account.
        
        Args:
            account_id: Account ID
            
        Returns:
            True if successful
        """
        pass
    
    def get_account_balance(self, account_id: int, 
                           end_date: Optional[date] = None) -> Decimal:
        """
        Calculate account balance.
        
        Args:
            account_id: Account ID
            end_date: Calculate up to this date
            
        Returns:
            Account balance
        """
        pass
    
    def get_account_tree(self, company_id: int) -> List[Dict]:
        """
        Get account tree structure.
        
        Args:
            company_id: Company ID
            
        Returns:
            Hierarchical account tree
        """
        pass
```

#### 4.2.3 JournalService

```python
from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import date

@dataclass
class JournalLineDTO:
    account_id: int
    account_code: str
    account_name: str
    debit: Decimal
    credit: Decimal
    description: Optional[str] = None
    sl_account_id: Optional[int] = None

@dataclass
class JournalDTO:
    id: int
    journal_no: str
    date: date
    reference: Optional[str]
    description: str
    lines: List[JournalLineDTO]
    total_debit: Decimal
    total_credit: Decimal
    status: str
    created_by: str
    created_at: datetime

class JournalService:
    """Handles Journal Entry operations"""
    
    def create_journal(self, company_id: int, user_id: int,
                       date: date, description: str,
                       lines: List[Dict[str, Any]],
                       reference: Optional[str] = None,
                       notes: Optional[str] = None) -> Optional[int]:
        """
        Create new journal entry.
        
        Args:
            company_id: Company ID
            user_id: Creating user ID
            date: Journal date
            description: Journal description
            lines: List of line items
            reference: Reference number
            notes: Additional notes
            
        Returns:
            New journal ID
            
        Raises:
            ValidationError: If journal is invalid
        """
        pass
    
    def post_journal(self, journal_id: int) -> bool:
        """
        Post journal entry.
        
        Args:
            journal_id: Journal ID
            
        Returns:
            True if successful
        """
        pass
    
    def void_journal(self, journal_id: int, reason: str, user_id: int) -> bool:
        """
        Void journal entry.
        
        Args:
            journal_id: Journal ID
            reason: Reason for voiding
            user_id: User performing void
            
        Returns:
            True if successful
        """
        pass
    
    def get_journal(self, journal_id: int) -> Optional[JournalDTO]:
        """
        Get journal by ID.
        
        Args:
            journal_id: Journal ID
            
        Returns:
            JournalDTO or None
        """
        pass
    
    def get_journals(self, company_id: int,
                     start_date: Optional[date] = None,
                     end_date: Optional[date] = None,
                     status: Optional[str] = None,
                     account_id: Optional[int] = None) -> List[JournalDTO]:
        """
        Get journals with filters.
        
        Args:
            company_id: Company ID
            start_date: Filter start date
            end_date: Filter end date
            status: Filter by status
            account_id: Filter by account
            
        Returns:
            List of JournalDTO
        """
        pass
    
    def get_next_journal_no(self, company_id: int, period_id: int) -> str:
        """
        Generate next journal number.
        
        Args:
            company_id: Company ID
            period_id: Period ID
            
        Returns:
            Next journal number
        """
        pass
```

#### 4.2.4 ReportService

```python
from typing import List, Dict, Any, Optional
from decimal import Decimal
from datetime import date

@dataclass
class TrialBalanceItem:
    account_code: str
    account_name: str
    level: int
    debit: Decimal
    credit: Decimal
    is_header: bool

@dataclass
class TrialBalanceResult:
    company_name: str
    period: str
    items: List[TrialBalanceItem]
    total_debit: Decimal
    total_credit: Decimal
    is_balanced: bool
    generated_at: datetime

class ReportService:
    """Handles Financial Report generation"""
    
    def get_trial_balance(self, company_id: int,
                           start_date: date,
                           end_date: date) -> TrialBalanceResult:
        """
        Generate Trial Balance report.
        
        Args:
            company_id: Company ID
            start_date: Period start date
            end_date: Period end date
            
        Returns:
            TrialBalanceResult
        """
        pass
    
    def get_general_ledger(self, company_id: int,
                          account_id: int,
                          start_date: date,
                          end_date: date) -> Dict[str, Any]:
        """
        Generate General Ledger report.
        
        Args:
            company_id: Company ID
            account_id: Account ID
            start_date: Period start date
            end_date: Period end date
            
        Returns:
            General ledger data
        """
        pass
    
    def get_balance_sheet(self, company_id: int,
                         as_of_date: date) -> Dict[str, Any]:
        """
        Generate Balance Sheet report.
        
        Args:
            company_id: Company ID
            as_of_date: Report date
            
        Returns:
            Balance sheet data
        """
        pass
    
    def get_profit_loss(self, company_id: int,
                        start_date: date,
                        end_date: date) -> Dict[str, Any]:
        """
        Generate Profit & Loss report.
        
        Args:
            company_id: Company ID
            start_date: Period start date
            end_date: Period end date
            
        Returns:
            P&L data
        """
        pass
```

---

## 5. Technology Stack Details

### 5.1 Python Version
- **Version:** Python 3.10+ (LTS)
- **Reason:** Modern syntax, good library support, fast

### 5.2 Dependencies

```txt
# requirements.txt

# GUI Framework
PyQt6>=6.4.0

# Database ORM
SQLAlchemy>=2.0.0

# Database Migrations
Alembic>=1.11.0

# Excel Export
openpyxl>=3.1.0
pandas>=2.0.0

# PDF Generation
reportlab>=4.0.0

# Password Hashing
bcrypt>=4.0.0

# Logging
loguru>=0.7.0

# Date/Time
python-dateutil>=2.8.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0

# Code Quality
ruff>=0.1.0

# Packaging
pyinstaller>=6.0.0
```

### 5.3 Project Structure

```
WISA-CLONE/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── app.py                  # Application class
│   │
│   ├── ui/                    # Presentation Layer
│   │   ├── __init__.py
│   │   ├── main_window.py      # Main window
│   │   ├── login_dialog.py     # Login dialog
│   │   │
│   │   ├── views/              # Screen views
│   │   │   ├── __init__.py
│   │   │   ├── gl_accounts_view.py
│   │   │   ├── journal_entry_view.py
│   │   │   ├── trial_balance_view.py
│   │   │   └── ...
│   │   │
│   │   ├── widgets/            # Reusable widgets
│   │   │   ├── __init__.py
│   │   │   ├── table_widget.py
│   │   │   ├── form_widget.py
│   │   │   └── ...
│   │   │
│   │   └── dialogs/           # Dialogs
│   │       ├── __init__.py
│   │       ├── confirm_dialog.py
│   │       └── error_dialog.py
│   │
│   ├── services/              # Service Layer
│   │   ├── __init__.py
│   │   ├── base_service.py     # Base service class
│   │   ├── auth_service.py
│   │   ├── gl_account_service.py
│   │   ├── journal_service.py
│   │   ├── report_service.py
│   │   ├── export_service.py
│   │   └── backup_service.py
│   │
│   ├── models/                # Data Layer - ORM Models
│   │   ├── __init__.py
│   │   ├── base.py             # Base model
│   │   ├── company.py
│   │   ├── user.py
│   │   ├── gl_account.py
│   │   ├── fs_account.py
│   │   ├── sl_account.py
│   │   ├── period.py
│   │   ├── journal.py
│   │   └── audit_log.py
│   │
│   ├── repositories/           # Data Layer - Data Access
│   │   ├── __init__.py
│   │   ├── base_repository.py
│   │   ├── company_repository.py
│   │   ├── user_repository.py
│   │   ├── account_repository.py
│   │   └── journal_repository.py
│   │
│   ├── database/               # Database Configuration
│   │   ├── __init__.py
│   │   ├── connection.py        # DB connection
│   │   ├── session.py           # Session management
│   │   └── migrations/          # Alembic migrations
│   │       ├── env.py
│   │       └── versions/
│   │
│   ├── utils/                  # Utilities
│   │   ├── __init__.py
│   │   ├── validators.py         # Input validation
│   │   ├── formatters.py        # Number/date formatting
│   │   ├── crypto.py            # Password hashing
│   │   └── helpers.py           # Helper functions
│   │
│   └── config/                 # Configuration
│       ├── __init__.py
│       ├── settings.py           # App settings
│       └── constants.py          # Constants
│
├── tests/                      # Unit Tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth_service.py
│   ├── test_gl_account_service.py
│   ├── test_journal_service.py
│   └── test_report_service.py
│
├── resources/                  # Resources
│   ├── icons/
│   ├── styles/
│   └── translations/
│
├── docs/                       # Documentation
│   ├── PRD.md
│   ├── FSD.md
│   ├── TSD.md
│   └── SPEC.md
│
├── data/                       # Runtime data (created at runtime)
│   └── gl.db                   # SQLite database
│
├── build/                      # Build output
│
├── scripts/                   # Build scripts
│   ├── build_exe.py
│   └── create_dist.py
│
├── .gitignore
├── requirements.txt
├── setup.py
├── pyproject.toml
├── README.md
├── CHANGELOG.md
└── LICENSE
```

---

## 6. API Design (Internal Services)

### 6.1 Service Communication Pattern

```python
# Pattern: Service calls Repository (not direct DB access)

┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                JournalEntryView                     │   │
│  │  - user_id_input                                     │   │
│  │  - date_input                                        │   │
│  │  - lines_table                                       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ calls
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      SERVICE LAYER                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 JournalService                      │   │
│  │  - create_journal()                                 │   │
│  │  - validate_journal()                               │   │
│  │  - post_journal()                                   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ calls
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    REPOSITORY LAYER                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │               JournalRepository                     │   │
│  │  - save_header()                                   │   │
│  │  - save_lines()                                    │   │
│  │  - get_by_id()                                     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ uses
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   SQLAlchemy                         │   │
│  │  - JournalHeader model                              │   │
│  │  - JournalLine model                                │   │
│  │  - Query builder                                    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ executes
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATABASE (SQLite)                        │
│                         gl.db                                 │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Transaction Management

```python
from contextlib import contextmanager

class UnitOfWork:
    """Transaction management"""
    
    def __init__(self):
        self.session = None
    
    def __enter__(self):
        self.session = Session()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
            self.session.close()
            return False
        
        self.session.commit()
        self.session.close()
        return True
    
    @contextmanager
    def transaction(self):
        """Nested transaction context"""
        try:
            yield self.session
        except Exception:
            self.session.rollback()
            raise
```

---

## 7. Error Handling

### 7.1 Exception Hierarchy

```python
class WisaCloneException(Exception):
    """Base exception for WISA-CLONE"""
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code or "ERR_UNKNOWN"
        super().__init__(self.message)

class ValidationError(WisaCloneException):
    """Validation errors"""
    def __init__(self, message: str, field: str = None):
        super().__init__(message, "ERR_VALIDATION")
        self.field = field

class DatabaseError(WisaCloneException):
    """Database errors"""
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message, "ERR_DATABASE")
        self.original_error = original_error

class AuthenticationError(WisaCloneException):
    """Authentication errors"""
    def __init__(self, message: str):
        super().__init__(message, "ERR_AUTH")

class AuthorizationError(WisaCloneException):
    """Authorization errors"""
    def __init__(self, message: str):
        super().__init__(message, "ERR_AUTHORIZATION")

class BusinessRuleError(WisaCloneException):
    """Business rule violations"""
    def __init__(self, message: str, rule_id: str = None):
        super().__init__(message, "ERR_BUSINESS_RULE")
        self.rule_id = rule_id
```

---

**Document History:**
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-31 | AI Assistant | Initial draft |
