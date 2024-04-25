# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['costom_ui2.py'],
    pathex=[],
    binaries=[('.\\static\\ffmpeg\\ffmpeg.exe', '.'), ('.\\static\\ffmpeg\\ffprobe.exe', '.')],
    datas=[('.\\static\\images\\left.png', 'data'), ('.\\static\\images\\right.png', 'data')],
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
    name='costom_ui2',
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
)
