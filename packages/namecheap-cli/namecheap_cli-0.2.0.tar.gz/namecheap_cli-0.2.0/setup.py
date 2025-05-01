from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="namecheap-cli",
    version="0.2.0",
    author="Connor O'Dea",
    author_email="connor@example.com",
    description="A command-line interface for managing Namecheap DNS records",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/connorodea/namecheap-cli",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "namecheap=namecheap_cli.cli:main",
        ],
    },
)
