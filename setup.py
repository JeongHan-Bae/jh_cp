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
import subprocess
import sys

from setuptools import setup, Command
import zipfile

from setuptools.command.bdist_wheel import bdist_wheel  # noqa: Meet the needs in requirements to build
from setuptools.command.install import install

# Set the project directory and version
__setup_dir__ = os.path.dirname(os.path.abspath(__file__))
__version__ = "2.0.0"  # major feature release

# Description: The package name and version for distribution
__package_name__ = "jh_cp"
__description__ = "A cross-platform file copy and archive tool with .cp_ignore management"
__author__ = "JeongHan Bae"
__author_email__ = "mastropseudo@gmail.com"
__url__ = "https://github.com/JeongHan-Bae/jh_cp"


class AddFilesToWheelCommand(Command):
    description = 'Add .pyi files to the generated .whl file'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # Find the generated .whl file
        wheel_file = os.path.join(__setup_dir__, 'dist', f'jh_cp-{__version__}-py3-none-any.whl')
        files = ['jh_cp.pyi', 'jh_cp_tools/.cp_ignore', 'jh_cp_tools/exclude-rules.ini']
        # Use zipfile to add the .pyi file to the .whl package
        with zipfile.ZipFile(wheel_file, 'a') as whl:
            for file in files:
                if not os.path.isfile(file):
                    print(f"Error: {file} file does not exist.")
                    return
                whl.write(os.path.join(__setup_dir__, file), file)

        print(f"Added {files},  to {wheel_file}")


# Inherit from bdist_wheel and override the run method
class CustomBdistWheelCommand(bdist_wheel):
    def run(self):
        # Call the parent class's run method to generate the .whl file
        super().run()  # No need to explicitly pass the class name and self

        # After generating the .whl file, execute the add_pyi command
        AddFilesToWheelCommand(self.distribution).run()


class BuildInstallCommand(install):
    description = 'Build the package and then install it'

    def run(self):
        # First, execute the build process to generate sdist and wheel files
        self.run_command('sdist')
        self.run_command('bdist_wheel')

        # Install the .whl file
        wheel_file = os.path.join(__setup_dir__, 'dist', f'jh_cp-{__version__}-py3-none-any.whl')
        print(f"Installing the wheel file: {wheel_file}")
        subprocess.check_call([
            sys.executable,
            "-m", "pip", "install", "--force-reinstall", "--no-cache-dir", wheel_file
        ])

        # Then, execute the installation command
        print("Installation complete.")


class CleanCommand(Command):
    description = "Clean build and egg-info directories"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # clear build/
        build_dir = os.path.join(__setup_dir__, 'build')
        if os.path.exists(build_dir):
            print(f"Removing {build_dir}")
            shutil.rmtree(build_dir)

        # clear *.egg-info/
        egg_info_dir = os.path.join(__setup_dir__, f'{__package_name__}.egg-info')
        if os.path.exists(egg_info_dir):
            print(f"Removing {egg_info_dir}")
            shutil.rmtree(egg_info_dir)


setup(
    name=__package_name__,
    version=__version__,
    description=__description__,
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    py_modules=['jh_cp'],
    entry_points={
        'console_scripts': [
            'jh_cp = jh_cp:jh_cp_main',
        ],
    },
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    license="Apache License 2.0",
    cmdclass={
        'bdist_wheel': CustomBdistWheelCommand,  # Override the default bdist_wheel
        'build_install': BuildInstallCommand,
        'clean': CleanCommand,
    }
)
