"""
Setup script for the MCP library.
"""

from setuptools import setup, find_packages

setup(
    name="nlmdb",  # Using your package name
    version="0.1.0",
    description="Model Context Protocol Library for database operations",
    author="Rakshith Dharmappa",
    author_email="rakshith.officialmail@gmail.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "langchain>=0.1.0",
        "langchain-core>=0.1.0",
        "langchain-community>=0.0.0",
        "langchain-experimental>=0.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)