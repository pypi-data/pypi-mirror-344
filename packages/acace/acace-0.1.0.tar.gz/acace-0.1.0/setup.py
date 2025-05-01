"""
Setup script for the acace package.
"""

from setuptools import setup, find_packages

# Read the content of README.md file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="acace",
    version="0.1.0",
    author="Sumedh Patil",
    author_email="sumedh1599@gmail.com",
    description="Adaptive Context-Aware Content Engine (ACACE): An open-source library for optimizing token usage and ensuring content coherence in AI-driven writing",
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
        "acace_token_weightor>=0.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "mypy>=0.9.0",
        ],
        "nlp": [
            "spacy>=3.0.0",
            "nltk>=3.6.0",
        ],
        "llm": [
            "openai>=0.27.0",
        ],
        "all": [
            "spacy>=3.0.0",
            "nltk>=3.6.0",
            "openai>=0.27.0",
        ],
    },
)
