# 🌴 Sawit Go - TSJ

> **Sistem Akuntansi Modern untuk Perkebunan Sawit - Ringan, Fleksibel, dan Bisa Jalan di Mana Saja**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Development-yellow.svg)

---

## 📋 Tentang Project

**Sawit Go - TSJ** adalah aplikasi akuntansi desktop modern berbasis Python + PyQt6 dengan database SQLite yang ringan namun powerful. Dibangun untuk memenuhi kebutuhan akuntansi perusahaan perkebunan kelapa sawit (**PT Tulas Sakti Jaya**) dengan fitur-fitur essential seperti Chart of Accounts, Journal Entry, Trial Balance, dan export ke Excel.

### ✨ Fitur Utama

- 📒 **Chart of Accounts** - GL Accounts dengan hierarchy tree view
- 📝 **Journal Entry** - Double-entry validation (Debit = Kredit)
- 📊 **Trial Balance** - Neraca Saldo dengan filter periode
- 📄 **Excel Export** - Semua data bisa export ke .xlsx
- 💾 **Backup/Restore** - Database backup ke file .db
- 🔐 **Multi-User** - Role-based access (Admin, User, Viewer)
- 🏢 **Multi-Company** - Support multiple perusahaan

### 🎯 Target Pengguna

- UMKM / Perusahaan perkebunan kelapa sawit
- Akuntan yang butuh sistem akuntansi sederhana namun powerful
- Pengguna yang butuh aplikasi ringan tanpa requirements tinggi

---

## 💻 System Requirements

| Komponen | Minimum | Recommended |
|----------|---------|-------------|
| **OS** | Windows 7 64-bit | Windows 10/11 64-bit |
| **CPU** | Intel Celeron / AMD A4 | Intel i3 / Ryzen 3 |
| **RAM** | 2 GB | 4 GB |
| **Storage** | 100 MB free | 500 MB free |

---

## 🚀 Instalasi

### Methode 1: Download Installer (Recommended)

1. Download versi terbaru dari [Releases](https://github.com/adi805/sawit-go-tsj/releases)
2. Jalankan `SawitGo-TSJ_Setup_vX.X.X.exe`
3. Ikuti instruksi instalasi
4. Jalankan aplikasi dari Start Menu

### Methode 2: Dari Source Code

```bash
# Clone repository
git clone https://github.com/adi805/sawit-go-tsj.git
cd sawit-go-tsj

# Buat virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
python src/main.py
```

### Methode 3: Build Sendiri

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python scripts/build_exe.py

# Executable akan ada di folder dist/
dist/SawitGo-TSJ.exe
```

---

## 📁 Struktur Project

```
sawit-go-tsj/
├── src/                    # Source code
│   ├── main.py            # Entry point
│   ├── app.py            # Application class
│   ├── models/           # SQLAlchemy models
│   ├── services/         # Business logic
│   ├── repositories/     # Data access
│   ├── ui/               # PyQt6 UI
│   └── utils/            # Utilities
├── tests/                 # Unit tests
├── docs/                  # Documentation
├── scripts/              # Build scripts
├── .github/              # GitHub Actions
├── requirements.txt
└── README.md
```

---

## 📚 Dokumentasi

| Document | Description |
|----------|-------------|
| [PRD.md](docs/PRD.md) | Product Requirements Document |
| [FSD.md](docs/FSD.md) | Functional Specification |
| [TSD.md](docs/TSD.md) | Technical Specification |
| [TASK_LIST.md](docs/TASK_LIST.md) | Task Breakdown |
| [IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) | Implementation Plan |
| [SPEC.md](SPEC.md) | Project Specification |

---

## 🔄 Update Mechanism

Aplikasi mendukung auto-update via GitHub Releases:

1. Saat startup, aplikasi akan cek versi terbaru
2. Jika ada update, akan muncul notifikasi
3. User bisa download dan install versi terbaru
4. Untuk manual update: download dari [Releases](https://github.com/adi805/sawit-go-tsj/releases)

### Versioning

Format versi: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

---

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/adi805/sawit-go-tsj.git
cd sawit-go-tsj

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dev dependencies
pip install -r requirements.txt
pip install pytest pytest-cov ruff

# Run tests
pytest tests/ -v

# Run linter
ruff check src/
```

### Build Executable

```bash
python scripts/build_exe.py
```

Output akan ada di `dist/SawitGo-TSJ.exe`

---

## 📝 Changelog

Lihat [CHANGELOG.md](CHANGELOG.md) untuk history perubahan.

---

## 🤝 Contributing

1. Fork repository ini
2. Buat feature branch (`git checkout -b feature/nama-feature`)
3. Commit perubahan (`git commit -m 'Add nama-feature'`)
4. Push ke branch (`git push origin feature/nama-feature`)
5. Buat Pull Request

---

## 📄 License

Project ini menggunakan MIT License - lihat file [LICENSE](LICENSE)

**Copyright (c) 2026 Syafriadi - PT Tulas Sakti Jaya**

---

## 👤 Owner

| Info | Details |
|------|---------|
| **Owner** | Syafriadi |
| **Company** | PT Tulas Sakti Jaya |
| **Project** | Sawit Go - TSJ |
| **Email** | syafriadi@tsj.co.id |

---

## 🔗 Links

- 🌐 **Repository**: https://github.com/adi805/sawit-go-tsj
- 📦 **Releases**: https://github.com/adi805/sawit-go-tsj/releases
- 🐛 **Issues**: https://github.com/adi805/sawit-go-tsj/issues

---

<div align="center">

**Made with ❤️ by AI Assistant for PT Tulas Sakti Jaya**

</div>
