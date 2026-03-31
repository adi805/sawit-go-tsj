# 🌴 SAWIT GO - TSJ - Project Rules

> **Project Rules untuk Sawit Go - TSJ Accounting System**
> **Owner:** Syafriadi
> **Repository:** https://github.com/adi805/sawit-go-tsj

---

## 📋 Daftar Isi

1. [Workflow Rules](#1-workflow-rules)
2. [Git & Version Control Rules](#2-git--version-control-rules)
3. [Code Quality Rules](#3-code-quality-rules)
4. [Documentation Rules](#4-documentation-rules)
5. [Testing Rules](#5-testing-rules)
6. [Build & Release Rules](#6-build--release-rules)
7. [Communication Rules](#7-communication-rules)

---

## 1. Workflow Rules

### 1.1 Main Workflow (WAJIB DI IKUTI)

```
┌─────────────────────────────────────────────────────────────────┐
│                    MAIN DEVELOPMENT WORKFLOW                     │
└─────────────────────────────────────────────────────────────────┘

START
  │
  ▼
┌─────────────────────────────────────┐
│ 1. Pull dari GitHub                 │
│    git pull origin main              │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ 2. Buat Feature Branch              │
│    git checkout -b feature/xxx      │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ 3. Coding & Testing Lokal          │
│    - Write code                     │
│    - Test manually                  │
│    - Run pytest                     │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ 4. Build Lokal (WAJIB)              │
│    python scripts/build_exe.py       │
│    ✓ Verify .exe berhasil dibuat     │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ 5. Commit & Push ke GitHub          │
│    git add .                        │
│    git commit -m "feat: description"│
│    git push origin feature/xxx       │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ 6. Buat Pull Request                │
│    - ke branch main                 │
│    - Include description            │
│    - Include test results          │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ 7. Code Review (Jika diperlukan)    │
│    - Owner review                   │
│    - Approve / Request changes      │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ 8. Merge ke main (setelah approved) │
│    git checkout main                │
│    git merge feature/xxx           │
│    git push origin main             │
└───────────────┬─────────────────────┘
                │
                ▼
              END
```

### 1.2 Branch Naming Convention

```
Format: <type>/<description>

Types:
- feature/      → Fitur baru
- fix/           → Bug fix
- refactor/      → Refactoring
- docs/          → Dokumentasi
- hotfix/        → Fix urgent/production
- release/       → Release preparation

Examples:
✓ feature/authentication
✓ feature/gl-accounts
✓ fix/journal-validation
✓ refactor/export-service
✓ docs/readme-update
✓ hotfix/crash-on-startup
✗ fix-1
✗ new-feature
```

### 1.3 Commit Message Convention

```
Format: <type>(<scope>): <description>

Types:
- feat     → New feature
- fix      → Bug fix
- docs     → Documentation
- style    → Formatting (no code change)
- refactor → Code refactoring
- test     → Adding tests
- chore    → Maintenance task

Scope (optional):
- auth      → Authentication
- gl        → GL Accounts
- journal   → Journal Entry
- report    → Reporting
- export    → Export feature
- ui        → UI changes
- db        → Database changes
- build     → Build process

Examples:
✓ feat(auth): add login functionality
✓ fix(journal): validate debit/credit balance
✓ feat(gl): add account tree view
✓ docs: update README installation
✓ refactor(export): improve Excel export speed
✓ fix(ui): resolve button alignment issue
```

---

## 2. Git & Version Control Rules

### 2.1 Push Rules (WAJIB)

> ⚠️ **PERATURAN KRUSIAL: SETIAP BUILD LOKAL WAJIB DI-PUSH KE GITHUB**

```
┌─────────────────────────────────────────────────────────────────┐
│                    PUSH RULES (WAJIB)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ JIKA...                                                      │
│  ─────────────────────────────────────────────────────────────  │
│  • Build .exe lokal berhasil                                    │
│  • Ada perubahan code signifikan                                │
│  • Selesai testing fitur baru                                  │
│  • Sebelum tutup sesi coding                                    │
│  • Setiap akhir hari kerja                                      │
│                                                                  │
│  ❌ JANGAN...                                                    │
│  ─────────────────────────────────────────────────────────────  │
│  • Push code yang belum di-test                                │
│  • Push dengan commit message tidak jelas                        │
│  • Push langsung ke branch main (selalu pakai PR)               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Git Commands Reference

```bash
# === SETUP (One Time) ===
git clone https://github.com/adi805/sawit-go-tsj.git
cd sawit-go-tsj
git config user.email "syafriadi@tsj.co.id"
git config user.name "Syafriadi"

# === DAILY WORKFLOW ===
# 1. Start hari: Pull terbaru
git checkout main
git pull origin main

# 2. Buat feature branch
git checkout -b feature/nama-fitur

# 3. Coding...

# 4. Build lokal (WAJIB!)
python scripts/build_exe.py
# Verifikasi: dist/SawitGo-TSJ.exe ada

# 5. Commit changes
git add .
git commit -m "feat(scope): description"

# 6. Push ke GitHub (WAJIB!)
git push origin feature/nama-fitur

# 7. Buat Pull Request via GitHub UI
# atau via command:
gh pr create --title "feat: nama fitur" --body "Description"
```

### 2.3 Version Tagging

```bash
# Format versi: MAJOR.MINOR.PATCH
# Contoh: v1.0.0

# Buat tag
git tag -a v1.0.0 -m "Release Sawit Go - TSJ v1.0.0"

# Push tag
git push origin v1.0.0

# List tags
git tag -l

# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin --delete v1.0.0
```

---

## 3. Code Quality Rules

### 3.1 Python Style Guide

```python
# ✅ WAJIB: Gunakan type hints
def calculate_total(debit: Decimal, credit: Decimal) -> Decimal:
    return debit + credit

# ✅ WAJIB: Docstring untuk fungsi publik
def create_journal(date: date, description: str) -> Optional[int]:
    """
    Create a new journal entry.
    
    Args:
        date: Journal date
        description: Journal description
        
    Returns:
        Journal ID if successful, None otherwise
        
    Raises:
        ValidationError: If validation fails
    """
    pass

# ✅ WAJIB: Error handling
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Error: {e}")
    raise CustomError("User-friendly message") from e

# ❌ JANGAN: Magic numbers
# Bad
if balance > 1000000:
    pass

# Good
MAX_BALANCE = Decimal('1000000')
if balance > MAX_BALANCE:
    pass
```

### 3.2 File Organization

```python
# src/
# ├── __init__.py          # Package init
# ├── main.py              # Entry point ONLY
# ├── app.py               # QApplication setup
# │
# ├── models/              # SQLAlchemy models (1 file per model)
# │   ├── __init__.py
# │   ├── base.py
# │   ├── company.py
# │   └── user.py
# │
# ├── services/            # Business logic (1 file per service)
# │   ├── __init__.py
# │   ├── auth_service.py
# │   └── journal_service.py
# │
# └── ui/                 # PyQt6 UI
#     ├── __init__.py
#     └── views/
```

---

## 4. Documentation Rules

### 4.1 Required Documentation

```
┌─────────────────────────────────────────────────────────────────┐
│                   DOCUMENTATION REQUIREMENTS                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  FILE              │  KAPAN UPDATE      │  OLEH                 │
│  ───────────────────────────────────────────────────────────    │
│  CHANGELOG.md     │  Setiap release    │  Developer            │
│  README.md         │  Major changes    │  Developer            │
│  Docstrings        │  Setiap fungsi   │  Developer            │
│  SPEC.md          │  Major changes    │  Owner/Developer      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 CHANGELOG Format

```markdown
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Fixed
- Bug fixes

### Security
- Security improvements
```

---

## 5. Testing Rules

### 5.1 Test Requirements

```
┌─────────────────────────────────────────────────────────────────┐
│                      TEST REQUIREMENTS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Coverage Target:                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  • Services:  > 80%                                             │
│  • Repos:     > 70%                                              │
│  • Utils:     > 80%                                              │
│  • Overall:   > 70%                                              │
│                                                                  │
│  Before Push, Pastikan:                                          │
│  ─────────────────────────────────────────────────────────────  │
│  ✓ pytest tests/ -v (semua test pass)                            │
│  ✓ ruff check src/ (tidak ada error)                            │
│  ✓ Manual test fitur terkait                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Test Naming

```python
# Test files: test_<module_name>.py
# test_auth_service.py
# test_journal_service.py

# Test functions: test_<what_is_tested>
def test_login_success():
    """Test successful login"""
    pass

def test_login_invalid_password():
    """Test login with invalid password"""
    pass

def test_journal_validation_debit_equals_credit():
    """Test journal entry validation for balanced debit/credit"""
    pass
```

---

## 6. Build & Release Rules

### 6.1 Build Process (WAJIB)

```
┌─────────────────────────────────────────────────────────────────┐
│                     BUILD PROCESS (WAJIB)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Clean previous build                                        │
│     - Hapus folder dist/ dan build/                             │
│                                                                  │
│  2. Run build script                                            │
│     python scripts/build_exe.py                                  │
│                                                                  │
│  3. VERIFIKASI                                                  │
│     - Cek dist/SawitGo-TSJ.exe ada                             │
│     - Test run .exe (double-click)                             │
│     - Verify tidak ada error saat startup                      │
│                                                                  │
│  4. Push ke GitHub (WAJIB!)                                     │
│     git add .                                                  │
│     git commit -m "build: generate vX.X.X"                     │
│     git push origin feature/xxx                                 │
│                                                                  │
│  5. Buat Release (untuk major releases)                        │
│     - Tag version                                               │
│     - Attach .exe ke release                                   │
│     - Write release notes                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Release Versioning

```
Format: MAJOR.MINOR.PATCH

Rules:
• PATCH (x.x.1) → Bug fixes, tidak ada fitur baru
• MINOR (x.1.0) → New features, backward compatible
• MAJOR (1.0.0) → Breaking changes

Contoh:
v1.0.0 → First release
v1.0.1 → Bug fix
v1.1.0 → Add Excel export
v2.0.0 → Breaking: change database schema
```

---

## 7. Communication Rules

### 7.1 GitHub Issues

```markdown
## Issue Template

**Title:** [BUG/FEATURE] Deskripsi singkat

**Description:**
- Apa yang terjadi?
- Apa yang diharapkan?
- Steps to reproduce (untuk bug)

**Environment:**
- OS: Windows 10
- Version: v1.0.0
- Python: 3.11

**Attachments:**
- Screenshot
- Traceback/error log
```

### 7.2 Pull Request Template

```markdown
## Description
Ringkasan perubahan

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests passed
- [ ] Integration tests passed
- [ ] Manual testing completed
- [ ] Build .exe verified

## Checklist
- [ ] Code follows style guide
- [ ] Self-reviewed
- [ ] Comments added
- [ ] Documentation updated
- [ ] CHANGELOG updated

## Screenshots (if UI changes)
```

---

## 📌 Quick Reference Commands

```bash
# === WORKFLOW LENGKAP ===
git checkout main && git pull origin main
git checkout -b feature/nama-fitur
# coding...
python scripts/build_exe.py
git add . && git commit -m "feat: description"
git push origin feature/nama-fitur

# === VERIFIKASI ===
pytest tests/ -v
ruff check src/

# === RELEASE ===
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

---

## ⚠️ Violation Consequences

| Violation | Consequence |
|-----------|-------------|
| Tidak push setelah build | ⚠️ Warning |
| Push tanpa test | ⚠️ PR rejected |
| Push breaking code ke main | 🔴 Rollback required |
| Tidak update CHANGELOG | ⚠️ Warning |
| Commit message tidak sesuai | ⚠️ PR rejected |

---

**Document Version:** 1.0  
**Last Updated:** 2026-03-31  
**Owner:** Syafriadi  
**Repository:** https://github.com/adi805/sawit-go-tsj
