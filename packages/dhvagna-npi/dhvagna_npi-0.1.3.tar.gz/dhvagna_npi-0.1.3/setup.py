"""
Setup script for dhvagna-npi package.
"""

import os
from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="dhvagna-npi",
    version="0.1.3",
    author="Gnanesh Balusa",
    author_email="gnaneshbalusa016g@gmail.com",
    description="Advanced voice transcription tool with multi-language support outperformed current llm models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gnanesh-16/dhvagna-npi",
    project_urls={
        "Bug Tracker": "https://github.com/gnanesh-16/dhvagna-npi/issues",
        "Documentation": "https://github.com/gnanesh-16/dhvagna-npi#readme",
        "Source Code": "https://github.com/gnanesh-16/dhvagna-npi",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Text Processing",
        "Environment :: Console",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "dhvagna-npi=dhvagna_npi.core:main",
            "dhvagna-npi-interactive=dhvagna_npi.core:run_interactive",
        ],
    },
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'isort>=5.10.0',
            'mypy>=0.950',
            'build>=0.8.0',
            'twine>=4.0.0',
            'pre-commit>=2.20.0',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)