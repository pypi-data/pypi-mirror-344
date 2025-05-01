"""
Setup script for the acace_token_weightor package.
"""

from setuptools import setup, find_packages

# Read the content of README.md file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="acace_token_weightor",
    version="0.1.0",
    author="Sumedh Patil",
    author_email="sumedh1599@gmail.com",
    description="Token weighting module for the Adaptive Context-Aware Content Engine (ACACE)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sumedh1599/acace",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "acace_text_preprocessor>=0.1.0",
        "acace_tokenizer>=0.1.0",
    ],
    extras_require={
        "spacy": ["spacy>=3.0.0"],
        "nltk": ["nltk>=3.6.0"],
        "all": ["spacy>=3.0.0", "nltk>=3.6.0"],
    },
)
