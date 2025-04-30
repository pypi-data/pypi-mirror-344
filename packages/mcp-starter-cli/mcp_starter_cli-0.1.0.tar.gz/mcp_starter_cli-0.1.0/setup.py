"""
Setup script for mcp_starter_cli
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mcp-starter_cli",
    version="0.1.0",
    author="Sumedh99",
    author_email="Sumedh99@users.noreply.github.com",
    description="CLI tool to scaffold, run, and test MCP servers locally with Node",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sumedh99/mcp_starter_cli",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
