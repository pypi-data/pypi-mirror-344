"""
Setup script for mcp_llm_inferencer
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mcp-llm_inferencer",
    version="0.1.0",
    author="Sumedh99",
    author_email="Sumedh99@users.noreply.github.com",
    description="Uses Claude or OpenAI API to convert prompt-mapped input into concrete MCP server components such as tools, resource templates, and prompt handlers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sumedh99/mcp_llm_inferencer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
