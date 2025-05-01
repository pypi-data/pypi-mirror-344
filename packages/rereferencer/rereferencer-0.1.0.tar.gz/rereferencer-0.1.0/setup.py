from setuptools import setup, find_packages

setup(
    name="rereferencer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "biopython>=1.81",
        "pandas>=2.0.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "rereferencer=primer_extractor.cli:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to extract amplified regions from reference sequences using primer pairs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rereferencer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 