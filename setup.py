#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="twbank-fx-client",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="台灣銀行外匯匯率查詢 API 客戶端",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/twbank-fx-api-client",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "pandas>=2.0.0",
        "html5lib>=1.1",
    ],
    entry_points={
        'console_scripts': [
            'twbank-fx=twbank_fx_client.cli:main',
        ],
    },
)
