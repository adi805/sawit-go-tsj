# WISA-CLONE - Functional Specification Document (FSD)

**Versi:** 1.0  
**Tanggal:** 2026-03-31  
**Status:** Draft  
**Author:** AI Assistant  

---

## 1. Introduction

### 1.1 Purpose
Dokumen ini menjelaskan spesifikasi fungsional aplikasi WISA-CLONE, termasuk:
- Screen/Form layouts
- User interactions & workflows
- Data validation rules
- Business logic

### 1.2 Scope
Fokus pada **MVP (Minimum Viable Product)** - Core GL functionality

---

## 2. Application Structure

### 2.1 Screen Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                        WISA-CLONE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐                                                │
│  │   LOGIN    │◄── Entry Point                                 │
│  └──────┬──────┘                                                │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┤
│  │                      MAIN WINDOW                            │
│  ├─────────────────────────────────────────────────────────────┤
│  │  MENU BAR                                                   │
│  │  ┌──────────┬──────────┬──────────┬──────────┬──────────┐   │
│  │  │  File    │  Master  │Transaksi│ Laporan  │   Help   │   │
│  │  └──────────┴──────────┴──────────┴──────────┴──────────┘   │
│  ├─────────────────────────────────────────────────────────────┤
│  │  TOOLBAR                                                    │
│  │  [New] [Save] [Delete] [Refresh] │ [Company: ▼] │ [User]   │
│  ├─────────────────────────────────────────────────────────────┤
│  │                                                              │
│  │                    CONTENT AREA                              │
│  │                                                              │
│  │   (Dynamic content based on menu selection)                 │
│  │                                                              │
│  │                                                              │
│  ├─────────────────────────────────────────────────────────────┤
│  │  STATUS BAR: [Company] │ [User] │ [DB Status] │ [Time]    │
│  └─────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Menu Structure

```
┌─────────────────────────────────────────────────────────────────┐
│ File │ Master │ Transaksi │ Laporan │ Help │
├──────┴────────┴───────────┴─────────┴──────┤
│                                                    │
│ File                                               │
│ ├─ New Company        (Ctrl+Shift+N)              │
│ ├─ Open Database      (Ctrl+O)                   │
│ ├─ Backup Database    (Ctrl+B)                   │
│ ├─ Restore Database   (Ctrl+R)                   │
│ ├─ ─────────────────────────                     │
│ ├─ Export to Excel    (Ctrl+E)                   │
│ ├─ Import from Excel  (Ctrl+I)                   │
│ ├─ ─────────────────────────                     │
│ ├─ Settings          (Ctrl+,)                    │
│ ├─ ─────────────────────────                     │
│ └─ Exit              (Alt+F4)                    │
│                                                    │
│ Master                                            │
│ ├─ Organization                                   │
│ ├─ ─────────────────────────                      │
│ ├─ GL Accounts       (Ctrl+G)                    │
│ ├─ SL Accounts       (Ctrl+L)                    │
│ ├─ FS Accounts       (Ctrl+F)                    │
│ └─ FS Elements                                    │
│                                                    │
│ Transaksi                                         │
│ ├─ Journal Entry     (Ctrl+J)                    │
│ └─ Journal List       (Ctrl+Shift+J)              │
│                                                    │
│ Laporan                                           │
│ ├─ Trial Balance     (Ctrl+T)                    │
│ ├─ General Ledger    (Ctrl+Shift+G)              │
│ ├─ Journal Report    (Ctrl+Shift+R)              │
│ ├─ ─────────────────────────                     │
│ ├─ Balance Sheet                                  │
│ └─ Profit & Loss                                 │
│                                                    │
│ Help                                              │
│ ├─ User Guide                                    │
│ ├─ Keyboard Shortcuts                             │
│ ├─ ─────────────────────────                     │
│ └─ About                                          │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 3. Screen Specifications

### 3.1 Login Screen

```
┌────────────────────────────────────────┐
│                                        │
│         ┌──────────────────┐           │
│         │   📒 WISA-CLONE  │           │
│         │   Accounting      │           │
│         └──────────────────┘           │
│                                        │
│    ┌─────────────────────────────┐     │
│    │ Username                     │     │
│    │ [________________________]   │     │
│    └─────────────────────────────┘     │
│                                        │
│    ┌─────────────────────────────┐     │
│    │ Password                     │     │
│    │ [________________________]   │     │
│    └─────────────────────────────┘     │
│                                        │
│    [x] Remember me                    │
│                                        │
│    ┌─────────────────────────────┐     │
│    │         LOGIN               │     │
│    └─────────────────────────────┘     │
│                                        │
│    ┌─────────────────────────────┐     │
│    │   Create New Account        │     │
│    └─────────────────────────────┘     │
│                                        │
│    ┌─────────────────────────────┐     │
│    │    Open Existing Database   │     │
│    └─────────────────────────────┘     │
│                                        │
│    Version 1.0.0                      │
└────────────────────────────────────────┘
```

**Fields:**
| Field | Type | Validation | Required |
|-------|------|------------|----------|
| Username | Text | 3-50 chars, alphanumeric | Yes |
| Password | Password | 6-50 chars | Yes |
| Remember me | Checkbox | - | No |

**Actions:**
- `Login` → Validate credentials → Open Main Window
- `Create New Account` → Open Registration Dialog
- `Open Existing Database` → Open file dialog for .db file

### 3.2 Main Window

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 📒 WISA-CLONE - [Company Name]                         [_][□][X]     │
├─────────────────────────────────────────────────────────────────────────┤
│ File │ Master │ Transaksi │ Laporan │ Help                              │
├─────────────────────────────────────────────────────────────────────────┤
│ [+New] [💾Save] [🗑️Delete] [🔄Refresh]  │ Company: [PT Contoh ▼] │ User: Admin │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐  ┌─────────────────────────────────────────────────┐  │
│  │ NAVIGATION  │  │                                                 │  │
│  │             │  │              CONTENT AREA                        │  │
│  │ ▼ Master    │  │                                                 │  │
│  │   ├ GL Acct │  │   (Screen content changes based on              │  │
│  │   ├ SL Acct │  │    selected navigation item)                    │  │
│  │   └ FS Acct │  │                                                 │  │
│  │             │  │                                                 │  │
│  │ ▼ Transaksi│  │                                                 │  │
│  │   ├ Jurnal │  │                                                 │  │
│  │   └ List   │  │                                                 │  │
│  │             │  │                                                 │  │
│  │ ▼ Laporan  │  │                                                 │  │
│  │   ├ Trial  │  │                                                 │  │
│  │   ├ GL     │  │                                                 │  │
│  │   └ Journal│  │                                                 │  │
│  │             │  │                                                 │  │
│  └─────────────┘  └─────────────────────────────────────────────────┘  │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│ Ready │ Company: PT Contoh │ User: Admin │ DB: ./data/gl.db │ 10:30:45 │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.3 GL Accounts Screen

```
┌─────────────────────────────────────────────────────────────────────────┐
│ GL Accounts                                            [+Add] [Save] │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Filter: [Search...        ] [Active Only ☑] [Show All ☐]              │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ ☑ │ Account Code │ Account Name          │ Type     │ Balance │   │
│  ├────┼──────────────┼────────────────────────┼───────────┼─────────┤   │
│  │ ☑ │ 1-0000       │ AKTIVA                 │ Header    │    -    │   │
│  │   │  ├ 1-1000    │   Aktiva Lancar        │ Header    │    -    │   │
│  │   │  │ ├ 1-1100  │     Kas                │ Detail    │ 10,000  │   │
│  │   │  │ ├ 1-1200  │     Bank               │ Detail    │ 50,000  │   │
│  │   │  │ └ 1-1300  │     Piutang            │ Detail    │ 25,000  │   │
│  │   │  └ 1-2000    │   Aktiva Tetap         │ Header    │    -    │   │
│  │   │     └ 2-1000 │     Kendaraan           │ Detail    │100,000  │   │
│  │ ☑ │ 2-0000       │ KEWAJIBAN             │ Header    │    -    │   │
│  │   │  ├ 2-1000    │   Hutang Lancar        │ Header    │    -    │   │
│  │   │  │ └ 2-1100  │     Hutang Dagang      │ Detail    │ 30,000  │   │
│  │ ☑ │ 3-0000       │ MODAL                 │ Header    │    -    │   │
│  │ ☑ │ 4-0000       │ PENDAPATAN            │ Header    │    -    │   │
│  │ ☑ │ 5-0000       │ BEBAN                  │ Header    │    -    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─ DETAIL PANEL ────────────────────────────────────────────────────┐  │
│  │ Account Code : [1-1100        ]  Parent : [1-1000 ▼]            │  │
│  │ Account Name : [Kas                                         ]  │  │
│  │ Account Type : [Detail ▼]  FS Mapping : [Kas ▼]                │  │
│  │ Initial Bal  : [0          ]  Currency : [IDR ▼]                │  │
│  │ Description  : [                                           ]  │  │
│  │ ─────────────────────────────────────────────────────────────── │  │
│  │ [☑] Active    [ ] Allow Entry   [☑] Show in Trial Balance       │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

**Fields:**
| Field | Type | Validation | Required |
|-------|------|------------|----------|
| Account Code | Text | Unique, format: X-XXXX | Yes |
| Parent | ComboBox | Valid parent account | No |
| Account Name | Text | Max 100 chars | Yes |
| Account Type | ComboBox | Header/Detail | Yes |
| FS Mapping | ComboBox | Valid FS account | No |
| Initial Balance | Number | >= 0 | No |
| Currency | ComboBox | IDR (default) | Yes |

### 3.4 Journal Entry Screen

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Journal Entry - NEW                                        [Save] [Cancel] │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─ HEADER ───────────────────────────────────────────────────────────┐  │
│  │ Journal No : [AUTO        ]  Date : [31/03/2026    📅]           │  │
│  │ Reference  : [____________]  Period : [Maret 2026    ▼]           │  │
│  │ Description: [Kas ke Bank untuk modal awal                      ]  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─ LINE ITEMS ──────────────────────────────────────────────────────┐  │
│  │ No │ Account (Code - Name)        │ Debit          │ Credit        │  │
│  ├───┼──────────────────────────────┼────────────────┼───────────────┤  │
│  │ 1  │ [1-1100     ▼] Kas          │ [Rp 100,000,00]│ [Rp 0,00     ] │  │
│  │ 2  │ [3-1000     ▼] Modal        │ [Rp 0,00     ]│ [Rp 100,000,00] │  │
│  │ 3  │ [+ Add Line]                │              │               │  │
│  ├───┼──────────────────────────────┼────────────────┼───────────────┤  │
│  │   │ TOTAL                       │ [Rp 100,000,00]│ [Rp 100,000,00] │  │
│  │   │ STATUS                      │ [✓ BALANCED   ]│               │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─ ACTIONS ─────────────────────────────────────────────────────────┐  │
│  │ [+ Add Line]  [Remove Selected]  [Auto Balance]  [Clear All]   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  Notes: [____________________________________________________________]  │
│  Attachment: [Choose File...] [file.pdf] [x]                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Validation Rules:**
| Rule | Description | Error Message |
|------|-------------|--------------|
| V001 | Total Debit = Total Credit | "Jumlah debit dan kredit harus sama" |
| V002 | At least 2 line items | "Minimal harus ada 2 baris jurnal" |
| V003 | No empty accounts | "Semua baris harus memiliki akun" |
| V004 | Valid account codes | "Kode akun tidak valid" |
| V005 | No future dates | "Tanggal tidak boleh di masa depan" |

### 3.5 Trial Balance Screen

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Trial Balance                                           [🔍Filter] [📥Export] │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Period : [Dari: 📅01/03/2026] [Sampai: 📅31/03/2026] [Apply]         │
│  Company: [PT Contoh ▼]  Currency: [IDR ▼]                             │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Account Code │ Account Name              │ Debit      │ Credit   │   │
│  ├──────────────┼───────────────────────────┼────────────┼──────────┤   │
│  │ 1-1100      │ Kas                       │ 10,000,000 │         │   │
│  │ 1-1200      │ Bank                      │ 50,000,000 │         │   │
│  │ 1-1300      │ Piutang                   │ 25,000,000 │         │   │
│  │ 2-1100      │ Hutang Dagang             │            │ 30,000,000│   │
│  │ 3-1000      │ Modal                     │            │ 55,000,000│   │
│  │ 4-1000      │ Penjualan                 │            │ 10,000,000│   │
│  │ 5-1000      │ Beban Gaji                │ 10,000,000 │         │   │
│  ├──────────────┼───────────────────────────┼────────────┼──────────┤   │
│  │             │ TOTAL                     │ 95,000,000 │ 95,000,000│   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  Status: ✓ BALANCED                                                     │
│  Generated: 31/03/2026 10:45:12                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Validation Rules

### 4.1 Account Code Format
```
Pattern: X-XXXX or XX-XXXX or XXX-XXXX
Where X = 0-9

Examples:
✓ 1-0000 (Valid)
✓ 11-1000 (Valid)
✓ 111-1000 (Valid)
✗ 1-000 (Too short)
✗ ABC-1000 (Contains letters)
✗ 1--1000 (Double dash)
```

### 4.2 Journal Entry Validation
```python
def validate_journal_entry(journal):
    errors = []
    
    # V001: Must have at least 2 lines
    if len(journal.lines) < 2:
        errors.append("Minimal harus ada 2 baris jurnal")
    
    # V002: Debit = Credit
    total_debit = sum(line.debit for line in journal.lines)
    total_credit = sum(line.credit for line in journal.lines)
    if abs(total_debit - total_credit) > 0.01:
        errors.append("Jumlah debit dan kredit tidak sama")
    
    # V003: No empty accounts
    for i, line in enumerate(journal.lines):
        if not line.account_id:
            errors.append(f"Baris {i+1}: Akun tidak boleh kosong")
    
    return errors
```

---

## 5. User Interactions

### 5.1 Keyboard Shortcuts

| Shortcut | Action | Context |
|----------|--------|---------|
| `Ctrl+N` | New Record | Global |
| `Ctrl+S` | Save | Global |
| `Ctrl+D` | Delete | Global |
| `Ctrl+F` | Find/Search | Global |
| `Ctrl+G` | GL Accounts | Global |
| `Ctrl+J` | Journal Entry | Global |
| `Ctrl+T` | Trial Balance | Global |
| `Ctrl+E` | Export | Global |
| `Ctrl+B` | Backup | Global |
| `F5` | Refresh | Global |
| `Esc` | Cancel/Close | Global |

### 5.2 Mouse Interactions

| Interaction | Component | Action |
|-------------|-----------|--------|
| Single Click | Grid Row | Select Row |
| Double Click | Grid Row | Edit Row |
| Right Click | Grid Row | Context Menu |
| Drag | Column Header | Reorder Column |
| Resize | Column Edge | Resize Column |
| Scroll | Grid | Vertical Scroll |
| Ctrl+Scroll | Grid | Horizontal Scroll |

### 5.3 Context Menus

**Grid Context Menu:**
```
┌─────────────────────────┐
│ Add New                 │
│ Edit                    │
│ Delete                  │
│ ─────────────────────── │
│ Copy                    │
│ Paste                   │
│ ─────────────────────── │
│ Export Selected to Excel│
│ Print Selected          │
└─────────────────────────┘
```

---

## 6. Error Handling

### 6.1 Error Types

| Error Type | Icon | Color | Action |
|------------|------|-------|--------|
| Validation Error | ⚠️ | Yellow | Show inline message |
| Database Error | ❌ | Red | Show dialog, log error |
| Network Error | 🌐 | Red | Show retry dialog |
| System Error | 💀 | Red | Show dialog, exit app |

### 6.2 Error Dialog Template

```
┌─────────────────────────────────────────┐
│ ⚠️ Error                                  │
├─────────────────────────────────────────┤
│                                          │
│   Message: [Error description here]     │
│                                          │
│   Error Code: ERR-XXX-001               │
│                                          │
│   ┌─────────┐  ┌─────────┐              │
│   │   OK    │  │ Details │              │
│   └─────────┘  └─────────┘              │
│                                          │
└─────────────────────────────────────────┘
```

---

## 7. Workflows

### 7.1 Create Journal Entry Flow

```
START
  │
  ▼
┌──────────────────┐
│ Click Transaksi  │
│ → Journal Entry  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Fill Header      │
│ (Date, Ref)     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Add Line Items   │◄────────────┐
│ (Account, D/C)   │             │
└────────┬─────────┘             │
         │                       │
         ▼                       │
┌──────────────────┐             │
│ Validate Entry   │             │
│ (Debit = Credit) │             │
└────────┬─────────┘             │
         │                       │
    ┌────┴────┐                  │
    │ Valid?  │                  │
    └────┬────┘                  │
     Yes │     No                │
    ┌────┴────┐                  │
    │         │                  │
    ▼         ▼                  │
┌────────┐ ┌──────────────────┐  │
│  Save  │ │ Show Error       │──┘
└───┬────┘ │ Message          │
    │      └──────────────────┘
    ▼
┌──────────────────┐
│ Success Message  │
│ "Jurnal saved"   │
└────────┬─────────┘
         │
         ▼
       END
```

### 7.2 Export to Excel Flow

```
START
  │
  ▼
┌──────────────────┐
│ Select Report    │
│ Type             │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Apply Filters    │
│ (Date Range)     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Click Export     │
│ Button           │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Choose Format    │
│ (xlsx / csv)     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Select Location  │
│ Save File Dialog │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Generate Excel   │
│ (openpyxl)       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Success!         │
│ Open File?       │
└────────┬─────────┘
         │
    ┌────┴────┐
    │   Yes   │
    └────┬────┘
         ▼
    ┌─────────┐
    │  Open   │
    │  File   │
    └────┬────┘
         │
         ▼
       END
```

---

## 8. Appendix

### 8.1 Screen List (MVP)

| Screen ID | Screen Name | Priority |
|-----------|-------------|----------|
| SCR-001 | Login | HIGH |
| SCR-002 | Main Window | HIGH |
| SCR-003 | GL Accounts | HIGH |
| SCR-004 | SL Accounts | HIGH |
| SCR-005 | FS Accounts | HIGH |
| SCR-006 | Journal Entry | HIGH |
| SCR-007 | Journal List | HIGH |
| SCR-008 | Trial Balance | HIGH |
| SCR-009 | General Ledger | MEDIUM |
| SCR-010 | Journal Report | MEDIUM |
| SCR-011 | Balance Sheet | MEDIUM |
| SCR-012 | Profit & Loss | MEDIUM |
| SCR-013 | Settings | MEDIUM |
| SCR-014 | Backup/Restore | HIGH |

### 8.2 Component Library

| Component | Widget | States |
|-----------|--------|--------|
| Button Primary | QPushButton | Normal, Hover, Pressed, Disabled |
| Button Secondary | QPushButton | Normal, Hover, Pressed, Disabled |
| Input Field | QLineEdit | Normal, Focus, Error, Disabled |
| ComboBox | QComboBox | Normal, Open, Disabled |
| Table | QTableView | Normal, Selected, Editing |
| DatePicker | QDateEdit | Normal, Calendar Open |
| Dialog | QDialog | Modal, Non-Modal |
| MessageBox | QMessageBox | Info, Warning, Error, Question |

---

**Document History:**
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-31 | AI Assistant | Initial draft |
