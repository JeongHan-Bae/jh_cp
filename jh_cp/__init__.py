"""
jh_cp — JeongHan's Copying Tool
================================

A cross-platform file management utility that provides gitignore-style
rules for copy, archive, and tree visualization commands.

This tool allows Python developers to perform advanced file operations
while respecting `.cp_ignore` patterns, mirroring `.gitignore` behavior.
It supports recursive directory copying, selective archiving, and visual
directory inspection with exclusion rules.

Main Features
-------------
- **cp** — Copy files or directories using ignore rules
- **archive** — Create `.zip` / `.tar` / `.tar.gz` archives with ignore rules
- **tree** — Display directory structure excluding ignored files
- **cp_ignore** — Manage `.cp_ignore` configuration (register, reset, export)
- Full `.gitignore` syntax support (comments, `!include`, `**` wildcards)
- Cross-platform colorized output for Unix / Windows terminals
- Optional exclusion presets via `exclude-rules.ini`

Author
------
JeongHan Bae <mastropseudo@gmail.com>

License
-------
Apache License 2.0

See: https://github.com/JeongHan-Bae/jh_cp/blob/main/LICENSE
"""
from .jh_cp import *