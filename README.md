# 📦 JeongHan’s Copying Tool – `jh_cp` 2.0.0

[![License](https://img.shields.io/github/license/JeongHan-Bae/jh_cp)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-X--platform-green.svg)]()
[![Build](https://img.shields.io/badge/Dependencies-None-red.svg)]()

A cross-platform CLI and Python tool for structured file copying and archiving, with `.cp_ignore` support.

Useful when transferring files to cloud drives or mobile devices **without** Git/SVN, while preserving directory hygiene and avoiding unwanted file uploads.

---

## ✨ Features

* Copy or archive files using `.gitignore`-style `.cp_ignore` rules
* Built-in support to skip logs, archives, and database files
* `.zip`, `.tar`, and `.tar.gz`(`tgz`) archive formats supported
* CLI and embedded Python API for automation workflows
* Zero external dependencies — runs on pure Python ≥ 3.9

---

## 🔧 Installation

> ❌ AVOID `pip install .`   
> ✅ RECOMMEND: use `setup.py build_install clean` for proper packaging and uninstallation.

### Option 1: Direct Install

```bash
git clone https://github.com/JeongHan-Bae/jh_cp.git
cd jh_cp
python setup.py build_install clean
```

Ensures all config/metadata files are installed and tracked by `pip uninstall`.

### Option 2: Build a Wheel for Distribution

```bash
python setup.py sdist bdist_wheel clean
```
This creates a distributable package in the `dist/` directory.

Then install it with:
```bash
pip install dist/jh_cp-2.0.0-py3-none-any.whl
```

You can also download pre-built `.whl` or `.tar.gz` packages from the [Releases](https://github.com/JeongHan-Bae/jh_cp/releases) page 
and install them directly with the command above.

---

## 🚀 CLI Usage

```bash
jh_cp --help
```

> 💡 Run `jh_cp --help` to see all available commands.  
> Each subcommand also supports `--help`, e.g. `jh_cp cp --help`

### 📂 Copy with Ignore Rules

```bash
jh_cp cp ./my_project ./backup --exclude-log --create-subdir
```

* Ignores patterns from `.cp_ignore`
* Skips logs (`*.log`, `*.err`, `*.out`)
* Optionally creates a subdirectory

**Flags**:

* `--exclude-zip`: Skip archives (`*.zip`, `*.tar.gz`, `*.7z`)
* `--exclude-db`: Skip databases (`*.db`, `*.sqlite`, `*.sql`, etc.)
* `--create-subdir`: Put content in a new folder named after the source
* `-ignore FILE`: Use a custom ignore file instead of `.cp_ignore`

---

### 📦 Archive with Ignore Rules

```bash
jh_cp archive ./my_project release.tar.gz --exclude-zip
```

Supported formats:

* `.zip`
* `.tar`
* `.tar.gz` or `.tgz`

**Flags**:  
Same as copy command. See above.

---
### 🛠 Manage `.cp_ignore` Rules

The `.cp_ignore` file defines what to skip during copy/archive. You can manage it via the `cp_ignore` subcommand.

Each command call performs **one specific action** — no mixing.

```bash
# Add patterns to ignore
jh_cp cp_ignore -ignore '*.tmp' '*.log'

# Mark files as always included (inverted ignore)
jh_cp cp_ignore -register 'README.md' '*.cfg'

# Export current rules to a file
jh_cp cp_ignore -export myrules.txt

# Reset to built-in default rules
jh_cp cp_ignore -reset

# Manually edit the .cp_ignore file (opens in nano)
jh_cp cp_ignore -nano
```

> ✅ Supports **multiple patterns** per call (quoted if using wildcards)
> ❌ Do **not** mix different options in a single command (`-ignore` + `-register` = ❌)

#### 🔍 Shell Wildcard Tip

When using wildcards like `*.log`, always quote them:

```bash
# ✅ Correct
jh_cp cp_ignore -ignore '*.log' '*.bak'

# ❌ Incorrect – may cause "no matches found" error in bash/zsh
jh_cp cp_ignore -ignore *.log *.bak
```

This ensures the patterns are passed as-is to the program instead of being expanded by your shell.

---

## 📚 Embedded Python API

All CLI behavior can be used from Python:

```python
from jh_cp import jh_cp_main

# Copy example
jh_cp_main(["cp", "src_dir", "dst_dir", "--exclude-log"])

# Archive example
jh_cp_main(["archive", "src", "output.tar.gz", "--exclude-zip"])
```

Perfect for scripting or integrating into other Python tools.

---

## 🧠 Ignore Config Format

### [`.cp_ignore`](jh_cp_tools/.cp_ignore)

Supports `.gitignore`-like rules:

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
**/__pycache__/        # Python cache directory
**/*.egg-info/         # Package metadata (setuptools)
*.egg                  # Python egg files
**/pip-wheel-metadata/ # pip build cache

# ----------------------------------------
# Build & virtual environment directories
# ----------------------------------------
**/*build*/            # Build directories (wildcard for case-insensitive match)
**/*Build*/
**/*BUILD*/
**/dist/               # Distribution output (wheels, tarballs, etc.)
**/venv/               # Common virtual environment folder
**/env/                # Alternative venv folder name

# ----------------------------------------
# System-generated files
# ----------------------------------------
Thumbs.db              # Windows thumbnail cache
.DS_Store              # macOS folder view settings
*.swp                  # Vim swap files
*.swo                  # Vim temporary swap files
*.bak                  # Backup files

# ----------------------------------------
# Native & compiled binary artifacts
# ----------------------------------------
**/bin/                 # Binary output directory
**/obj/                 # Object files directory
**/out/                 # Output directory
**/*debug*/             # Debug builds
**/*release*/           # Release builds

# ----------------------------------------
# Development & project settings
# ----------------------------------------
**/.vscode/             # VS Code config
**/.idea/               # JetBrains IDE config
**/.git/                # Git repo metadata
**/.svn/                # Subversion metadata
**/.tox/                # Tox testing environments
**/.coverage            # Coverage report data
**/node_modules/        # Node.js dependencies
```

</details>

### [`exclude-rules.ini`](jh_cp_tools/exclude-rules.ini)

Grouped pattern-based exclusions:

<details>
<summary>Extend to see details of <code>exclude-rules.ini</code></summary>

```ini
[exclude-zip]
patterns = *.zip, *.7z, *.tar, *.tar.gz, *.rar, *.gz, *.tgz

[exclude-log]
patterns = *.log, *.err, *.out

[exclude-db]
patterns = *.db, *.sql, *.pg, *.mdb, *.sqlite, *.sqlite3, *.accdb, *.dbf, *.ndf, *.ldf, *.frm, *.ibd
```

</details>

---

## 🧼 Uninstallation

```bash
pip uninstall jh_cp
```

Removes `jh_cp` and its config from your Python environment.

---

## 🛠 Requirements

* **Python 3.9+**
* No external dependencies required

To build locally:

```bash
pip install setuptools~=75.6.0 wheel~=0.45.1
```

---

## 🪪 License

Apache License 2.0 © 2025 JeongHan Bae
See [LICENSE](LICENSE) for full terms.
