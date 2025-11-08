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

import argparse
from pathlib import Path

__all__ = ['Host', 'host', 'load_ignore_rules', 'load_exclude_rules', 'should_ignore',
           'copytree_with_ignore', 'create_archive_with_ignore', 'handle_cp_ignore', 'draw_tree_with_ignore',
           'jh_cp_main']


class Host:
    """the Host object based on the platform system."""
    _print_unix: callable = None
    _print_windows: callable = None

    def print(self, message: str, is_error: bool = False):
        """
        Prints the message with colors on Terminal (via PowerShell or Shell depending on the system).

        :param message: The message to print
        :param is_error: Whether the message is an error (default is False)
        :return: None
        """
        ...

    def mk_silent(self):
        """
        Forbid the host object from printing the output.
        :return: None
        """


host: Host
"""
The module level host object use for printing.
"""


def load_ignore_rules(ignore_path: Path, additional_patterns: list[str] = None) -> list[tuple[str, bool]]:
    """
    Loads the ignore rules from the given path. If the path does not exist, default rules are used.

    :param ignore_path: Path to the ignore rules file
    :param additional_patterns: Optional additional patterns to include in the rules
    :return: A list of tuples where each tuple is a pattern and a flag (True for exception, False for ignore)
    """
    ...


def should_ignore(file_path: Path, rules: list[tuple[str, bool]], is_dir: bool = False) -> bool:
    """
    Determines whether a file or directory should be ignored based on the rules.

    :param file_path: Path to the file or directory to check
    :param rules: List of rules to apply (pattern, is_include)
    :param is_dir: Whether the path is a directory (affects pattern matching)
    :return: True if the file should be ignored, False otherwise
    """
    ...


def copytree_with_ignore(src: Path, target: Path, rules: list[tuple[str, bool]]) -> None:
    """
    Copies the directory tree from src to target, ignoring files based on the provided rules.
    May print the errors {shutil.Error, PermissionError} through Host.

    :param src: Source directory path (can be a Directory or a File)
    :param target: Target directory path (MUST be a Directory)
    :param rules: List of ignore rules
    :return: None
    """
    ...


def create_archive_with_ignore(src: Path, output: Path, rules: list[tuple[str, bool]]) -> None:
    """
    Creates a ZIP or TAR archive from the source directory, ignoring files based on the provided rules.

    :param src: Source directory to archive (can be a Directory or a File)
    :param output: Output archive path (.zip, .tar, or .tar.gz)
    :param rules: List of ignore rules
    :return: None
    """
    ...


def handle_cp_ignore(args: argparse.Namespace) -> None:
    """
    Handles the cp_ignore subcommand to manage the .cp_ignore file.

    This function supports the following operations via the `args` parsed from argparse:
      - Register a format to include in the ignore file using the `-register` option.
      - Add a format to ignore using the `-ignore` option.
      - Export the current ignore rules to a specified file using the `-export` option.
      - Reset the ignore rules back to their default values using the `-reset` option.
      - Open the `.cp_ignore` file in the nano editor for manual editing using the `-nano` option.

    Usage:
        jh_cp cp_ignore [-h] [-register *REGISTER*] [-ignore *IGNORE*] [-export *EXPORT*] [-reset] [-nano]

    :param args: Parsed arguments from argparse
    :return: None
    """
    ...


def draw_tree_with_ignore(src: Path, rules: list[tuple[str, bool]], max_depth: int | None = None) -> None:
    """
    Draws the directory tree structure while applying ignore rules.

    This function visualizes the directory hierarchy starting from the given source path,
    skipping all files and directories matching the ignore patterns.
    The matching logic is identical to `copytree_with_ignore`, ensuring consistent results
    when previewing which files will be included or excluded before performing copy or archive.

    :param src: Root directory path to display
    :param rules: List of ignore rules (pattern, is_include)
    :param max_depth: Optional maximum recursion depth limit
    :return: None
    """
    ...


def load_exclude_rules() -> dict[str, list[str]]:
    """
    Loads additional file rules from an .ini configuration file.

    :return: A dictionary of exclude rules for zip, log, and db
    """
    ...


def jh_cp_main(argv: list[str] = None) -> None:
    """
    Main entry point for the `jh_cp` command-line tool.

    Supports structured copying and archiving with `.cp_ignore` rules, pattern-based exclusions,
    and interactive rule management.

    Supported Subcommands:
    ----------------------

    - **cp**  
      Copy files or directories with to-ignore and exclusion rules.

      * Arguments:

        >> `src`               Source path (file or directory)

        >> `target`            Destination directory

      * Options:

        >> `--create-subdir`     Place contents inside a subdirectory named after source

        >> `--exclude-zip`       Exclude archive files (*.zip, *.tar.gz, *.7z, etc.)

        >> `--exclude-log`       Exclude log files (*.log, *.err, *.out)

        >> `--exclude-db`        Exclude DB files (*.db, *.sqlite, *.sql, etc.)

        >> `-ignore FILE`        Use custom ignore rule file (default is .cp_ignore)

    - **archive**  
      Create a compressed archive from a directory while applying to-ignore and exclusion rules.

      * Arguments:

        >> `src`               Source directory to archive

        >> `output`            Output file path (.zip, .tar, .tar.gz, .tgz)

      * Options:

        >> `--exclude-zip`       Exclude archive files (*.zip, *.tar.gz, *.7z, etc.)

        >> `--exclude-log`       Exclude log files (*.log, *.err, *.out)

        >> `--exclude-db`        Exclude DB files (*.db, *.sqlite, *.sql, etc.)

        >> `-ignore FILE`        Use custom ignore rule file (default is .cp_ignore)

    - **cp_ignore**  
      Manage `.cp_ignore` rules and behaviors.

      * Options:

        >> `-register PATTERN`   Add an inclusion rule (equivalent to !PATTERN)

        >> `-ignore PATTERN`     Add an exclusion rule

        >> `[-export FILE]`      Export current rules to file

        >> `[-reset]`            Reset to default ignore rules

        >> `[-nano]`             Open `.cp_ignore` in nano editor (Unix-like only)

    - **tree**
      Display directory structure while applying the same ignore logic as copy and archive.

      * Arguments:

        >> `src`                 Source directory to visualize

      * Options:

        >> `--max-depth N`       Limit traversal depth (optional)

        >> `--exclude-zip`       Exclude archive files (*.zip, *.tar.gz, *.7z, etc.)

        >> `--exclude-log`       Exclude log files (*.log, *.err, *.out)

        >> `--exclude-db`        Exclude DB files (*.db, *.sqlite, *.sql, etc.)

        >> `-ignore FILE`        Use custom ignore rule file (default is .cp_ignore)

    Notes:
    ------

    - Ignore rules follow `.gitignore`-like syntax with glob patterns.

    - Lines starting with '!' define inclusion exceptions.

    >> `exclude-rules.ini` allows external configuration of file-type-based exclusion.

    :param argv: Optional list of command-line arguments (default: sys.argv[1:])
    :return: None
    """
