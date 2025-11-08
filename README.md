# 📦 JeongHan's Copying Tool – `jh_cp` 3.0.0

[![License](https://img.shields.io/github/license/JeongHan-Bae/jh_cp)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-green.svg)]()
[![Dependencies](https://img.shields.io/badge/Dependencies-None-red.svg)]()

A cross-platform Python CLI and library for structured file copying and archiving,
powered by `.gitignore`-style `.cp_ignore` rules.

Ideal for transferring clean file sets to cloud storage, portable drives, or mobile devices
without pushing `.git` or build artifacts — while keeping directories tidy.

---

## ✨ Features

* Copy or archive files using `.cp_ignore` rules (fully `.gitignore` compatible)
* Built-in exclusion groups for logs, archives, and databases
* Supports `.zip`, `.tar`, `.tar.gz` (`.tgz`)
* Unified CLI and Python API (`jh_cp_main`)
* Zero external dependencies (only `tomli` auto-installed on Python 3.10)

---

## 🔧 Installation

> ✅ Requires **Python ≥ 3.10**

`jh_cp` now uses a proper **module-folder + `__init__.py`** layout,
so both standard `pip install` and PEP 517 builds work cleanly.

### Option 1 — Install Directly

```bash
git clone https://github.com/JeongHan-Bae/jh_cp.git
cd jh_cp
pip install .
```

### Option 2 — Build and Install

```bash
python -m build
pip install dist/jh_cp-3.0.0-py3-none-any.whl
```

---

## 🚀 CLI Overview

`jh_cp` provides four primary subcommands:

| Command     | Purpose                                           |
| ----------- | ------------------------------------------------- |
| `cp`        | Copy files/directories with ignore rules          |
| `archive`   | Create `.zip`/`.tar`/`.tar.gz` archives           |
| `cp_ignore` | Manage or edit ignore rules                       |
| `tree`      | Visualize directory structure with ignore filters |

### Global Help

```bash
jh_cp --help
```

Each subcommand supports `--help`, e.g. `jh_cp archive --help`.

---

## 📂 Copy Files and Directories (`cp`)

```bash
jh_cp cp ./my_project ./backup --exclude-log --create-subdir
```

**Options**

| Flag              | Description                                             |
|-------------------|---------------------------------------------------------|
| `--create-subdir` | Place contents in a subdirectory named after source     |
| `--exclude-zip`   | Skip archives (`*.zip`, `*.tar.gz`, `*.7z`, etc.)       |
| `--exclude-log`   | Skip log files (`*.log`, `*.err`, `*.out`)              |
| `--exclude-db`    | Skip database files (`*.db`, `*.sqlite`, `*.sql`, etc.) |
| `-ignore FILE`    | Use a custom ignore file instead of `.cp_ignore`        |

---

## 📦 Archive Files (`archive`)

```bash
jh_cp archive ./src release.tar.gz --exclude-zip
```

Supports `.zip`, `.tar`, and `.tar.gz` (`.tgz`) formats.
Uses the same ignore/exclude logic as `cp`.

---

## 🌳 Visualize Folder Structure (`tree`)

The `tree` command lets you **easily visualize a project's directory structure** —
perfect for documentation, AI-assisted code analysis, or quick inspection.

```bash
# Draw structure for current directory (default)
jh_cp tree ./

# Draw structure for a specific folder
jh_cp tree ./include

# Use an existing .gitignore file for filtering
jh_cp tree ./include -ignore .gitignore
jh_cp tree ./src -ignore .gitignore
```

Example output:

```
include/
└── jh/
    ├── core/
    │   └── pool.h
    └── macros/
        └── platform.h
```

**Notes**

* Uses the exact same ignore logic as `jh_cp cp` and `jh_cp archive`
* Any ignore file (`.gitignore`, `.cp_ignore`, etc.) can be used via `-ignore`
* Supports `--max-depth N` to limit recursion depth
* Produces clean, AI-friendly, documentation-ready tree output

---

## 🛠 Manage `.cp_ignore` (`cp_ignore`)

```bash
jh_cp cp_ignore -ignore '*.tmp' '*.bak'
jh_cp cp_ignore -register 'README.md'
jh_cp cp_ignore -export myrules.txt
jh_cp cp_ignore -reset
jh_cp cp_ignore -nano
```

* `-ignore` — add patterns to ignore
* `-register` — add patterns to include (`!PATTERN`)
* `-export` / `-reset` — manage rule sets
* `-nano` — open the ignore file in *nano* (Unix-like systems only)

Each command performs one action only; do not mix options.

---

## 🧠 Configuration Files

### `.cp_ignore`

Located at `jh_cp/jh_cp_tools/.cp_ignore`
Implements `.gitignore`-style glob patterns and inclusion rules (`!pattern`).

<details>
<summary>Extend to see details of <code>.cp_ignore</code></summary>

```gitignore
# ----------------------------------------
# jh_cp Ignore Rules File (.cp_ignore)
# ----------------------------------------
# This file defines which files and directories should be ignored
# when using jh_cp's copy or archive commands.
# Patterns here follow glob-style matching.
# Lines starting with "!" are exceptions (inclusions).
# ----------------------------------------

# ----------------------------------------
# Python bytecode & metadata
# ----------------------------------------
*.py[cod]              # Python compiled bytecode (pyc, pyo, etc.)
*.pyc                  # Explicit .pyc files
*.pyo                  # Obsolete compiled files
__pycache__/           # Python cache directory
*.egg-info/            # Package metadata (setuptools)
*.egg                  # Python egg files
pip-wheel-metadata/    # pip build cache
.pytest_cache/         # pytest cache

# ----------------------------------------
# Build & virtual environment directories
# ----------------------------------------
*build*/            # Build directories (wildcard for case-insensitive match)
*Build*/
*BUILD*/
dist/               # Distribution output (wheels, tarballs, etc.)
venv/               # Common virtual environment folder
env/                # Alternative venv folder name

# ----------------------------------------
# System-generated files
# ----------------------------------------
Thumbs.db                 # Windows thumbnail cache
.DS_Store                 # macOS folder view settings
*.swp                     # Vim swap files
*.swo                     # Vim temporary swap files
*.bak                     # Backup files

# ----------------------------------------
# Native & compiled binary artifacts
# ----------------------------------------
bin/                 # Binary output directory
obj/                 # Object files directory
out/                 # Output directory
*debug*/             # Debug builds
*release*/           # Release builds

# ----------------------------------------
# Development & project settings
# ----------------------------------------
.vscode/             # VS Code config
.idea/               # JetBrains IDE config
.git/                # Git repo metadata
.svn/                # Subversion metadata
.tox/                # Tox testing environments
.coverage            # Coverage report data
node_modules/        # Node.js dependencies
```

</details>

### `exclude-rules.ini`

Located at `jh_cp/jh_cp_tools/exclude-rules.ini`
Defines grouped patterns for quick exclusions:

```ini
[exclude-zip]
patterns = *.zip, *.7z, *.tar, *.tar.gz, *.rar, *.tgz

[exclude-log]
patterns = *.log, *.err, *.out

[exclude-db]
patterns = *.db, *.sqlite, *.sql, *.pg, *.mdb
```

---

## 🧩 Embedded Python API

```python
from jh_cp import jh_cp_main

jh_cp_main(["cp", "src", "dest", "--exclude-log"])
jh_cp_main(["archive", "src", "output.tar.gz", "--exclude-zip"])
jh_cp_main(["tree", "src"])
```

CLI and API share the same logic and output pipeline.
Color and error handling are performed by `Host.print()`.

---

## 🧼 Uninstallation

```bash
pip uninstall jh_cp
```

Cleanly removes the CLI and package from your environment.

---

## 🧱 Project Layout

```
jh_cp/
├── jh_cp/
│   ├── jh_cp_tools/
│   │   ├── .cp_ignore
│   │   └── exclude-rules.ini
│   ├── __init__.py
│   ├── jh_cp.py
│   └── jh_cp.pyi
├── LICENSE
├── MANIFEST.in
├── pyproject.toml
├── README.md
└── setup.py
```

---

## ⚙️ Environment & Requirements

* Python ≥ 3.10
* No external dependencies (except `tomli` on 3.10)
* Works on Windows, macOS, and Linux

For development:

```bash
pip install setuptools wheel build
```

---

## 🪪 License

Licensed under the [Apache License 2.0](LICENSE)
© 2025 JeongHan Bae
