from setuptools import setup, find_packages

setup(
    name="agentic_rag",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "asyncio",
        "typing",
        "dataclasses",
        "pytest",
        "pytest-asyncio",
    ],
    author="Dev Bot",
    description="An agentic RAG system with document preservation capabilities",
    python_requires=">=3.12",  # Targeting Python 3.12 as per .python-version
)
