# SAWIT GO - TSJ - Project Specification

**Versi:** 1.0  
**Tanggal:** 2026-03-31  
**Status:** ✅ READY FOR IMPLEMENTATION  
**Owner:** Syafriadi  

> **"Sistem Akuntansi Modern untuk Perkebunan Sawit - Ringan, Fleksibel, dan Bisa Jalan di Mana Saja"**

---

## Quick Summary

| Info | Value |
|------|-------|
| **Project** | Sawit Go - TSJ |
| **Type** | Desktop Application (.exe) |
| **Tech Stack** | Python 3.10 + PyQt6 + SQLite |
| **Database** | SQLite (fleksibel, bisa export Excel) |
| **Target** | Laptop specs rendah (2GB RAM cukup) |
| **Size Estimate** | ~60-80 MB installer |
| **Update** | Via GitHub Releases |
| **License** | MIT |

---

## Project Overview

**Sawit Go - TSJ** adalah clone modern dari Wisa Accounting System v2.3, dirancang khusus untuk:
- Akuntansi perusahaan perkebunan kelapa sawit (PT Tulas Sakti Jaya)
- Bisa jalan di laptop specs rendah
- Database SQLite yang fleksibel dan bisa export ke Excel
- Single-file .exe installer dengan auto-update

### Key Features (MVP)

1. **Authentication** - Login dengan role-based access
2. **Multi-Company** - Support multiple perusahaan dalam 1 database
3. **Chart of Accounts** - GL Accounts dengan hierarchy tree
4. **Journal Entry** - Double-entry validation (Debit = Kredit)
5. **Trial Balance** - Neraca Saldo dengan filter periode
6. **Excel Export** - Semua data bisa export ke .xlsx
7. **Backup/Restore** - Database backup ke file .db

### Out of Scope (v2)

- Multi-user with server mode
- Cloud sync
- Payroll module
- Inventory module

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER (PyQt6)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  Views   │  │  Dialogs │  │  Widgets │  │  Menus   │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SERVICE LAYER (Business Logic)               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │AuthService│  │GLService │  │RptService│  │ExpService│     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER (SQLAlchemy)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  Models  │  │ Queries  │  │ Migrations│  │ Repos     │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE (SQLite: gl.db)                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Database Schema (11 Tables)

```sql
┌─────────────────────────────────────────────────────────────────┐
│                         CORE TABLES                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  company ──────────────┬───────────────────                    │
│  (Perusahaan)          │ 1:N                                     │
│  ├─ id, code, name    │                                         │
│  ├─ address, phone    │                                         │
│  └─ npwp, logo       │                                         │
│                         ▼                                         │
│  "user" ──────────────┼───────────────────                    │
│  (User/Akun)          │ 1:N                                     │
│  ├─ id, username       │                                         │
│  ├─ password_hash     │                                         │
│  ├─ role (ADMIN/USER│                                         │
│  └─ is_active         │                                         │
│                         ▼                                         │
│  gl_account ──────────────────────────────────────────           │
│  (Buku Besar)         │                                         │
│  ├─ id, code, name   │ Self-ref FK                             │
│  ├─ parent_id ────────┼─────────────┐                           │
│  ├─ level, type      │             │                           │
│  └─ normal_balance    │             │                           │
│                         │             │                           │
│                         ▼             │                           │
│  journal_header ──────┴─────────────┤                           │
│  (Header Jurnal)    │                 │                           │
│  ├─ id, journal_no   │                 │                           │
│  ├─ date, reference  │                 │                           │
│  ├─ description      │                 │                           │
│  └─ status           │                 │                           │
│                         │                 │                           │
│                         ▼                 │                           │
│  journal_line ─────────┴─────────────────┘                           │
│  (Baris Jurnal)                                                  │
│  ├─ id, header_id                                                 │
│  ├─ account_id ──────────────────────────────────────► gl_account│
│  ├─ debit, credit                                                │
│  └─ description                                                  │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                         SUPPORT TABLES                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  period        - Accounting Period (bulan/tahun)              │
│  fs_account    - Financial Statement Account mapping             │
│  fs_element    - FS Elements (Assets, Liabilities, etc.)        │
│  sl_account    - Subsidiary Ledger (Buku Pembantu)             │
│  audit_log     - Audit trail (CREATE/UPDATE/DELETE)            │
│  settings      - Application settings (key-value)              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Table Relationships

```
company (1) ─────┬───── (N) "user"
                  │
                  ├───── (N) gl_account
                  │
                  ├───── (N) journal_header
                  │
                  ├───── (N) period
                  │
                  ├───── (N) fs_account
                  │
                  ├───── (N) fs_element
                  │
                  └───── (N) sl_account

journal_header (1) ─── (N) journal_line

gl_account (1) ──────┬───── (N) journal_line
                       │
                       └───── (N) sl_account
```

---

## Module Structure

```
sawit-go-tsj/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── app.py                 # Application class (PyQt6)
│   │
│   ├── ui/                    # Presentation Layer
│   │   ├── main_window.py     # Main window + navigation
│   │   ├── login_dialog.py   # Login form
│   │   ├── views/            # Screen views
│   │   │   ├── gl_accounts_view.py
│   │   │   ├── journal_entry_view.py
│   │   │   ├── journal_list_view.py
│   │   │   ├── trial_balance_view.py
│   │   │   └── ...
│   │   ├── widgets/          # Reusable widgets
│   │   │   ├── tree_model.py
│   │   │   ├── table_model.py
│   │   │   └── form_widget.py
│   │   └── dialogs/         # Dialogs
│   │       ├── confirm_dialog.py
│   │       └── error_dialog.py
│   │
│   ├── services/            # Service Layer
│   │   ├── base_service.py   # Base CRUD + transaction
│   │   ├── auth_service.py   # Login/logout
│   │   ├── company_service.py
│   │   ├── gl_account_service.py
│   │   ├── journal_service.py
│   │   ├── report_service.py
│   │   ├── export_service.py # Excel/CSV/PDF
│   │   └── backup_service.py
│   │
│   ├── models/              # Data Layer - ORM Models
│   │   ├── base.py
│   │   ├── company.py
│   │   ├── user.py
│   │   ├── gl_account.py
│   │   ├── journal.py
│   │   ├── period.py
│   │   ├── fs_account.py
│   │   ├── sl_account.py
│   │   ├── audit_log.py
│   │   └── settings.py
│   │
│   ├── repositories/        # Data Access Layer
│   │   ├── base_repository.py
│   │   ├── company_repository.py
│   │   ├── user_repository.py
│   │   ├── account_repository.py
│   │   └── journal_repository.py
│   │
│   ├── database/            # Database Configuration
│   │   ├── connection.py
│   │   ├── session.py
│   │   └── migrations/
│   │
│   ├── utils/               # Utilities
│   │   ├── validators.py
│   │   ├── formatters.py
│   │   ├── crypto.py
│   │   ├── exceptions.py
│   │   └── update_checker.py
│   │
│   └── config/             # Configuration
│       ├── settings.py
│       └── constants.py
│
├── tests/                   # Unit Tests (pytest)
│   ├── test_auth_service.py
│   ├── test_gl_account_service.py
│   ├── test_journal_service.py
│   └── test_report_service.py
│
├── resources/              # Static Resources
│   ├── icons/
│   └── styles/
│
├── docs/                   # Documentation
│   ├── PRD.md             # Product Requirements
│   ├── FSD.md            # Functional Specification
│   ├── TSD.md            # Technical Specification
│   ├── TASK_LIST.md      # Task Breakdown
│   └── IMPLEMENTATION_PLAN.md
│
├── scripts/               # Build Scripts
│   ├── build_exe.py      # PyInstaller config
│   └── create_installer.py
│
├── .github/               # GitHub Actions
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
│
├── requirements.txt
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── LICENSE
└── .gitignore
```

---

## Task Breakdown (35 Tasks)

### Phase 1: Foundation (Week 1-2) - 8 Tasks

| ID | Task | Hours | Status |
|----|------|-------|--------|
| T-101 | Setup Python project + venv | 2 | TODO |
| T-102 | Initialize Git repo + .gitignore | 1 | TODO |
| T-103 | Create project structure | 1 | TODO |
| T-104 | Install dependencies | 1 | TODO |
| T-110 | Create SQLAlchemy base model | 2 | TODO |
| T-111 | Create all ORM models (11 tables) | 4 | TODO |
| T-120 | Implement BaseService + UnitOfWork | 4 | TODO |
| T-130 | Create Main Window (PyQt6) | 4 | TODO |

### Phase 2: Core Modules (Week 3-5) - 12 Tasks

| ID | Task | Hours | Status |
|----|------|-------|--------|
| T-201 | AuthService + password hashing | 4 | TODO |
| T-202 | Login Dialog UI | 3 | TODO |
| T-210 | CompanyService + Period management | 4 | TODO |
| T-220 | GLAccountService (CRUD + hierarchy) | 4 | TODO |
| T-221 | GL Accounts View (tree + form) | 6 | TODO |
| T-230 | JournalService (CRUD + validation) | 5 | TODO |
| T-231 | Journal Entry View (lines table) | 8 | TODO |
| T-232 | Journal List View (search/filter) | 4 | TODO |
| T-240 | SLAccountService + View | 4 | TODO |
| T-250 | FSAccountService + View | 4 | TODO |
| T-260 | Company Settings View | 3 | TODO |
| T-270 | Audit Log View | 2 | TODO |

### Phase 3: Reporting (Week 6-7) - 8 Tasks

| ID | Task | Hours | Status |
|----|------|-------|--------|
| T-301 | ReportService base | 2 | TODO |
| T-302 | Trial Balance Report | 4 | TODO |
| T-303 | General Ledger Report | 4 | TODO |
| T-304 | Journal Report | 3 | TODO |
| T-310 | ExportService (Excel/CSV/PDF) | 4 | TODO |
| T-311 | Excel Export Implementation | 4 | TODO |
| T-320 | Balance Sheet Report | 4 | TODO |
| T-330 | Profit & Loss Report | 4 | TODO |

### Phase 4: Polish & Release (Week 8) - 7 Tasks

| ID | Task | Hours | Status |
|----|------|-------|--------|
| T-401 | Backup/Restore Service | 3 | TODO |
| T-402 | Settings Module | 2 | TODO |
| T-410 | PyInstaller configuration | 4 | TODO |
| T-411 | Auto-Update via GitHub | 4 | TODO |
| T-420 | GitHub Actions CI/CD | 3 | TODO |
| T-430 | README + Documentation | 2 | TODO |
| T-440 | Final Testing + Release | 4 | TODO |

**Total: 80 hours across 35 tasks**

---

## Implementation Timeline

```
Week 1-2: FOUNDATION (16h)
├── T-101 to T-104: Setup (5h)
├── T-110 to T-111: Models (6h)
└── T-120, T-130: Architecture + UI (5h)

Week 3-5: CORE MODULES (32h)
├── T-201 to T-202: Auth (7h)
├── T-210: Company + Period (4h)
├── T-220 to T-221: GL Accounts (10h)
└── T-230 to T-270: Journal + SL + FS (11h)

Week 6-7: REPORTING (24h)
├── T-301: Report base (2h)
├── T-302 to T-304: Core reports (11h)
└── T-310 to T-330: Export + FS reports (11h)

Week 8: POLISH & RELEASE (8h)
├── T-401 to T-402: Utilities (5h)
├── T-410 to T-420: Distribution (7h)
└── T-430 to T-440: Docs + Release (6h)
```

---

## GitHub Workflow

### Branch Strategy

```
main (production)
  │
  ├── develop (development)
  │     │
  │     ├── feature/auth
  │     ├── feature/gl-accounts
  │     ├── feature/journal
  │     ├── feature/reports
  │     └── feature/installer
  │
  └── release/v1.0.0
```

### Auto-Update Flow

```
User launches app
        │
        ▼
┌──────────────────┐
│ Check for Updates │ (GitHub API)
└────────┬─────────┘
         │
    ┌────┴────┐
    │New ver? │
    └────┬────┘
     Yes │ No
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌─────────┐
│ Show    │ │ Continue│
│ Dialog  │ │ to App  │
└────┬────┘ └─────────┘
     │
     ▼
┌─────────────────┐
│ Download new    │ (from GitHub Release)
│ version         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Launch installer│ + Exit app
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Done! New ver  │
└─────────────────┘
```

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 7 64-bit | Windows 10/11 64-bit |
| **CPU** | Intel Celeron / AMD A4 | Intel i3 / Ryzen 3 |
| **RAM** | 2 GB | 4 GB |
| **Storage** | 100 MB free | 500 MB free |
| **Display** | 1024x768 | 1920x1080 |

---

## Dependencies

```txt
# Core
PyQt6>=6.4.0
SQLAlchemy>=2.0.0
Alembic>=1.11.0

# Export
openpyxl>=3.1.0
pandas>=2.0.0
reportlab>=4.0.0

# Security
bcrypt>=4.0.0

# Utils
loguru>=0.7.0
python-dateutil>=2.8.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0

# Code Quality
ruff>=0.1.0

# Distribution
pyinstaller>=6.0.0
```

---

## Deliverables

| Document | File | Status |
|----------|------|--------|
| ✅ Product Requirements | [PRD.md](docs/PRD.md) | Complete |
| ✅ Functional Specification | [FSD.md](docs/FSD.md) | Complete |
| ✅ Technical Specification | [TSD.md](docs/TSD.md) | Complete |
| ✅ Task List | [TASK_LIST.md](docs/TASK_LIST.md) | Complete |
| ✅ Implementation Plan | [IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) | Complete |
| ✅ **SPEC.md (This file)** | [SPEC.md](SPEC.md) | **Current** |
| 🔜 README | README.md | Next |
| 🔜 CHANGELOG | CHANGELOG.md | Per release |

---

## Questions for Owner

```
□ 1. Apakah ada template Chart of Accounts spesifik untuk perkebunan sawit?
□ 2. Format nomor jurnal apa yang preferred? (e.g., JRN-2026-001)
□ 3. Apakah perlu integration dengan sistem lain (payroll, inventory)?
□ 4. Target user primarily di lapangan atau kantor?
□ 5. Bahasa UI: Indonesia atau English?
□ 6. Sudah ada GitHub account untuk repository?
```

---

## Next Steps

```
□ 1. Owner review & approve spec
□ 2. Create GitHub repository (sawit-go-tsj)
□ 3. Push all docs to GitHub
□ 4. Start Phase 1: Foundation
   □ Initialize project
   □ Create database models
   □ Build main window
□ 5. Continue until v1.0.0 release
```

---

**Document Status:** ✅ READY FOR IMPLEMENTATION

**Owner Approval:** _____________ (Syafriadi)

**Developer:** AI Assistant (Trae)

**Date:** 2026-03-31
