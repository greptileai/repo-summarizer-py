from setuptools import setup, find_packages

setup(
    name="repo-summarizer",
    version="1.0.0",
    description="A CLI tool to summarize files in a directory using OpenAI",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "repo-summarizer=src.main:main",
        ],
    },
    python_requires=">=3.8",
    keywords=["cli", "openai", "summarizer", "files"],
    author="",
    license="MIT",
)