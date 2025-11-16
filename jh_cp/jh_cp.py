#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2024 JeongHan Bae <mastropseudo@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import shutil
import argparse
import sys
from pathlib import Path
import platform
import configparser
import subprocess
import zipfile
import tarfile
import fnmatch

__all__ = ['Host', 'host', 'load_ignore_rules', 'load_exclude_rules', 'should_ignore',
           'copytree_with_ignore', 'create_archive_with_ignore', 'handle_cp_ignore', 'draw_tree_with_ignore',
           'jh_cp_main']


class Host:
    shell_failed: bool = False

    def __init__(self):
        self.system = platform.system()

        # Bind the correct print method based on the system type
        if self.system == 'Windows':
            self.print = Host._print_windows
        else:
            self.print = Host._print_unix

    def mk_silent(self):
        def silent_print(*args, **kwargs):  # noqa
            pass

        self.print = silent_print

    @staticmethod
    def _print_unix(message: str, is_error: bool = False):
        """
        Prints the message with colors on Unix-like systems (via echo command).

        :param message: The message to print
        :param is_error: Whether the message is an error (default is False)
        :return: None
        """
        if not Host.shell_failed:
            try:
                # Attempt to use the system's echo command for colored output
                color_code = '91' if is_error else '93'  # Red -> 91, Yellow -> 93
                subprocess.run(f"echo \"\033[{color_code}m{message}\033[0m\"", shell=True, check=True,
                               encoding='utf-8')
                return
            except (subprocess.CalledProcessError, OSError, Exception) as e:
                # If the shell command fails, catch the exception and fall back to normal print
                print(f"Shell command failed: {e}", file=sys.stderr)
            finally:
                Host.shell_failed = True
                # Catch the exception and fall back to normal printing
        print(message, file=sys.stderr if is_error else sys.stdout)

    @staticmethod
    def _print_windows(message: str, is_error: bool = False):
        """
        Prints the message with colors on Windows (via PowerShell or cmd).

        :param message: The message to print
        :param is_error: Whether the message is an error (default is False)
        :return: None
        """
        if not Host.shell_failed:
            try:
                color_code = 'Red' if is_error else 'Yellow'
                # Use PowerShell's Write-Host to print colored text
                # Use UTF-8 encoding to ensure correct output of Chinese characters
                subprocess.run(["powershell", "-Command",
                                f"Write-Host \"{message}\" -ForegroundColor {color_code}"],
                               check=True, encoding='utf-8')
                return
            except (subprocess.CalledProcessError, OSError, Exception) as e:
                # If the PowerShell command fails
                print(f"PowerShell command failed: {e}", file=sys.stderr)
            finally:
                Host.shell_failed = True
                # Catch the exception and fall back to normal printing
        print(message, file=sys.stderr if is_error else sys.stdout)


# Initialize the host
host = Host()

CP_IGNORE_DEFAULT = "jh_cp_tools/.cp_ignore"
DEFAULT_IGNORE_RULES = [
    # Python bytecode & metadata
    "*.py[cod]", "*.pyc", "*.pyo", "__pycache__/", "*.egg-info/", "*.egg", "pip-wheel-metadata/",
    # Build & virtual environment directories
    "*build*/", "*Build*/", "*BUILD*/", "dist/", "venv/", "env/",
    # System-generated files
    "Thumbs.db", ".DS_Store", "*.swp", "*.swo", "*.bak",
    # Native & compiled binary artifacts
    "bin/", "obj/", "out/", "*debug*/", "*release*/",
    # Development & project settings
    ".vscode/", ".idea/", ".git/", ".svn/", ".tox/", ".coverage", "node_modules/",
]
EXCLUDE_RULES_INI = "jh_cp_tools/exclude-rules.ini"


def load_ignore_rules(ignore_path: Path, additional_patterns: list[str] = None) -> list[tuple[str, bool]]:
    rules = []

    if ignore_path.exists():
        with open(ignore_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue  # Skip blank or comment lines
                line = line.split("#", 1)[0].strip()  # Remove trailing inline comment
                if not line:
                    continue
                if line.startswith("!"):
                    rules.append((line[1:].strip(), True))  # Include rule (exception)
                else:
                    rules.append((line.strip(), False))  # Ignore rule
    else:
        for rule in DEFAULT_IGNORE_RULES:
            rules.append((rule, False))  # Default rules are ignore rules

    if additional_patterns:
        rules.extend((pattern.strip(), False) for pattern in additional_patterns)

    normalized = []
    for pattern, is_include in rules:
        if not pattern:
            continue

        if ('/' not in pattern or
                (pattern.endswith('/')
                 and not pattern.startswith('/')
                 and not pattern.startswith('**/'))):
            normalized.append((f"**/{pattern}", is_include))

        normalized.append((pattern, is_include))

    return normalized


def should_ignore(file_path: Path, rules: list[tuple[str, bool]], is_dir: bool = False) -> bool:
    # Convert to POSIX-like string to match patterns like **/release*/
    file_str = file_path.as_posix()
    if is_dir:
        if not str(file_path).endswith('/'):
            file_str += '/'
        dir_rules = (
            (pattern, is_include)
            for pattern, is_include in reversed(rules)
            if pattern.endswith('/')
        )
        for pattern, is_include in dir_rules:
            if fnmatch.fnmatch(file_str, pattern):
                return not is_include  # If it's an include rule, return False (do not ignore), else return True (ignore)
    else:
        for pattern, is_include in reversed(rules):
            if fnmatch.fnmatch(file_str, pattern):
                return not is_include
    return False  # If no rules match, do not ignore the file


def copytree_with_ignore(src: Path, target: Path, rules: list[tuple[str, bool]], create_subdir: bool = False) -> None:
    src = Path(src).resolve()
    target = Path(target).resolve()
    if src.is_dir() and create_subdir:
        target = target / src.name

    if target.is_relative_to(src):
        # If subdir, add the relative path to ignore_rules
        relative_target_path = target.relative_to(src)
        length = len(relative_target_path.parts)

        for i in range(length):
            subdir_path = Path(*relative_target_path.parts[:i + 1])
            if not os.path.isdir(subdir_path):  # Check if the directory exists
                rules.append((f"{subdir_path}/", False))  # Add the first non-existing directory to the rules
                break

    # Ensure the target directory exists if copying a directory
    if not target.exists():
        try:
            os.makedirs(target)
        except FileNotFoundError:
            # This exception is raised if part of the path is a file instead of a directory
            host.print(f"Some part of the Target Dir '{target}' is a File", True)
            return  # Return or exit the function to avoid further operations
        except PermissionError as e:
            host.print(f"Permission Denied: {e.filename}", True)
            return
        except Exception as e:
            host.print(f"Unexpected error: {str(e)}", True)
            return
    # === Handle the case where src is a file ===
    if src.is_file():
        # Ensure the target is a directory
        if not target.is_dir():
            raise ValueError(f"Target {target} must be a directory if copying a file.")
        shutil.copy(src, target / src.name)
        host.print(f"Copied file from {src} to {target / src.name}.")

    # === Handle the case where src is a directory ===
    # Ignore function
    def ignore_func(_dir: str, files: list[str]) -> list[str]:
        dir_path = Path(_dir)
        rel_dir = dir_path.relative_to(src)

        # If the directory itself should be ignored, return all files
        if should_ignore(rel_dir, rules, is_dir=True):
            return [file for file in files]

        ignored = []
        for file in files:
            file_path = rel_dir / file
            if (dir_path / file).is_dir():
                if should_ignore(file_path, rules, is_dir=True):
                    # Entire subdirectory is ignored: tell copytree to skip it completely
                    ignored.append(file)
            else:
                if should_ignore(file_path, rules):
                    ignored.append(file)
        return ignored

    try:
        shutil.copytree(src, target, ignore=ignore_func, dirs_exist_ok=True)
        host.print(f"Copied from {src} to {target}, skipping ignored files.")
    except shutil.Error as e:
        # Catch errors during copying
        for _, dst_file, _ in e.args[0]:
            host.print(f"Permission Denied: {dst_file}", True)
    except PermissionError as e:
        host.print(f"Permission Denied: {e.filename}", True)
    except Exception as e:
        host.print(f"Unexpected error: {str(e)}", True)


def create_archive_with_ignore(src: Path, output: Path, rules: list[tuple[str, bool]]) -> None:
    src = Path(src).resolve()
    output = Path(output).resolve()

    suffix = output.suffix.lower()
    archive_format: str
    if suffix == ".zip":
        archive_format = "zip"
    elif suffix == ".tar":
        archive_format = "tar"
    elif suffix in [".tgz", ".tar.gz"]:
        archive_format = "tgz"
    else:
        host.print("Unsupported archive format. Use .zip, .tar, or .tar.gz/.tgz", True)
        return

    if output.is_relative_to(src):
        # If subdir, add the relative path to ignore_rules
        relative_target_path = output.relative_to(src)
        rules.append((str(relative_target_path), False))

    # === Handle single file case (skip rules) ===
    if src.is_file():
        try:
            arc_name = src.name
            if archive_format == "zip":
                with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zip_f:
                    zip_f.write(src, arcname=arc_name)
            else:
                mode = 'w:gz' if archive_format == "tgz" else 'w'
                with tarfile.open(output, mode) as tar_f:
                    tar_f.add(src, arcname=arc_name)
            host.print(f"Archived file {src} -> {output}")
        except Exception as e:
            host.print(f"Failed to archive file: {str(e)}", True)
        return

    # === Directory case with rules ===
    if not src.is_dir():
        host.print(f"Source {src} must be a directory or file.", True)
        return

    def archive_filter(filepath: Path) -> bool:
        relpath = filepath.relative_to(src)
        return not should_ignore(relpath, rules)

    try:
        if archive_format == "zip":
            with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zip_f:
                for root, dirs, files in os.walk(src):
                    root_path = Path(root)
                    rel_root = root_path.relative_to(src)
                    # pre-filter directories to ignore
                    dirs[:] = [
                        d for d in dirs
                        if not should_ignore(rel_root / d, rules, is_dir=True)
                    ]
                    for file in files:
                        full_path = Path(root) / file
                        rel_path = full_path.relative_to(src)
                        if archive_filter(full_path):
                            zip_f.write(full_path, arcname=str(rel_path))
            host.print(f"ZIP archive created at {output}")

        elif archive_format in ["tar", "tgz"]:
            mode = 'w:gz' if archive_format == "tgz" else 'w'
            print(f"rules: {rules}")
            with tarfile.open(output, mode) as tar_f:
                for root, dirs, files in os.walk(src):
                    root_path = Path(root)
                    # pre-filter directories to ignore
                    rel_root = root_path.relative_to(src)
                    dirs[:] = [
                        d for d in dirs
                        if not should_ignore(rel_root / d, rules, is_dir=True)
                    ]
                    for file in files:
                        full_path = Path(root) / file
                        rel_path = full_path.relative_to(src)
                        if archive_filter(full_path):
                            tar_f.add(full_path, arcname=str(rel_path))
                            print(full_path)
            host.print(f"TAR archive created at {output}")

    except Exception as e:
        host.print(f"Failed to create archive: {str(e)}", True)


def handle_cp_ignore(args: argparse.Namespace) -> None:
    """Handles the cp_ignore subcommand to manage the .cp_ignore file."""
    cp_ignore_path = Path(os.path.dirname(os.path.abspath(__file__))) / CP_IGNORE_DEFAULT

    if args.register:
        with open(cp_ignore_path, "a") as f:
            for pattern in args.register:
                f.write(f"!{pattern}\n")
        host.print(f"Registered {[f'!{p}' for p in args.register]} in {cp_ignore_path}")

    elif args.ignore:
        with open(cp_ignore_path, "a") as f:
            for pattern in args.ignore:
                f.write(f"{pattern}\n")
        host.print(f"Ignored {args.ignore} in {cp_ignore_path}")

    elif args.export:
        shutil.copy(cp_ignore_path, args.export)
        host.print(f"Exported ignore rules to {args.export}")

    elif args.reset:
        with open(cp_ignore_path, "w") as f:
            f.writelines(f"{rule}\n" for rule in DEFAULT_IGNORE_RULES)
        host.print(f"Reset {cp_ignore_path} to default rules.")

    elif args.nano:
        # Check if Unix-like system (macOS, BSD, Linux, etc.)
        if platform.system() in ['Darwin', 'FreeBSD', 'NetBSD', 'OpenBSD', 'Linux']:
            os.system(f"nano {cp_ignore_path}")
        else:
            host.print(f"Nano might not be available on your system. "
                       f"Please edit {cp_ignore_path} manually.")
    else:
        host.print("No valid action specified for cp_ignore.")


def draw_tree_with_ignore(src: Path, rules: list[tuple[str, bool]], max_depth: int | None = None) -> None:
    """
    Draws the directory tree structure while applying "ignore rules".
    Matching logic identical to copytree_with_ignore().
    """
    src = Path(src).resolve()
    if not src.exists():
        host.print(f"Source {src} does not exist.", True)
        return
    if not src.is_dir():
        host.print(f"Source {src} must be a directory.", True)
        return

    def _draw(current: Path, prefix: str = "", depth: int = 0):
        if max_depth is not None and depth > max_depth:
            return

        try:
            entries = sorted(current.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except PermissionError:
            host.print(f"Permission denied: {current}", True)
            return

        rel_dir = current.relative_to(src)
        visible_entries = [
            e for e in entries
            if not should_ignore(rel_dir / e.name, rules, is_dir=e.is_dir())
        ]

        total = len(visible_entries)
        for i, entry in enumerate(visible_entries):
            is_last = (i == total - 1)
            connector = "└── " if is_last else "├── "

            display_name = entry.name + "/" if entry.is_dir() else entry.name
            host.print(f"{prefix}{connector}{display_name}")

            if entry.is_dir():
                new_prefix = prefix + ("    " if is_last else "│   ")
                _draw(entry, new_prefix, depth + 1)

    host.print(src.name + "/")
    _draw(src)


def load_exclude_rules() -> dict[str, list[str]]:
    """Load exclusion rules from the INI File"""
    exclude_rules = {}
    rules_path = Path(os.path.dirname(os.path.abspath(__file__))) / EXCLUDE_RULES_INI
    config = configparser.ConfigParser()

    if os.path.exists(rules_path):
        config.read(rules_path)

        # Get exclude-zip, exclude-log, and exclude-db rules
        for section in ['exclude-zip', 'exclude-log', 'exclude-db']:
            if config.has_section(section):
                patterns = config.get(section, 'patterns', fallback='').split(',')
                exclude_rules[section] = [pattern.strip() for pattern in patterns if pattern.strip()]

    return exclude_rules


def jh_cp_main(argv: list[bytes] = None) -> None:
    """Main function to execute the jh_cp command."""
    parser = argparse.ArgumentParser(description="jh_cp script with ignore functionality")
    subparsers = parser.add_subparsers(dest="command")
    if argv is None:
        argv = sys.argv[1:]

    # jh_cp command for file copying
    cp_parser = subparsers.add_parser("cp", help="Copy files or directories with ignore rules")
    cp_parser.add_argument("src", type=str, help="Source path [Directory / File]")
    cp_parser.add_argument("target", type=str, help="Target path [Directory]")
    cp_parser.add_argument("-ignore", type=str, help="Custom ignore file path")
    cp_parser.add_argument("--exclude-zip", action='store_true', help="Exclude zip-related patterns")
    cp_parser.add_argument("--exclude-log", action='store_true', help="Exclude log-related patterns")
    cp_parser.add_argument("--exclude-db", action='store_true', help="Exclude db-related patterns")
    cp_parser.add_argument("--create-subdir", action='store_true',
                           help="Create a subdirectory with the same name as the source")

    # archive command for creating compressed archives
    archive_parser = subparsers.add_parser("archive", help="Create an archive with ignore rules")
    archive_parser.add_argument("src", type=str, help="Source directory to archive")
    archive_parser.add_argument("output", type=str, help="Output archive file path (with .zip/.tar/.tar.gz)")
    archive_parser.add_argument("-ignore", type=str, help="Custom ignore file path")
    archive_parser.add_argument("--exclude-zip", action='store_true', help="Exclude zip-related patterns")
    archive_parser.add_argument("--exclude-log", action='store_true', help="Exclude log-related patterns")
    archive_parser.add_argument("--exclude-db", action='store_true', help="Exclude db-related patterns")

    # cp_ignore subcommand for managing .cp_ignore
    cp_ignore_parser = subparsers.add_parser("cp_ignore", help="Manage .cp_ignore rules")
    cp_ignore_parser.add_argument("-register", nargs="+", help="Register pattern(s) to include")
    cp_ignore_parser.add_argument("-ignore", nargs="+", help="Ignore pattern(s)")
    cp_ignore_parser.add_argument("-export", type=str, help="Export current ignore rules to file")
    cp_ignore_parser.add_argument("-reset", action='store_true', help="Reset to default ignore rules")
    cp_ignore_parser.add_argument("-nano", action='store_true', help="Open .cp_ignore with nano editor")

    # tree command for displaying directory structure
    tree_parser = subparsers.add_parser("tree", help="Display directory structure with ignore rules")
    tree_parser.add_argument("src", type=str, help="Source directory to visualize")
    tree_parser.add_argument("-ignore", type=str, help="Custom ignore file path")
    tree_parser.add_argument("--exclude-zip", action='store_true', help="Exclude zip-related patterns")
    tree_parser.add_argument("--exclude-log", action='store_true', help="Exclude log-related patterns")
    tree_parser.add_argument("--exclude-db", action='store_true', help="Exclude db-related patterns")
    tree_parser.add_argument("--max-depth", type=int, default=None, help="Optional maximum depth to traverse")

    args = parser.parse_args(argv)

    if args.command == "cp" or args.command == "archive":
        if args.command == "cp":
            if os.path.isfile(args.target):
                host.print(f"FileExistsError: {args.target} is a File instead of a Directory", True)
                return
        elif args.command == "archive":
            if not args.output.endswith(('.zip', '.tar', '.tar.gz', '.tgz')):
                host.print("Output must end with .zip, .tar, or .tar.gz/.tgz", True)
                return
        exclude_rules = load_exclude_rules()
        additional_rules = []

        if args.exclude_zip:
            additional_rules.extend(exclude_rules.get('exclude-zip', []))
        if args.exclude_log:
            additional_rules.extend(exclude_rules.get('exclude-log', []))
        if args.exclude_db:
            additional_rules.extend(exclude_rules.get('exclude-db', []))
        ignore_path = Path(args.ignore) if args.ignore else Path(
            os.path.dirname(os.path.abspath(__file__))) / CP_IGNORE_DEFAULT
        rules = load_ignore_rules(ignore_path, additional_rules)
        if args.command == "cp":
            rules.append((str(Path(args.target).resolve()) + '/', False))
            copytree_with_ignore(args.src, args.target, rules, args.create_subdir)
        elif args.command == "archive":
            rules.append((str(Path(args.output).resolve()), False))  # Ensure the output archive is ignored
            create_archive_with_ignore(args.src, args.output, rules)
    elif args.command == "cp_ignore":
        handle_cp_ignore(args)

    elif args.command == "tree":
        src_path = Path(args.src).resolve()
        exclude_rules = load_exclude_rules()
        additional_rules = []
        if args.exclude_zip:
            additional_rules.extend(exclude_rules.get('exclude-zip', []))
        if args.exclude_log:
            additional_rules.extend(exclude_rules.get('exclude-log', []))
        if args.exclude_db:
            additional_rules.extend(exclude_rules.get('exclude-db', []))

        ignore_path = Path(args.ignore) if args.ignore else Path(
            os.path.dirname(os.path.abspath(__file__))) / CP_IGNORE_DEFAULT
        rules = load_ignore_rules(ignore_path, additional_rules)

        draw_tree_with_ignore(src_path, rules, args.max_depth)

    elif not argv:
        host.print("Hello from JeongHan's Copying Tool.")


if __name__ == "__main__":
    jh_cp_main()
