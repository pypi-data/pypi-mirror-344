from setuptools import setup, find_packages

# Constants
PACKAGE_NAME = "financial_tracker"
VERSION = "0.1.0"
AUTHOR = "Jiawang Liu"
AUTHOR_EMAIL = "rainingalltheday@163.com"
DESCRIPTION = "A personal finance tracking system"
LICENSE = "MIT"
KEYWORDS = "finance, personal finance, expense tracker"


setup(
    # Package metadata
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    keywords=KEYWORDS,

    # Package configuration
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["*.csv", "*.json"],
    },
    python_requires=">=3.9",
    install_requires=[
        "matplotlib",
        "numpy",
        "pandas",
        "scikit-learn",
    ],
    extras_require={
        "dev": ["pytest", "flake8", "black"],  # Optional dependencies for development
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # Entry points for CLI
    entry_points={
        "console_scripts": [
            "financial-tracker=financial_tracker.cli:main",
        ],
    },

    # License files
    license_files=("LICENSE",),
)