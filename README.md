
# JeongHan's Copying Tool: `jh_cp`

## Overview

`jh_cp` is a command-line utility for copying files and directories while respecting customizable ignore rules. The tool allows for the exclusion of specific file types or directories from being copied, making it especially useful for tasks like backup or file synchronization. Additionally, it offers functionality to manage the `.cp_ignore` file and provides flexible rules for different environments.

### Features

- **File Copying (`cp`)**: Copy files directly (like the standard `cp` command). If copying a directory, the tool applies the ignore mechanism (e.g., `*.log`, `node_modules/`). Additionally, if the target directory does not exist, it will be created automatically.
- **Manage `.cp_ignore` File (`cp_ignore`)**: Register new formats to ignore, export the current ignore rules, reset them, or open the `.cp_ignore` file for manual editing.
- **Cross-Platform**: Works on both Unix-like systems (macOS, BSD, Linux) and Windows.

---

### Installation

To install `jh_cp`, clone the repository and ensure you have Python 3.9+:
(for better I/O performance and cooler type hints.)

```bash
git clone https://github.com/JeongHan-Bae/jh_cp.git
cd jh_cp
pip install .
```

---

## Usage

---

### `cp` Subcommand

The `cp` subcommand allows users to copy files or directories from a source to a target while respecting specific exclusion rules. Additionally, it ensures safe recursive copying without the risk of copying the target directory into itself.

#### Command Syntax:

```bash
jh_cp cp [-h] [-ignore IGNORE] [--exclude-zip] [--exclude-log] [--exclude-db] [--create-subdir] src target
```

#### Options:
- `-h`, `--help`: Show help message and exit.
- `-ignore IGNORE`: Specify a custom ignore file path.
- `--exclude-zip`: Exclude files matching zip-related patterns (e.g., `*.zip`, `*.7z`, `*.tar.gz`).
- `--exclude-log`: Exclude files matching log-related patterns (e.g., `*.log`, `*.err`).
- `--exclude-db`: Exclude files matching database-related patterns (e.g., `*.db`, `*.sql`).
- `--create-subdir`: Create a subdirectory with the same name as the source directory in the target directory.

#### Arguments:
- **`src`**: Source path. This can be either a **file** or a **directory**.
- **`target`**: Target path. This must be a **directory**.

#### Behavior:
- **File Copying**: If the source is a file, it will be copied directly to the target directory.
- **Directory Copying**: If the source is a directory, the contents will be copied to the target directory, and files matching the exclusion rules will be ignored. 
- **Target Directory Creation**: If the target directory does not exist, it will be created automatically.
- **Preventing Self-Copying**: If the target directory is a subdirectory of the source, the copy operation avoids recursively copying the target directory into itself. This ensures no unintended duplication of directory contents within itself.
- **`--create-subdir` Option**: If the `--create-subdir` flag is used, the source directory's contents will be copied into a new subdirectory with the same name as the source within the target directory. This effectively prevents accidental overwriting or confusion when copying directories.

#### Example:

```bash
jh_cp cp --exclude-log --exclude-zip src_folder target_folder
# --exclude-log: Excludes files matching log-related patterns (e.g., *.log, *.err).
# --exclude-zip: Excludes files matching zip-related patterns (e.g., *.zip, *.7z, *.tar.gz).

jh_cp cp --create-subdir --exclude-db src_folder target_folder
# --create-subdir: Creates a subdirectory within the target with the same name as the source directory (e.g., src_folder -> target_folder/src_folder).
# --exclude-db: Excludes files matching database-related patterns (e.g., *.db, *.sql, *.sqlite).

jh_cp cp -ignore custom/.gitignore --exclude-log src_file.txt target_folder
# --ignore: Specifies a custom ignore file (e.g., custom/.gitignore) that defines patterns to exclude during the copy.
# --exclude-log: Excludes files matching log-related patterns (e.g., *.log, *.err).

jh_cp cp --exclude-db --exclude-log --no-recursive src_folder target_folder
# --exclude-db: Excludes database-related files (e.g., *.db, *.sql, *.sqlite).
# --exclude-log: Excludes log-related files (e.g., *.log, *.err).
# --no-recursive: Prevents recursion if the target is inside the source directory, avoiding infinite loops.

```

This command copies all files from `src_folder` to `target_folder`, excluding files that match the specified exclusion patterns (such as logs and zip files).

---

### `cp_ignore` Subcommand

The `cp_ignore` subcommand is used to manage the `.cp_ignore` file, which defines file patterns to exclude during copy operations. You can register new patterns, edit the ignore list, export the current rules, or reset them to their default settings.

#### Command Syntax:

```bash
jh_cp cp_ignore [-h] [-register REGISTER] [-ignore IGNORE] [-export EXPORT] [-reset] [-nano]
```

#### Options:
- `-h`, `--help`: Show help message and exit.
- `-register REGISTER`: Register a pattern to include in the ignore file. **This automatically adds a negation rule (`!`)**, which makes the pattern an exception to the current ignore rules.  
  Example: `-register "*.log"` adds `!*.log` to the `.cp_ignore` file.
- `-ignore IGNORE`: Manually add a pattern to be ignored (e.g., `*.log`).
- `-export EXPORT`: Export the current ignore rules to a file (e.g., `output_ignore.txt`).
- `-reset`: Reset the `.cp_ignore` file to the default ignore rules.
- `-nano`: Open the `.cp_ignore` file in the nano editor (if available), allowing for manual editing.

#### Example:

```bash
# Register "!*.log" as an exception to the current ignore rules
jh_cp cp_ignore -register "*.log"

# Manually add "*.tmp" to the ignore list
jh_cp cp_ignore -ignore "*.tmp"

# Export the current ignore rules to a file
jh_cp cp_ignore -export output_ignore.txt

# Reset the ignore rules to the defaults
jh_cp cp_ignore -reset

# Edit the ignore file using nano (Only with ['Darwin', 'FreeBSD', 'NetBSD', 'OpenBSD', 'Linux'])
jh_cp cp_ignore -nano
```

This command allows you to manage your `.cp_ignore` file easily, providing flexibility in how you handle files and directories to be excluded during copy operations.

---

## Python Interface

--- 

### `jh_cp_main()` as the Entry Point

`jh_cp` is primarily a **command-line tool**, built with Python, and it requires **Python 3.9 or higher**. While the tool is intended for use through the command line interface (CLI), it also provides a Python entry point for users who wish to integrate it into their Python scripts or applications. This allows users to invoke the `jh_cp` commands programmatically, using Python as the environment.

In practice, the most common way to use the tool is via the **CLI**, where you run the tool from the command line with arguments that control its behavior. However, for Python developers, we expose functions that allow the same operations to be performed directly within Python scripts.

We recommend using `jh_cp_main()` for direct Python invocations, as it mimics the behavior of the command line interface.

#### Using `jh_cp_main()` in Python

You can invoke the `jh_cp_main()` function in your Python script, simulating the command-line interface (CLI). The function accepts arguments in the same way as the CLI and will execute the corresponding commands.

##### Example of using `jh_cp_main()` in a Python script:

```python
from jh_cp import jh_cp_main

# Simulating command-line arguments (e.g., copying files, excluding logs and zip files)
args = ['cp', 'source_folder', 'target_folder', '--exclude-log', '--exclude-zip']

# Call the main function to run the command
jh_cp_main(argv=args)
```

In this example:
- The `args` list simulates the command-line arguments you would normally pass in the terminal.
- The `jh_cp_main()` function is called, which internally handles these arguments and executes the corresponding copy operation.

The main advantage of using `jh_cp_main()` is that it abstracts away the need to manually handle argument parsing or command execution, providing a simple interface for executing the tool's operations directly from Python.

---

### Host Class for System Integration

In addition to `jh_cp_main()`, `jh_cp` provides a `Host` class, which helps manage platform-specific behaviors and the printing of output. This class is designed to make it easy for users to integrate system-specific features, such as printing messages with colors or controlling output verbosity.

#### Host Class Overview

The `Host` class is used for managing how messages are printed on different platforms (e.g., Windows, macOS, Linux). It uses system-specific mechanisms to provide colorized terminal output, making it easier to distinguish between normal messages and errors.

##### Key Methods:

- **`print()`**  
   This method is used for printing messages to the terminal. It will automatically adjust for the platform (e.g., using PowerShell or Shell), and it supports color-coding messages for better readability.

   **Parameters:**
   - `message`: The message to print.
   - `is_error`: Whether the message is an error (default is `False`).
   
   **Example Usage:**
```python
from jh_cp import host
host.print("This is a normal message.")
host.print("This is an error message.", is_error=True)
```

- **`mk_silent()`**  
   This method disables any output from the `Host` object. This can be useful if you want to suppress all output (e.g., in background processes or automated scripts).

   **Example Usage:**
```python
from jh_cp import host
host.mk_silent()  # Suppresses all output from the Host object
```

##### Host Object:

The `Host` class is initialized as a module-level object, typically referred to as `host`. You can directly use this object to print messages or suppress output as required.

```python
from jh_cp import host
# Example: Accessing the Host object
host.print("This will print normally.")
host.mk_silent()  # This will prevent any further output from being printed.
host.print("This message will not be shown.")
```

#### Platform-Specific Behavior

The `Host` class handles platform-specific differences in how output is displayed. On **Windows**, it uses PowerShell's features, while on **Unix-based systems** (macOS, Linux), it uses Shell's color capabilities. This allows for better cross-platform behavior without requiring special handling in the user's code.

#### Integration with `jh_cp_main()`

You can customize the output behavior by interacting with the `Host` object. For example, if you want to redirect or suppress output when running `jh_cp_main()` programmatically, you can configure the `Host` object before calling `jh_cp_main()`.

##### Example:

```python
from jh_cp import jh_cp_main, host

# Disable output printing
host.mk_silent()

# Run the command silently
args = ['cp', 'source_folder', 'target_folder']
jh_cp_main(argv=args)

# Output will be suppressed during the operation
```

Alternatively, you can use the `host.print()` method to direct messages to the terminal in a more controlled manner, such as with color or specific error handling.

---

### Conclusion

While `jh_cp` is designed to be used primarily as a **command-line tool**, its **Python API** provides flexibility for integration into Python scripts. By using `jh_cp_main()`, you can easily simulate command-line execution, allowing you to automate file copying operations directly from Python.

Additionally, the `Host` class allows you to manage system-specific output, making it easier to control message display, including error handling and output redirection.

For most use cases, we recommend using the **CLI** as the primary interface, with Python integration provided as a convenience for users who need to automate or script `jh_cp` operations within their Python applications.


## Default `.cp_ignore` Rules

The default ignore rules are designed to exclude common temporary or unnecessary files that are typically not needed during copying operations.

**Default `.cp_ignore` File:**

```txt
*.pyc
__pycache__/
build/
dist/
venv/
env/
pip-wheel-metadata/
*.egg-info/
*.pyo
Thumbs.db
.DS_Store
*.swp
*.swo
*.bak
make-build*/
build*/
bin/
obj/
out/
debug*/
release*/
cmake-build*/
.vscode/
.idea/
.git/
.svn/
.tox/
.coverage
node_modules/
```

These rules are automatically applied unless you specify custom rules with the `-ignore` option or modify the `.cp_ignore` file.

---

## Default `exclude-rules.ini`

The `exclude-rules.ini` configuration file allows for additional patterns to exclude specific file types. It includes predefined sections for zip, log, and database-related files.

**Default `exclude-rules.ini` File:**

```ini
[exclude-zip]
patterns = *.zip, *.7z, *.tar.gz, *.rar, *.gz, *.tgz

[exclude-log]
patterns = *.log, *.err, *.out

[exclude-db]
patterns = *.db, *.sql, *.pg, *.mdb, *.sqlite, *.sqlite3, *.accdb, *.dbf, *.ndf, *.ldf, *.frm, *.ibd
```

These exclusion patterns are automatically loaded and applied when using the `--exclude-zip`, `--exclude-log`, or `--exclude-db` options in the `cp` command.

---

### Development & Contributions

We welcome contributions! Please fork the repository, make your changes, and submit a pull request. Be sure to run tests before submitting.

---

### License

`jh_cp` is released under the Apache License 2.0. See the [LICENSE](LICENSE) file for more details.

