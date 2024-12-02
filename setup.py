from setuptools import setup, find_packages

setup(
    name="jh_cp",
    version="0.1.0",
    description="A cross-platform file copy tool with .cp_ignore management",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author="JeongHan Bae",
    author_email="mastropseudo@gmail.com",
    url="https://github.com/JeongHan-Bae/jh_cp",
    packages=find_packages(),
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
)
