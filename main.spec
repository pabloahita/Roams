# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('basededatos.db', '.')],
    hiddenimports=['subprocess', 'sys', 'flask', 'pydantic', 'flask_restx', 're', 'sqlite3', 'cliente', 'dbhelper', 'email_validator', 'importlib_resources.trees'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
