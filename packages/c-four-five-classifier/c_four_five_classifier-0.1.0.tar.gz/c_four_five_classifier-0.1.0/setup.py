from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="c_four_five_classifier",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Python implementation of C4.5 decision tree algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/c-four-five-classifier",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "graphviz>=0.14.0",
    ],
)