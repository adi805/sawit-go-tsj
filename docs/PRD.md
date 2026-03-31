# WISA-CLONE - Product Requirements Document (PRD)

**Versi:** 1.0  
**Tanggal:** 2026-03-31  
**Status:** Draft  
**Author:** AI Assistant  

---

## 1. Overview

### 1.1 Product Name
**WISA-CLONE** - Aplikasi Akuntansi General Ledger Desktop

### 1.2 Product Type
Desktop Application (.exe) - Portable, single-file executable

### 1.3 Core Functionality
Sistem akuntansi General Ledger berbasis desktop dengan database fleksibel (SQLite) yang dapat diekspor ke Excel. Clone modern dari Wisa Accounting System v2.3.

### 1.4 Target Users
- UMKM / Perusahaan menengah di Indonesia
- Akuntan yang membutuhkan sistem akuntansi sederhana namun powerful
- Pengguna yang butuh aplikasi portable tanpa instalasi complex

---

## 2. Business Context

### 2.1 Problem Statement
- Wisa Accounting System adalah aplikasi legacy (2006) dengan teknologi usang
- Hanya berjalan di Windows 32-bit dengan Microsoft Access
- Tidak ada backup cloud / sync
- Maintenance sulit karena teknologi lama

### 2.2 Opportunity
- Modernisasi aplikasi dengan teknologi yang lebih ringan & portable
- Database fleksibel yang bisa diakses via Excel
- Cross-platform potential (Windows/Linux/Mac)

---

## 3. Product Vision

### 3.1 Core Value Proposition
> *"Akuntansi modern yang ringan, fleksibel, dan bisa jalan di mana saja - seperti Wisa Accounting, tapi lebih baik."*

### 3.2 Key Benefits
| Benefit | Description |
|---------|-------------|
| **Ringan** | Ukuran < 100MB, bisa jalan di laptop specs rendah |
| **Fleksibel** | Database SQLite yang bisa di-export Excel |
| **Portable** | Single .exe file, tidak perlu instalasi |
| **Modern** | UI modern dengan PyQt6 |
| **Gratis** | 100% open source, tanpa license cost |

---

## 4. User Requirements

### 4.1 User Personas

#### Persona 1: Akuntan UMKM
- **Nama:** Budi Santoso
- **Usia:** 35 tahun
- **Profil:** Owner accounting department di PT swasta menengah
- **Pain Points:**
  - Butuh sistem yang simple tapi lengkap
  - Tidak punya IT staff khusus
  - Sering kerja remote / ke client
- **Goals:**
  - Input jurnal dengan cepat
  - Lihat laporan keuangan kapan saja
  - Backup data mudah

#### Persona 2: Freelance Accountant
- **Nama:** Siti Rahayu
- **Usia:** 28 tahun
- **Profil:** Freelance akuntan untuk 5+ klien
- **Pain Points:**
  - Klien punya data berbeda format
  - Butuh fleksibilitas database
  - Kerja di mana saja
- **Goals:**
  - Multi-company support
  - Export laporan ke Excel
  - Portable app

### 4.2 User Stories

| ID | Story | Priority | Acceptance Criteria |
|----|-------|----------|---------------------|
| US-001 | Sebagai Akuntan, saya ingin login ke aplikasi dengan username/password | HIGH | User bisa login dengan kredensial yang tersimpan di database |
| US-002 | Sebagai Akuntan, saya ingin membuat Chart of Accounts | HIGH | User bisa CRUD akun GL dengan hierarchy |
| US-003 | Sebagai Akuntan, saya ingin input jurnal umum | HIGH | User bisa buat jurnal dengan multiple line items |
| US-004 | Sebagai Akuntan, saya ingin melihat Trial Balance | HIGH | Report Trial Balance dengan filter periode |
| US-005 | Sebagai Akuntan, saya ingin export data ke Excel | HIGH | Semua data bisa di-export ke .xlsx |
| US-006 | Sebagai Akuntan, saya ingin multi-company support | MEDIUM | Satu database bisa handle multiple perusahaan |
| US-007 | Sebagai Akuntan, saya ingin backup/restore database | HIGH | Backup ke file .db, restore kapan saja |
| US-008 | Sebagai Akuntan, saya ingin print laporan | MEDIUM | Bisa print laporan dalam format PDF |

---

## 5. Functional Requirements

### 5.1 Core Modules

#### 5.1.1 Authentication Module
- Login dengan username & password
- Session management
- Role-based access (Admin, User, Viewer)

#### 5.1.2 Master Data Module
- **Organization** - Data perusahaan
- **Chart of Accounts (COA)** - Akun GL dengan hierarchy
- **Subsidiary Accounts** - Akun Buku Pembantu
- **Financial Statement Mapping** - Mapping ke laporan keuangan

#### 5.1.3 Transaction Module
- **Journal Entry** - Input jurnal umum
  - Header: Tanggal, No Jurnal, Keterangan
  - Detail: Multiple line items (Akun, Debit, Kredit)
  - Validation: Total Debit = Total Kredit
- **Journal Approval** - Optional approval workflow

#### 5.1.4 Reporting Module
- **Trial Balance** - Neraca Saldo
- **General Ledger** - Buku Besar
- **Journal Report** - Laporan Jurnal
- **Balance Sheet** - Neraca (opname)
- **Profit & Loss** - Laba Rugi

#### 5.1.5 Utility Module
- **Database Backup/Restore**
- **Export to Excel**
- **Import from Excel**
- **Settings & Configuration**

### 5.2 Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        WISA-CLONE                               │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │  Login   │───▶│  Master  │───▶│   Jurnal │───▶│  Report  │ │
│  │  Screen  │    │   Data   │    │  Entry   │    │  Engine  │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│       │              │               │               │        │
│       └──────────────┴───────────────┴───────────────┘        │
│                            │                                   │
│                     ┌──────────────┐                           │
│                     │    SQLite    │                           │
│                     │   Database   │                           │
│                     └──────────────┘                           │
│                            │                                   │
│              ┌─────────────┼─────────────┐                     │
│              ▼             ▼             ▼                     │
│        ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│        │  Excel   │  │   PDF    │  │  Backup  │               │
│        │  Export  │  │  Print   │  │  .db file│               │
│        └──────────┘  └──────────┘  └──────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Non-Functional Requirements

### 6.1 Performance
| Metric | Target |
|--------|--------|
| Startup Time | < 3 detik |
| Memory Usage | < 200MB RAM |
| Database Size | Unlimited (tested up to 1GB) |
| Response Time | < 1 detik untuk operasi CRUD |

### 6.2 Platform Support
| Platform | Status |
|----------|--------|
| Windows 10/11 (64-bit) | ✅ Primary |
| Windows 7/8 (64-bit) | ✅ Supported |
| Linux (optional) | 🔜 Future |
| macOS (optional) | 🔜 Future |

### 6.3 Security
| Requirement | Implementation |
|-------------|---------------|
| Password Storage | SHA-256 hash with salt |
| Session | JWT-like token (24hr expiry) |
| Database | File-based encryption (optional) |
| Audit Log | Semua transaksi di-log |

### 6.4 Portability
- Single .exe file
- No installation required
- Database dalam folder yang sama atau bisa di-move
- Settings dalam file JSON

---

## 7. Technical Stack

### 7.1 Selected Technology

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **GUI Framework** | PyQt6 | Modern, feature-rich, professional look |
| **Database** | SQLite3 | Built-in Python, zero-config, portable |
| **ORM** | SQLAlchemy | Type-safe queries, migration support |
| **Excel Export** | openpyxl + pandas | Industry standard, full feature |
| **Packaging** | PyInstaller | Industry standard for Python exe |
| **Logging** | loguru | Simple, beautiful logging |
| **Testing** | pytest | Industry standard |

### 7.2 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Windows 7 64-bit | Windows 10/11 64-bit |
| CPU | Intel Celeron / AMD A4 | Intel i3 / Ryzen 3 |
| RAM | 2 GB | 4 GB |
| Storage | 100 MB free | 500 MB free |
| Display | 1024x768 | 1920x1080 |

---

## 8. Scope & Boundaries

### 8.1 In-Scope (MVP)
- [x] Single-user mode (multi-user v2)
- [x] Chart of Accounts
- [x] Journal Entry
- [x] Trial Balance
- [x] Export to Excel
- [x] Backup/Restore
- [x] Multi-company support

### 8.2 Out-of-Scope (v2)
- [ ] Multi-user with server mode
- [ ] Cloud sync
- [ ] Mobile companion app
- [ ] API for external integration
- [ ] Payroll module
- [ ] Inventory module

---

## 9. Success Metrics

### 9.1 Technical Metrics
| Metric | Target |
|--------|--------|
| Code Coverage | > 80% |
| Bug Count | 0 critical, < 5 minor at release |
| Performance Score | > 90 (Google PageSpeed-like) |

### 9.2 Business Metrics
| Metric | Target |
|--------|--------|
| User Satisfaction | > 4/5 |
| Data Integrity | 100% (no data loss) |
| Export Accuracy | 100% match with screen display |

---

## 10. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| SQLite concurrency issues | Low | Medium | Design for single-user, document multi-user limitations |
| Large data performance | Medium | Low | Implement pagination, indexing, lazy loading |
| PyInstaller false positives | Medium | Low | Sign executable, document clearly |
| Unicode/encoding issues | Medium | High | Use UTF-8 everywhere, test with Indonesian characters |

---

## 11. Appendix

### 11.1 Glossary
| Term | Definition |
|------|------------|
| GL | General Ledger - Buku Besar |
| COA | Chart of Accounts - Daftar Akun |
| Trial Balance | Neraca Saldo |
| Journal Entry | Jurnal Umum |

### 11.2 References
- WISA-CLONE FSD (Functional Specification Document)
- WISA-CLONE TSD (Technical Specification Document)
- WISA-CLONE Task List
- WISA-CLONE Implementation Plan

### 11.3 Related Documents
- Reverse Engineering Report (from original Wisa Accounting)

---

**Document History:**
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-31 | AI Assistant | Initial draft |
