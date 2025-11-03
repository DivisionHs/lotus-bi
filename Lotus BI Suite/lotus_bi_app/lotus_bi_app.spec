# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Lotus BI Suite\\frontend\\lotus_bi_app.py'],
    pathex=['Lotus BI Suite'],
    binaries=[],
    datas=[('Lotus BI Suite/assets/logotipo_oficial.png', 'assets'), ('Lotus BI Suite/assets/lotus_icon.ico', 'assets')],
    hiddenimports=[],
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
    name='lotus_bi_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['Lotus BI Suite\\assets\\lotus_icon.ico'],
)
