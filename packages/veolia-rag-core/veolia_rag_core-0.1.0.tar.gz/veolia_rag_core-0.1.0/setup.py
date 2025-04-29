from setuptools import setup, find_packages
import os

# Lê o README.md para usar como long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Lê o requirements.txt para obter as dependências
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = []
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            requirements.append(line)

setup(
    name="veolia-rag-core",
    version="0.1.0",
    author="Angelo Vicente Filho",
    author_email="angelo.vicente@veolia.com",
    description="Sistema modular de RAG (Retrieval Augmented Generation) para processamento de documentos e geração de respostas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/angelo-vicente/veolia-rag-core",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "veolia-rag=rag_core.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "rag_core": [
            "config/*.yaml",
            "config/*.json",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/angelo-vicente/veolia-rag-core/issues",
        "Source": "https://github.com/angelo-vicente/veolia-rag-core",
        "Documentation": "https://veolia-rag-core.readthedocs.io/",
    },
) 