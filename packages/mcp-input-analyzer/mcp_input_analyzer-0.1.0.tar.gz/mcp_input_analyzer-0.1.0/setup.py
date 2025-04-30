"""
Setup script for mcp_input_analyzer
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mcp-input_analyzer",
    version="0.1.0",
    author="Sumedh99",
    author_email="Sumedh99@users.noreply.github.com",
    description="Analyzes user-described build features (e",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sumedh99/mcp_input_analyzer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
