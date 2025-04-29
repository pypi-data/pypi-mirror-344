#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mcp-server-moralis",
    version="0.1.0",
    description="基于Model Context Protocol (MCP)的Moralis区块链API服务器",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DAOCAT",
    url="https://github.com/DAOCAT/mcp-server-moralis",
    py_modules=["main"],  # 明确指定顶级模块
    install_requires=[
        "httpx>=0.28.1",
        "mcp>=1.6.0",
        "python-dotenv>=1.0.0",
        "moralis>=0.1.37",
        "fastmcp>=1.0",
    ],
    extras_require={
        "dev": [
            "black>=24.1.0",
            "isort>=5.12.0",
            "pytest>=7.4.0",
        ],
    },
    python_requires=">=3.12",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "mcp-server-moralis=main:main",
        ],
    },
) 