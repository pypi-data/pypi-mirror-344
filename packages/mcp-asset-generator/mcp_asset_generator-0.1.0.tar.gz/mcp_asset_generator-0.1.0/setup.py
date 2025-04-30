"""
Setup script for mcp_asset_generator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mcp-asset_generator",
    version="0.1.0",
    author="Sumedh99",
    author_email="Sumedh99@users.noreply.github.com",
    description="Builds supplemental UI, helper scripts, and resource files for use in client apps like Theia, Cursor, or TypingMind with visual rendering of tools, resources, and prompts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sumedh99/mcp_asset_generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
