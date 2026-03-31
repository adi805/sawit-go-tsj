# SAWIT GO - TSJ - Implementation Plan

**Versi:** 1.0  
**Tanggal:** 2026-03-31  
**Status:** Draft  
**Author:** AI Assistant  
**Owner:** Syafriadi  

---

## Ringkasan Eksekutif

### Visi Project

> **"Sistem Akuntansi Modern untuk Perkebunan Sawit - Ringan, Fleksibel, dan Bisa Jalan di Mana Saja"**

**Sawit Go - TSJ** adalah aplikasi akuntansi desktop modern berbasis Python + PyQt6 dengan database SQLite yang ringan namun powerful. Dibangun untuk memenuhi kebutuhan akuntansi perusahaan perkebunan kelapa sawit (PT Tulas Sakti Jaya) dengan fitur-fitur essential seperti Chart of Accounts, Journal Entry, Trial Balance, dan export ke Excel.

---

## 1. Teknologi Stack

### 1.1 Stack yang Dipilih (Gratis & Ringan)

| Komponen | Teknologi | Alasan |
|----------|-----------|--------|
| **Bahasa** | Python 3.10+ | AI bisa handle 100%, komunitas besar |
| **GUI** | PyQt6 | Modern, professional, ringan |
| **Database** | SQLite3 | Built-in Python, zero-config, portable |
| **ORM** | SQLAlchemy | Type-safe, migration support |
| **Excel** | openpyxl + pandas | Industry standard |
| **Installer** | PyInstaller | Compile to .exe |
| **Update** | GitHub Releases | Auto-update via GitHub |

### 1.2 System Requirements

| Komponen | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 7 64-bit | Windows 10/11 64-bit |
| **CPU** | Intel Celeron / AMD A4 | Intel i3 / Ryzen 3 |
| **RAM** | 2 GB | 4 GB |
| **Storage** | 100 MB free | 500 MB free |
| **Display** | 1024x768 | 1920x1080 |

### 1.3 Estimasi Ukuran Installer

```
PyQt6:              ~40 MB
SQLAlchemy:         ~5 MB
openpyxl:           ~5 MB
Application code:   ~10 MB
Database driver:    Built-in
────────────────────────────
Total estimate:     ~60-80 MB (compressed)
```

---

## 2. Timeline Implementation

### 2.1 Timeline Overview (8 Weeks)

```
Week 1-2: FOUNDATION
├── Project Setup
├── Database Schema
├── Base Architecture
└── UI Framework

Week 3-5: CORE MODULES
├── Authentication
├── Company Setup
├── GL Accounts
├── Journal Entry
└── Basic CRUD

Week 6-7: REPORTING & EXPORT
├── Report Engine
├── Trial Balance
├── General Ledger
├── Excel Export
└── PDF Export

Week 8: POLISH & RELEASE
├── Backup/Restore
├── Settings
├── Installer (PyInstaller)
├── GitHub Release
└── Auto-Update System
```

### 2.2 Detailed Schedule

```
┌────────────────────────────────────────────────────────────────────────┐
│                           SAWIT GO - TSJ                              │
│                      Implementation Timeline                            │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│ WEEK 1 (Foundation)                                                    │
│ ├── Day 1-2: Setup environment & project structure                    │
│ ├── Day 3-4: Create database models (SQLAlchemy)                     │
│ ├── Day 5:   Setup Alembic migrations                                │
│ └── Day 6-7: Create base service classes                             │
│                                                                        │
│ WEEK 2 (Foundation)                                                   │
│ ├── Day 8-9: Create Main Window (PyQt6)                             │
│ ├── Day 10-11: Create Login Dialog                                   │
│ ├── Day 12-13: Setup navigation & menus                             │
│ └── Day 14: Integration & testing                                     │
│                                                                        │
│ WEEK 3 (Core Modules)                                                │
│ ├── Day 15-16: Implement AuthService                                 │
│ ├── Day 17-18: Create Login View                                     │
│ ├── Day 19-20: Company module                                       │
│ └── Day 21: Review & testing                                         │
│                                                                        │
│ WEEK 4 (Core Modules)                                                │
│ ├── Day 22-24: GL Accounts Service + View                          │
│ ├── Day 25-26: Account Tree implementation                           │
│ └── Day 27: Review & testing                                         │
│                                                                        │
│ WEEK 5 (Core Modules)                                                │
│ ├── Day 28-30: Journal Service + Validation                         │
│ ├── Day 31-32: Journal Entry View                                   │
│ ├── Day 33-34: Journal List View                                    │
│ └── Day 35: Review & testing                                         │
│                                                                        │
│ WEEK 6 (Reporting)                                                    │
│ ├── Day 36-37: ReportService base                                    │
│ ├── Day 38-39: Trial Balance Report                                 │
│ ├── Day 40-41: General Ledger Report                                 │
│ └── Day 42: Review & testing                                         │
│                                                                        │
│ WEEK 7 (Export)                                                      │
│ ├── Day 43-44: ExportService + Excel Export                         │
│ ├── Day 45-46: Balance Sheet Report                                 │
│ ├── Day 47-48: Profit & Loss Report                                │
│ └── Day 49: Review & testing                                         │
│                                                                        │
│ WEEK 8 (Polish & Release)                                            │
│ ├── Day 50-51: Backup/Restore + Settings                            │
│ ├── Day 52-53: PyInstaller configuration                            │
│ ├── Day 54-55: GitHub Actions setup                                 │
│ ├── Day 56: Auto-update system                                       │
│ └── Day 57-58: Final testing & release                               │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘

Total: ~58 working days (with AI assistance)
```

---

## 3. Effort Breakdown

### 3.1 By Phase

| Phase | Hours | Percentage |
|-------|-------|------------|
| Foundation | 16 hours | 20% |
| Core Modules | 32 hours | 40% |
| Reporting | 16 hours | 20% |
| Polish & Release | 16 hours | 20% |
| **Total** | **80 hours** | **100%** |

### 3.2 By Task Type

```
Foundation (16h)
├── Setup: 4h (5%)
├── Database: 8h (10%)
└── Architecture: 4h (5%)

Core Modules (32h)
├── Auth: 6h (7.5%)
├── Company: 4h (5%)
├── GL Accounts: 10h (12.5%)
└── Journal: 12h (15%)

Reporting (16h)
├── Report Engine: 4h (5%)
├── Trial Balance: 4h (5%)
├── General Ledger: 4h (5%)
└── Excel Export: 4h (5%)

Polish & Release (16h)
├── Utilities: 4h (5%)
├── Installer: 4h (5%)
├── GitHub: 4h (5%)
└── Testing: 4h (5%)
```

---

## 4. GitHub Integration

### 4.1 Repository Structure

```
sawit-go-tsj/
├── .github/
│   └── workflows/
│       ├── ci.yml          # CI pipeline
│       └── release.yml      # Release pipeline
├── src/
│   ├── app.py
│   ├── main.py
│   ├── models/
│   ├── services/
│   ├── repositories/
│   ├── ui/
│   └── utils/
├── tests/
├── docs/
├── resources/
├── scripts/
│   └── build_exe.py
├── requirements.txt
├── README.md
├── CHANGELOG.md
└── LICENSE
```

### 4.2 Branch Strategy

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

### 4.3 Auto-Update Mechanism

```python
# update_checker.py
class UpdateChecker:
    GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/releases"
    
    def check_for_updates(self):
        response = requests.get(
            self.GITHUB_API.format(owner="owner", repo="sawit-go-tsj")
        )
        releases = response.json()
        latest = releases[0]
        
        if version.parse(latest['tag_name']) > version.parse(CURRENT_VERSION):
            return latest
        return None
```

### 4.4 GitHub Actions Workflow

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pip install pyinstaller
      - run: python scripts/build_exe.py
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/SawitGo-TSJ.exe
```

---

## 5. Risk Management

### 5.1 Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| PyInstaller false positives | Medium | Medium | Document clearly, submit to MS |
| Large file size | Low | Low | Use UPX compression |
| SQLite performance | Low | Low | Indexing, pagination |
| Encoding issues (Indonesian) | Medium | High | UTF-8 everywhere |
| Dependency conflicts | Low | Medium | Virtual environment |

### 5.2 Contingency Plans

| Scenario | Contingency |
|----------|-------------|
| PyInstaller fails | Use cx_Freeze as backup |
| SQLite too slow | Add connection pooling |
| Encoding problems | Force UTF-8 in all I/O |
| Update fails | Manual download link |

---

## 6. Quality Assurance

### 6.1 Testing Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                        TESTING PYRAMID                           │
└─────────────────────────────────────────────────────────────────┘

                        ┌───────────┐
                       │   E2E     │  ← Manual testing
                       │   Tests   │    (Full flow)
                       └─────┬─────┘
                             │
                    ┌────────┴────────┐
                   │  Integration   │  ← Service tests
                   │    Tests       │    (DB + Services)
                   └─────┬──────────┘
                         │
                ┌────────┴────────┐
               │     Unit        │  ← pytest
               │     Tests        │    (Functions)
               └─────────────────┘
```

### 6.2 Test Coverage Target

| Module | Target Coverage |
|--------|-----------------|
| Services | > 80% |
| Repositories | > 70% |
| UI | > 50% |
| Utils | > 80% |
| **Overall** | **> 70%** |

### 6.3 Manual Testing Checklist

```
□ Login Flow
  □ Valid credentials → Success
  □ Invalid credentials → Error message
  □ Empty fields → Validation error
  
□ GL Accounts
  □ Create header account
  □ Create detail account (child)
  □ Edit account
  □ Delete account (with children)
  □ Tree view expands/collapses
  
□ Journal Entry
  □ Create journal with 2+ lines
  □ Debit ≠ Credit → Validation error
  □ Empty account → Validation error
  □ Save journal
  □ View journal list
  □ Void journal
  
□ Reports
  □ Trial Balance shows correct totals
  □ Date filter works
  □ Export to Excel
  □ Excel file opens correctly
```

---

## 7. Deployment Strategy

### 7.1 Release Versioning

```
MAJOR.MINOR.PATCH
     │    │    │
     │    │    └── Bug fixes
     │    └─────── New features (backward compatible)
     └─────────── Breaking changes
```

### 7.2 Release Types

| Type | Frequency | Description |
|------|-----------|-------------|
| **Hotfix** | As needed | Critical bug fixes |
| **Patch** | Bi-weekly | Bug fixes |
| **Minor** | Monthly | New features |
| **Major** | Quarterly | Breaking changes |

### 7.3 Installation Process

```
┌─────────────────────────────────────────────────────────────────┐
│                   INSTALLATION FLOW                              │
└─────────────────────────────────────────────────────────────────┘

User downloads SawitGo-TSJ_Setup_v1.0.0.exe
                    │
                    ▼
┌────────────────────────────────────────┐
│        Welcome Screen                   │
│   "Selamat datang di Sawit Go - TSJ"   │
└────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────┐
│        License Agreement               │
│   [ ] I accept the terms              │
└────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────┐
│        Installation Location            │
│   [C:\Program Files\SawitGo-TSJ]      │
└────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────┐
│        Desktop Shortcut                │
│   [x] Create desktop shortcut         │
└────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────┐
│           Installing...                │
│   ████████████░░░░░░░ 60%             │
└────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────┐
│           Installation Complete!        │
│   [ ] Launch Sawit Go - TSJ          │
└────────────────────────────────────────┘
```

---

## 8. Support & Maintenance

### 8.1 Support Channels

| Channel | Purpose | Response Time |
|---------|---------|--------------|
| GitHub Issues | Bug reports, feature requests | 24-48 hours |
| GitHub Discussions | Q&A | 48-72 hours |

### 8.2 Update Notification

```
┌─────────────────────────────────────────────────────────┐
│          🆕 Update Available                             │
│                                                          │
│  Version 1.1.0 is now available!                       │
│                                                          │
│  Changes:                                                │
│  • Fixed trial balance calculation bug                  │
│  • Added account code validation                        │
│  • Improved Excel export speed                          │
│                                                          │
│  [  Download & Install  ]     [  Remind Me Later  ]    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 9. Document Deliverables

| Document | File | Status |
|----------|------|--------|
| Product Requirements | [PRD.md](PRD.md) | ✅ Complete |
| Functional Specification | [FSD.md](FSD.md) | ✅ Complete |
| Technical Specification | [TSD.md](TSD.md) | ✅ Complete |
| Task List | [TASK_LIST.md](TASK_LIST.md) | ✅ Complete |
| Implementation Plan | [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) | ✅ Complete |
| Database Schema | [db_schema.dbml](db_schema.dbml) | ✅ Complete |
| README | README.md | 🔜 Next |
| CHANGELOG | CHANGELOG.md | 🔜 Per release |

---

## 10. Next Steps

### 10.1 Immediate (This Week)

```
□ 1. Review all documents
□ 2. Approve project scope
□ 3. Create GitHub repository
□ 4. Initialize project
□ 5. Start Phase 1 implementation
```

### 10.2 Week 1 Deliverables

```
□ 1. Python environment setup
□ 2. Git repository initialized
□ 3. Basic project structure created
□ 4. Database models implemented
□ 5. Main window skeleton created
```

### 10.3 Questions for Clarification

```
□ 1. Apakah ada template Chart of Accounts spesifik untuk perkebunan sawit?
□ 2. Format nomor jurnal apa yang preferred? (e.g., JRN-2026-001)
□ 3. Apakah perlu integration dengan sistem lain?
□ 4. Target user primarily di lapangan atau kantor?
□ 5. Bahasa UI: Indonesia atau English?
```

---

## 11. Contact & Owner

| Info | Details |
|------|---------|
| **Owner** | Syafriadi |
| **Project** | Sawit Go - TSJ |
| **Purpose** | Sistem Akuntansi untuk PT Tulas Sakti Jaya |
| **Tech Stack** | Python + PyQt6 + SQLite |
| **License** | MIT License |

---

## 12. Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Owner | Syafriadi | __________ | __________ |
| Developer | AI Assistant | 2026-03-31 | __________ |

---

**Document Status:** Ready for Review

**Next Action:** 
1. Owner review & approve
2. Create GitHub repository
3. Start Phase 1 implementation
