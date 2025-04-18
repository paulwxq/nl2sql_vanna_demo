# setup.py
"""
项目安装脚本
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nl2sql_demo",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="基于Python 3.12、LangChain、Vanna、LLM、pgvector和Embedding的自然语言转SQL Demo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nl2sql_demo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[
        "python-dotenv",
        "sqlalchemy",
        "psycopg2-binary",
        "langchain",
        "langchain-community",
        "pydantic",
        "vanna",
        "chromadb",
        "flask",
        "flask-cors",
        "streamlit",
    ],
)