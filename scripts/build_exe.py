#!/usr/bin/env python3
"""
Build script for Sawit Go - TSJ
Compiles the application into a single .exe file using PyInstaller
"""

import os
import sys
import shutil
import PyInstaller.__main__

def clean_build():
    """Clean previous build artifacts"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}/...")
            shutil.rmtree(dir_name)

def build_exe():
    """Build the executable using PyInstaller"""
    
    print("=" * 60)
    print("Building Sawit Go - TSJ")
    print("=" * 60)
    
    # PyInstaller arguments
    args = [
        'src/main.py',                    # Entry point
        '--name=SawitGo-TSJ',            # Executable name
        '--onefile',                     # Single executable
        '--windowed',                    # No console window
        '--icon=resources/icons/app.ico', # App icon (if exists)
        '--add-data=resources;resources',  # Include resources
        '--hidden-import=PyQt6',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=sqlalchemy',
        '--hidden-import=openpyxl',
        '--hidden-import=pandas',
        '--hidden-import=bcrypt',
        '--hidden-import=loguru',
        '--collect-submodules=PyQt6',    # Include all PyQt6 modules
        '--collect-submodules=sqlalchemy',
        '--noconfirm',                   # Overwrite without asking
        '--clean',                       # Clean build
    ]
    
    # Add version info if on Windows
    if sys.platform == 'win32':
        args.append('--version-file=version_info.txt')
    
    print(f"\nPyInstaller arguments: {' '.join(args)}\n")
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    # Verify build
    exe_path = 'dist/SawitGo-TSJ.exe'
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"\n{'=' * 60}")
        print(f"✅ Build successful!")
        print(f"   Executable: {exe_path}")
        print(f"   Size: {size_mb:.2f} MB")
        print(f"{'=' * 60}")
    else:
        print(f"\n❌ Build failed - executable not found!")
        sys.exit(1)

def create_version_info():
    """Create version info file for Windows"""
    version_info = '''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [
            StringStruct(u'CompanyName', u'Syafriadi - PT Tulas Sakti Jaya'),
            StringStruct(u'FileDescription', u'Sistem Akuntansi Sawit Go'),
            StringStruct(u'FileVersion', u'1.0.0.0'),
            StringStruct(u'InternalName', u'SawitGo-TSJ'),
            StringStruct(u'OriginalFilename', u'SawitGo-TSJ.exe'),
            StringStruct(u'ProductName', u'Sawit Go - TSJ'),
            StringStruct(u'ProductVersion', u'1.0.0.0'),
            StringStruct(u'LegalCopyright', u'Copyright (c) 2026 Syafriadi'),
          ]
        )
      ]
    )
  ]
)
'''
    with open('version_info.txt', 'w') as f:
        f.write(version_info)
    print("Created version_info.txt")

if __name__ == '__main__':
    # Create version info if on Windows
    if sys.platform == 'win32':
        create_version_info()
    
    # Clean and build
    clean_build()
    build_exe()
