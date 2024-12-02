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
           'copytree_with_ignore', 'handle_cp_ignore', 'jh_cp_main']


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

def should_ignore(file_path: Path, rules: list[tuple[str, bool]]) -> bool:
    """
    Determines whether a file should be ignored based on the rules.

    :param file_path: Path to the file to check
    :param rules: List of rules to apply to the file
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


def load_exclude_rules() -> dict[str, list[str]]:
    """
    Loads additional file rules from an .ini configuration file.

    :return: A dictionary of exclude rules for zip, log, and db
    """
    ...


def jh_cp_main(argv: list[str] = None) -> None:
    """
    Main function to execute the jh_cp command.

    This function provides the primary interface for the `jh_cp` command, which supports the following subcommands:
    - `cp`: Copy files/directories, with support for custom ignore rules and exclusion patterns.
    - `cp_ignore`: Manage the `.cp_ignore` file (add formats to ignore, register exceptions, export rules, reset, or edit manually).

    Usage:
        jh_cp cp -h             # Show help for the cp subcommand
        jh_cp cp_ignore -h      # Show help for the cp_ignore subcommand

    :param argv: Command line arguments (optional). If None, sys.argv is used.
    :return: None

    :param argv: Command line arguments (optional). If None, sys.argv is used.
    :return: None
    """
    ...