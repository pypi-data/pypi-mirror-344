"""
Setup script for the MCP library.
"""

from setuptools import setup, find_packages

setup(
    name="nlmdb",  # Using your package name
    version="1.3.0",
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
        "langchain-huggingface>=0.0.1",
        "timm"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)