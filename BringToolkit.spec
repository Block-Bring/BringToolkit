# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('core/config', 'core/config'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不必要的模块以减小体积
        'tkinter',
        'unittest',
        'doctest',
        'test',
        'pydoc',
        'distutils',
        'setuptools',
        'pkg_resources',
    ],
    noarchive=False,
    optimize=2,  # 优化字节码
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='BringToolkit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # 移除符号表
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False = 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icon.ico',  # 添加图标
)
