# WISA-CLONE - Task List & Implementation Plan

**Versi:** 1.0  
**Tanggal:** 2026-03-31  
**Status:** Draft  
**Author:** AI Assistant  

---

## Table of Contents
1. [Project Phases](#1-project-phases)
2. [Phase 1: Foundation (Week 1-2)](#2-phase-1-foundation-week-1-2)
3. [Phase 2: Core Modules (Week 3-5)](#3-phase-2-core-modules-week-3-5)
4. [Phase 3: Reporting (Week 6-7)](#4-phase-3-reporting-week-6-7)
5. [Phase 4: Polish & Distribution (Week 8)](#5-phase-4-polish--distribution-week-8)
6. [Task Breakdown Matrix](#6-task-breakdown-matrix)
7. [GitHub Workflow](#7-github-workflow)

---

## 1. Project Phases

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         WISA-CLONE PROJECT TIMELINE                      │
└─────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: Foundation          │ PHASE 2: Core Modules  │ PHASE 3+4    │
│ Week 1-2                     │ Week 3-5                │ Week 6-8     │
├───────────────────────────────┼────────────────────────┼──────────────┤
│ • Project Setup               │ • Authentication       │ • Reports   │
│ • Database Schema             │ • Company Setup        │ • Export    │
│ • Base Architecture           │ • GL Accounts          │ • Polish    │
│ • UI Framework                │ • SL Accounts          │ • Installer │
│                               │ • Journal Entry        │ • GitHub    │
│                               │ • Basic CRUD           │ • Release   │
└───────────────────────────────┴────────────────────────┴──────────────┘

Total Estimated Time: 8 weeks (with AI assistance)
```

---

## 2. Phase 1: Foundation (Week 1-2)

### 2.1 Task 1.1: Project Setup
| ID | Task | Sub-tasks | Status |
|----|------|-----------|--------|
| T-101 | Initialize Python Project | Create virtual environment | TODO |
| T-102 | Setup Git Repository | Initialize git, create .gitignore | TODO |
| T-103 | Create Project Structure | Create folder structure per TSD | TODO |
| T-104 | Configure Dependencies | Create requirements.txt | TODO |
| T-105 | Setup IDE Configuration | Create pyproject.toml | TODO |

**Detailed Sub-tasks for T-101:**
```
□ 1.1.1 Create project directory
     - mkdir WISA-CLONE
     - cd WISA-CLONE
     
□ 1.1.2 Create virtual environment
     - python -m venv venv
     - venv\Scripts\activate (Windows)
     
□ 1.1.3 Install core dependencies
     - pip install PyQt6
     - pip install sqlalchemy
     - pip install alembic
     - pip install openpyxl pandas
     - pip install bcrypt loguru
     - pip install pytest
     
□ 1.1.4 Verify installation
     - python --version
     - python -c "import PyQt6; print('OK')"
```

### 2.2 Task 1.2: Database Schema Implementation
| ID | Task | Sub-tasks | Status |
|----|------|-----------|--------|
| T-110 | Create Base Model | Implement SQLAlchemy base class | TODO |
| T-111 | Create ORM Models | Create all tables per TSD | TODO |
| T-112 | Setup Alembic | Configure migrations | TODO |
| T-113 | Create Database | Initialize SQLite database | TODO |
| T-114 | Seed Data | Insert default company/admin | TODO |

**Detailed Sub-tasks for T-111:**
```
□ 1.2.1 Create models/__init__.py
     - Import all models
     - Create Base class
     
□ 1.2.2 Create Company model
     - id, code, name, address
     - phone, email, npwp
     - fiscal_year_start, currency_code
     
□ 1.2.3 Create User model
     - id, company_id, username
     - password_hash, full_name
     - role, is_active
     
□ 1.2.4 Create GLAccount model
     - id, company_id, code, name
     - parent_id (self-ref FK)
     - level, account_type, normal_balance
     
□ 1.2.5 Create JournalHeader model
     - id, company_id, period_id
     - journal_no, date, description
     - status, created_by
     
□ 1.2.6 Create JournalLine model
     - id, header_id, account_id
     - debit, credit, description
     
□ 1.2.7 Create remaining models
     - FSAccount, FSElement
     - SLAccount, Period
     - AuditLog, Settings
```

### 2.3 Task 1.3: Base Architecture
| ID | Task | Sub-tasks | Status |
|----|------|-----------|--------|
| T-120 | Implement BaseService | Create base service with CRUD | TODO |
| T-121 | Implement UnitOfWork | Transaction management | TODO |
| T-122 | Setup Logging | Configure loguru | TODO |
| T-123 | Setup Exception Handling | Create exception hierarchy | TODO |
| T-124 | Create Config Module | Settings management | TODO |

### 2.4 Task 1.4: UI Framework Setup
| ID | Task | Sub-tasks | Status |
|----|------|-----------|--------|
| T-130 | Create Main Window | Basic PyQt6 window | TODO |
| T-131 | Create Login Dialog | Login form | TODO |
| T-132 | Setup Menu System | Menu bar structure | TODO |
| T-133 | Setup Navigation | Sidebar navigation | TODO |
| T-134 | Create Status Bar | Status information | TODO |

**Detailed Sub-tasks for T-130:**
```
□ 1.4.1 Create app.py
     - QApplication subclass
     - Single instance check
     - Style configuration
     
□ 1.4.2 Create main_window.py
     - QMainWindow setup
     - Menu bar
     - Toolbar
     - Status bar
     
□ 1.4.3 Create theme/stylesheet
     - Color scheme
     - Typography
     - Spacing
```

---

## 3. Phase 2: Core Modules (Week 3-5)

### 3.1 Task 2.1: Authentication Module
| ID | Task | Sub-tasks | Status |
|----|------|-----------|--------|
| T-201 | Implement AuthService | Login, logout, session | TODO |
| T-202 | Create Login View | Login dialog UI | TODO |
| T-203 | Implement Password Hashing | bcrypt integration | TODO |
| T-204 | Add User Registration | Create user flow | TODO |
| T-205 | Add Session Management | Token/session handling | TODO |

**Detailed Sub-tasks for T-201:**
```
□ 2.1.1 Create AuthService class
     - login(username, password) -> LoginResult
     - logout(user_id) -> bool
     - validate_session(user_id, token) -> bool
     
□ 2.1.2 Implement password verification
     - bcrypt.check_password_hash()
     - SHA-256 with salt
     
□ 2.1.3 Add audit logging
     - Log login attempts
     - Log logout
```

### 3.2 Task 2.2: Company Setup Module
| ID | Task | Sub-tasks | Status |
|----|------|-----------|--------|
| T-210 | Implement CompanyService | CRUD operations | TODO |
| T-211 | Create Company View | Company settings UI | TODO |
| T-212 | Add Company Selector | Multi-company switcher | TODO |
| T-213 | Implement Period Management | Open/close period | TODO |

### 3.3 Task 2.3: GL Accounts Module
| ID | Task | Sub-tasks | Status |
|----|------|-----------|--------|
| T-220 | Implement GLAccountService | CRUD + hierarchy | TODO |
| T-221 | Create GL Accounts View | Account list/tree UI | TODO |
| T-222 | Add Account Form | Create/edit account | TODO |
| T-223 | Implement Account Tree | Hierarchical display | TODO |
| T-224 | Add Account Balance Calc | Balance computation | TODO |

**Detailed Sub-tasks for T-221:**
```
□ 2.3.1 Create GLAccountsView class
     - QWidget subclass
     - TreeView for hierarchy
     - Filter toolbar
     
□ 2.3.2 Create AccountForm dialog
     - Code input (validated)
     - Name input
     - Parent selector (ComboBox)
     - Type selector (Header/Detail)
     - FS mapping selector
     
□ 2.3.3 Add context menu
     - Add child account
     - Edit
     - Delete (with validation)
     
□ 2.3.4 Implement tree model
     - QAbstractItemModel
     - Lazy loading support
```

### 3.4 Task 2.4: Journal Entry Module
| ID | Task | Sub-tasks | Status |
|----|------|-----------|--------|
| T-230 | Implement JournalService | CRUD + validation | TODO |
| T-231 | Create Journal Entry View | Entry form UI | TODO |
| T-232 | Add Journal List View | List/search journals | TODO |
| T-233 | Implement Double-Entry Validation | Debit = Credit check | TODO |
| T-234 | Add Journal Numbering | Auto-numbering | TODO |
| T-235 | Implement Journal Posting | Status change | TODO |
| T-236 | Add Void Journal | Reverse transaction | TODO |

**Detailed Sub-tasks for T-231:**
```
□ 2.4.1 Create JournalEntryView class
     - Header section
       - Journal No (auto)
       - Date picker
       - Reference
       - Description
     - Line items table
       - Account selector (ComboBox with search)
       - Debit input
       - Credit input
       - Description
     - Footer section
       - Total debit
       - Total credit
       - Balance status
     - Action buttons
       - Add line
       - Remove line
       - Save
       - Cancel
       
□ 2.4.2 Implement line item model
     - QAbstractTableModel
     - Add/remove row support
     
□ 2.4.3 Add real-time validation
     - On-the-fly balance check
     - Error highlighting
```

---

## 4. Phase 3: Reporting (Week 6-7)

### 4.1 Task 3.1: Report Engine
| ID | Task | Sub-tasks | Status |
|----|------|-----------|--------|
| T-301 | Implement ReportService | Report generation | TODO |
| T-302 | Create Trial Balance | Trial balance report | TODO |
| T-303 | Create General Ledger | Book of accounts | TODO |
| T-304 | Create Journal Report | Journal listing | TODO |
| T-305 | Create Balance Sheet | BS report | TODO |
| T-306 | Create Profit & Loss | P&L report | TODO |

### 4.2 Task 3.2: Export Module
| ID | Task | Sub-tasks | Status |
|----|------|-----------|--------|
| T-310 | Implement ExportService | Excel export | TODO |
| T-311 | Export to Excel | openpyxl integration | TODO |
| T-312 | Export to CSV | CSV format | TODO |
| T-313 | Export to PDF | ReportLab integration | TODO |
| T-314 | Add Print Preview | Print functionality | TODO |

**Detailed Sub-tasks for T-311:**
```
□ 3.2.1 Create Excel export templates
     - Trial Balance template
     - General Ledger template
     - Journal template
     
□ 3.2.2 Implement export_formatter.py
     - format_currency(value)
     - format_date(date)
     - apply_styles(ws)
     
□ 3.2.3 Add export dialog
     - Format selector
     - Save location picker
     - Progress indicator
```

---

## 5. Phase 4: Polish & Distribution (Week 8)

### 5.1 Task 4.1: Utilities & Polish
| ID | Task | Sub-tasks | Status |
|----|------|-----------|--------|
| T-401 | Backup/Restore | Database backup | TODO |
| T-402 | Settings Module | App configuration | TODO |
| T-403 | Error Handling | User-friendly errors | TODO |
| T-404 | Performance Optimization | Query optimization | TODO |
| T-405 | UI/UX Polish | Visual improvements | TODO |

### 5.2 Task 4.2: Installer & Distribution
| ID | Task | Sub-tasks | Status |
|----|------|-----------|--------|
| T-410 | Create Installer Script | PyInstaller configuration | TODO |
| T-411 | Create Auto-Updater | GitHub-based updates | TODO |
| T-412 | Setup GitHub Release | Release workflow | TODO |
| T-413 | Create README | Documentation | TODO |
| T-414 | Test Installation | QA testing | TODO |

**Detailed Sub-tasks for T-411:**
```
□ 4.2.1 Create update_checker.py
     - Check GitHub releases
     - Compare versions
     - Download update
     - Apply update
     
□ 4.2.2 Add update notification
     - Check on startup
     - User notification dialog
     
□ 4.2.3 Implement self-update
     - Download new installer
     - Launch installer
     - Exit current app
```

### 5.3 Task 4.3: GitHub Integration
| ID | Task | Sub-tasks | Status |
|----|------|-----------|--------|
| T-420 | Setup GitHub Repo | Create repository | TODO |
| T-421 | Create GitHub Actions | CI/CD pipeline | TODO |
| T-422 | Setup Releases | Version releases | TODO |
| T-423 | Create CHANGELOG | Version history | TODO |

---

## 6. Task Breakdown Matrix

### 6.1 Effort Estimation

| Task ID | Task Name | Estimated Hours | Priority | Dependencies |
|---------|-----------|-----------------|----------|--------------|
| T-101 | Initialize Project | 2 | HIGH | - |
| T-102 | Git Setup | 1 | HIGH | T-101 |
| T-103 | Project Structure | 1 | HIGH | T-101 |
| T-104 | Dependencies | 1 | HIGH | T-101 |
| T-110 | Base Model | 2 | HIGH | T-103 |
| T-111 | ORM Models | 4 | HIGH | T-110 |
| T-112 | Alembic Setup | 2 | HIGH | T-111 |
| T-120 | BaseService | 2 | HIGH | T-111 |
| T-121 | UnitOfWork | 2 | HIGH | T-120 |
| T-130 | Main Window | 4 | HIGH | T-104 |
| T-131 | Login Dialog | 3 | HIGH | T-130 |
| T-201 | AuthService | 4 | HIGH | T-120 |
| T-202 | Login View | 3 | HIGH | T-201 |
| T-210 | CompanyService | 3 | MEDIUM | T-120 |
| T-220 | GLAccountService | 4 | HIGH | T-120 |
| T-221 | GL Accounts View | 6 | HIGH | T-220 |
| T-230 | JournalService | 5 | HIGH | T-220 |
| T-231 | Journal Entry View | 8 | HIGH | T-230 |
| T-232 | Journal List View | 4 | HIGH | T-230 |
| T-301 | ReportService | 4 | HIGH | T-230 |
| T-302 | Trial Balance | 4 | HIGH | T-301 |
| T-310 | ExportService | 4 | HIGH | T-301 |
| T-311 | Excel Export | 4 | HIGH | T-310 |
| T-401 | Backup/Restore | 3 | MEDIUM | T-111 |
| T-410 | Installer | 4 | HIGH | All |
| T-411 | Auto-Updater | 4 | MEDIUM | T-410 |
| T-420 | GitHub Setup | 2 | HIGH | T-410 |

**Total Estimated Hours:** ~80 hours (with AI assistance)

### 6.2 Task Priority Matrix

```
                    HIGH IMPACT
                         │
      ┌─────────────────┼─────────────────┐
      │                 │                   │
      │    T-221        │    T-231         │  DO FIRST
      │    GL Accounts  │    Journal Entry │
      │                 │                   │
LOW ──┼─────────────────┼─────────────────┼──── HIGH
URGENCY│                 │                   │  URGENCY
      │                 │                   │
      │    T-103        │    T-410         │  SCHEDULE
      │    Structure    │    Installer     │
      │                 │                   │
      └─────────────────┼─────────────────┘
                         │
                    LOW IMPACT
```

---

## 7. GitHub Workflow

### 7.1 Branch Strategy

```
main (production)
  │
  ├── develop (development)
  │     │
  │     ├── feature/auth-module
  │     ├── feature/gl-accounts
  │     ├── feature/journal-entry
  │     ├── feature/reports
  │     └── feature/installer
  │
  └── release/v1.0.0 (release candidate)
```

### 7.2 Commit Convention

```
<type>(<scope>): <subject>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Refactoring
- test: Testing
- chore: Maintenance

Examples:
feat(auth): add login functionality
fix(journal): validate debit/credit balance
docs(readme): update installation guide
```

### 7.3 Pull Request Template

```markdown
## Description
[Summary of changes]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests passed
- [ ] Integration tests passed
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style
- [ ] Self-reviewed code
- [ ] Comments added for complex logic
- [ ] Documentation updated

## Screenshots (if applicable)
[Attach screenshots]
```

### 7.4 GitHub Actions Workflow

```yaml
# .github/workflows/main.yml
name: WISA-CLONE CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
      - run: ruff check src/

  build:
    needs: test
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pip install pyinstaller
      - run: python scripts/build_exe.py
      - uses: actions/upload-artifact@v3
        with:
          name: installer
          path: dist/WISA-CLONE.exe

  release:
    needs: build
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: softprops/action-gh-release@v1
        with:
          files: dist/WISA-CLONE.exe
          generate_release_notes: true
```

### 7.5 Auto-Update Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      AUTO-UPDATE FLOW                            │
└─────────────────────────────────────────────────────────────────┘

User launches app
        │
        ▼
┌──────────────────┐
│ Check for Updates │
│ (GitHub API)      │
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
│ User clicks     │
│ "Update Now"    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Download new    │
│ version from    │
│ GitHub Release  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Launch installer│
│ and exit app   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Run installer   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Launch new      │
│ version         │
└─────────────────┘
```

---

## 8. Implementation Checklist

### Pre-Development Checklist
```
□ Environment Setup
  □ Python 3.10+ installed
  □ Git installed
  □ IDE configured (VS Code recommended)
  □ Virtual environment created
  
□ Documentation Review
  □ PRD reviewed and approved
  □ FSD reviewed and approved
  □ TSD reviewed and approved
  □ All questions clarified
  
□ Repository Setup
  □ GitHub repository created
  □ SSH key configured
  □ Initial commit done
```

### Development Checklist (Per Sprint)
```
□ Code Implementation
  □ Feature code written
  □ Code follows style guide
  □ Comments added where needed
  
□ Testing
  □ Unit tests written
  □ Tests pass locally
  □ No regression
  
□ Documentation
  □ Docstrings added
  □ README updated if needed
  
□ Code Review
  □ Self-review completed
  □ PR created
  □ Review feedback addressed
```

### Release Checklist
```
□ Pre-Release
  □ All tests pass
  □ No known bugs
  □ Documentation complete
  □ CHANGELOG updated
  
□ Release
  □ Version tag created
  □ Release notes written
  □ Installer tested
  □ GitHub release published
  
□ Post-Release
  □ User feedback monitored
  □ Issues tracked
  □ Hotfix plan ready
```

---

**Document History:**
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-31 | AI Assistant | Initial draft |
