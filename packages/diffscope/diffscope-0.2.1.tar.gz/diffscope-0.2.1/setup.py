from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="diffscope",
    version="0.2.1",
    author="DiffScope Team",
    author_email="your.email@example.com",
    description="Function-level git commit analysis tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/DiffScope",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/DiffScope/issues",
        "Documentation": "https://github.com/yourusername/DiffScope/docs",
        "Source Code": "https://github.com/yourusername/DiffScope",
    },
    package_dir={"diffscope": "src"},
    packages=["diffscope"] + ["diffscope." + pkg for pkg in find_packages(where="src")],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "PyGithub>=2.1.1",
        "tree-sitter>=0.20.1",
        "structlog>=23.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "diffscope=diffscope.cli:main",
        ],
    },
)
