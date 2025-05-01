"""
Setup script for openai-gpt-image-1-mcp package.
This is used for backward compatibility with older pip versions.
"""

from setuptools import setup

# This setup.py exists as a bridge for old pip versions
# Modern installations should use the pyproject.toml file
setup(
    name="openai-gpt-image-1-mcp",
    version="0.1.1",
    # All other configurations are in pyproject.toml
)