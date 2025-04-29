from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="idThree_classifier",  # Hyphenated name for PyPI
    version="0.1.1",
    author="Srinu Vakada",
    author_email="your.email@example.com",
    description="A Python implementation of the ID3 decision tree algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/idThree-classifier",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "numpy",
        "graphviz",
    ],
)