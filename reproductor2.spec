# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['reproductor2.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/estudiante/Documents/Escuela/ReproductorPython/icono.ico', '.'), ('C:/Users/estudiante/Documents/Escuela/ReproductorPython/config.ini', '.'), ('C:/Users/estudiante/Documents/Escuela/ReproductorPython/images/*', 'images')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='reproductor2',
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
    icon=['icono.ico'],
)
